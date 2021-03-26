import RPi.GPIO as GPIO
import time
import datetime
from constants import Constants

import robot
import belt
import phototransistor
import led
import motor
import protocol
import logger
import switch
import detect


class Controller:
    __robot: robot.Robot = None
    __sorting_belt: belt.SortingBelt = None
    __main_belt: belt.Belt = None
    __phototransistor: phototransistor.Phototransistor = None
    __gate_led: led.Led = None
    __color_led: led.Led = None
    __main_switch: switch.Switch = None
    __protocol: protocol.Protocol = None
    __logger: logger.Logger = None
    __running: bool = False
    __detect: detect.Detect = None

    def __init__(self):
        self.__running = False
        self.__gate_led = led.Led(Constants.GATE_LIGHT_PIN.value)
        self.__color_led = led.Led(Constants.COLOR_LIGHT_PIN.value)
        self.__robot = robot.Robot(
            motor.Motor(
                Constants.ROBOT_MOTOR_FORWARD_PIN.value,
                Constants.ROBOT_MOTOR_BACKWARD_PIN.value,
                Constants.ROBOT_MOTOR_ENABLE_PIN.value,
                Constants.ROBOT_MOTOR_VIBRATION_PIN.value,
                self.motor_panic,
            ),
            switch.Switch(Constants.ROBOT_START_SWITCH_PIN.value),
            switch.Switch(Constants.ROBOT_ARRIVAL_SWITCH_PIN.value),
        )
        self.__sorting_belt = belt.SortingBelt(
            motor.Motor(
                Constants.SORTING_BELT_MOTOR_FORWARD_PIN.value,
                Constants.SORTING_BELT_MOTOR_BACKWARD_PIN.value,
                Constants.SORTING_BELT_MOTOR_ENABLE_PIN.value,
                Constants.SORTING_BELT_VIBRATION_PIN.value,
                self.motor_panic,
            )
        )
        self.__main_belt = belt.Belt(
            motor.Motor(
                Constants.MAIN_BELT_MOTOR_FORWARD_PIN.value,
                Constants.MAIN_BELT_MOTOR_BACKWARD_PIN.value,
                Constants.MAIN_BELT_MOTOR_ENABLE_PIN.value,
            )
        )
        self.__phototransistor = phototransistor.Phototransistor(
            Constants.PHOTOTRANSISTOR_CLK_PIN.value,
            Constants.PHOTOTRANSISTOR_DOUT_PIN.value,
            Constants.PHOTOTRANSISTOR_DIN_PIN.value,
            Constants.PHOTOTRANSISTOR_CS_PIN.value,
        )
        self.__logger = logger.Logger()
        self.__main_switch = switch.Switch(Constants.MAIN_SWITCH_PIN.value)
        if Constants.OBJECT_DETECTION_ENABLED.value:
            self.__detect = detect.Detect(Constants.OBJECT_DETECTION_MODEL.value)

        if not Constants.ISOLATED.value:
            self.__protocol = protocol.Protocol(self.__logger)
            self.__protocol.login()
            self.__logger.set_protocol(self.__protocol)

        GPIO.add_event_detect(
            self.__main_switch.get_pin(),
            GPIO.RISING,
            callback=self.switch_main,
            bouncetime=Constants.MAIN_SWITCH_DEBOUNCE_MS.value
        )

        time_start = datetime.datetime.now()
        if not Constants.ISOLATED.value:
            self.__protocol.heartbeat()
            last_heartbeat = datetime.datetime.now()

        try:
            while True:
                if self.__running:
                    gate_reading = self.__phototransistor.get_reading(1)
                    if gate_reading < Constants.LIGHT_GATE_VALUE.value:
                        if Constants.ISOLATED.value or self.__protocol.can_pickup():
                            self.__color_led.on()
                            time.sleep(Constants.GATE_TO_COLOR_INTERVAL_S.value)
                            color_reading = self.__phototransistor.get_reading(0)
                            color = self.__phototransistor.get_color(color_reading)
                            self.__color_led.off()

                            no_error = False
                            if self.__detect is not None:
                                detected = self.__detect.detect()
                                self.__logger.log("Object detection system detected: " + str(self.__detect.detect()))
                                self.__logger.log("Color detection system detected: " + str(color))
                                if detected == "white":
                                    if color == 1:
                                        self.__sorting_belt.white()
                                        no_error = True
                                    else:
                                        # log and error handling: light sensor and camera detect differ
                                        self.__logger.log("Detection discrepancy between object and color detection.")
                                elif detected == "black":
                                    if color == 0:
                                        self.__sorting_belt.black()
                                        no_error = True
                                    else:
                                        # log and error handling: light sensor and camera detect differ
                                        self.__logger.log("Detection discrepancy between object and color detection.")
                                elif detected == "none":
                                    # log and error handling: no object or wrong color
                                    self.__logger.log("No object has been found.")
                                elif detected == "unknown":
                                    # log and error handling: unknown object
                                    self.__logger.log("The detected object is not a disk.")

                            if no_error:
                                time.sleep(Constants.COLOR_TO_ROBOT_INTERVAL_S.value)
                                self.__robot.arm_push_off()

                                if not Constants.ISOLATED.value:
                                    self.__protocol.picked_up_object()
                                    self.__protocol.determined_object(color)

                        time.sleep(1)  # required sleep after picking up item (especially for protocol)

                    if not Constants.ISOLATED.value and (datetime.datetime.now() - last_heartbeat).seconds >= 3:
                        self.__protocol.heartbeat()
                        last_heartbeat = datetime.datetime.now()

                    if (datetime.datetime.now() - time_start).seconds >= 180:  # possible shutdown requirement
                        break
                time.sleep(Constants.GATE_SENSOR_SENSE_INTERVAL_S.value)
        finally:
            self.shutdown()  # shutdown if the controller exits unexpectedly

    # Callback to run when the main switch is pressed
    def switch_main(self, channel):
        if not self.__running:
            self.startup()
            time.sleep(0.1)  # wait for gate light to turn on
            self.__running = True
        else:
            self.shutdown()
            self.__running = False

    # Method to run when a motor behaves unexpectedly
    def motor_panic(self, pin):
        self.__logger.log("Motor on pin " + str(pin) + " is behaving unexpectedly! Disabling functionality...")
        self.standby()

    # Start functionality
    def startup(self):
        self.__gate_led.on()
        self.__color_led.off()
        self.__robot.arm_move_back()
        self.__main_belt.forward(Constants.MAIN_BELT_MOTOR_POWER.value)
        self.__sorting_belt.white()

    # Stop functionality
    def standby(self):
        self.__running = False
        self.__gate_led.off()
        self.__color_led.off()
        self.__robot.arm_move_back()
        self.__sorting_belt.stop()

    # Turn everything off
    def shutdown(self):
        self.standby()
        self.__robot.arm_back(0)
        self.__main_belt.stop()
