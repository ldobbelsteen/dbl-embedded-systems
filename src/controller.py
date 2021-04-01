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
                # Constants.ROBOT_MOTOR_VIBRATION_PIN.value,
                # self.motor_panic,
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

        if Constants.OBJECT_DETECTION_ENABLE.value:
            self.__detect = detect.Detect(
                Constants.OBJECT_DETECTION_MODEL.value)

        if Constants.USE_API.value:
            self.__protocol = protocol.Protocol(self.__logger)
            self.__logger.set_protocol(self.__protocol)

        GPIO.add_event_detect(
            self.__main_switch.get_pin(),
            GPIO.RISING,
            callback=self.switch_main,
            bouncetime=Constants.MAIN_SWITCH_DEBOUNCE_MS.value
        )

        self.__logger.log("Controller class initialized.", ["Controller"])

        try:
            self.run()
        finally:
            self.shutdown()  # shutdown if the main loop exits unexpectedly

    # Main logic loop
    def run(self):
        time_start = datetime.datetime.now()
        while True:
            if self.__running:
                gate_light_value = self.__phototransistor.get_reading(7)
                gate_is_blocked = gate_light_value <= Constants.LIGHT_GATE_VALUE.value
                if gate_is_blocked:
                    self.__logger.log(
                        "An object has been detected.", ["Robot"])
                    can_pickup = self.__protocol is None or self.__protocol.can_pickup()
                    if can_pickup:
                        self.__logger.log(
                            "Permission to pickup object has been received.", ["Protocol"])

                        # Determine the object's color
                        self.__color_led.on()
                        time.sleep(Constants.GATE_TO_COLOR_INTERVAL_S.value)
                        color_reading = self.__phototransistor.get_reading(6)
                        color = self.__phototransistor.get_color(color_reading)
                        self.__color_led.off()

                        self.__logger.log(
                            "Color has been determined.", ["Robot"])

                        # Determine the object's class
                        if self.__detect is not None:
                            detected = self.__detect.detect()
                        else:
                            if color == 1:
                                detected = "white"
                            if color == 0:
                                detected = "black"
                            if color == -1:
                                detected = "unknown"

                        self.__logger.log(
                            "Object has been determined.", ["Robot"])

                        # Compare color to class and deal with the result accordingly
                        no_error = False
                        if detected == "white":
                            if color == 1:
                                self.__sorting_belt.white()
                                no_error = True
                                self.__logger.log(
                                    "Object has been confirmed as white disk.", ["Robot"])
                            else:
                                # log and error handling: light sensor and camera detect differ
                                self.__logger.log(
                                    "Detection discrepancy between object and color detection!", ["Fault"])
                        elif detected == "black":
                            if color == 0:
                                self.__sorting_belt.black()
                                no_error = True
                                self.__logger.log(
                                    "Object has been confirmed as black disk.", ["Robot"])
                            else:
                                # log and error handling: light sensor and camera detect differ
                                self.__logger.log(
                                    "Detection discrepancy between object and color detection!", ["Fault"])
                        elif detected == "none":
                            # log and error handling: no object or wrong color
                            self.__logger.log(
                                "No object could be found or it has the wrong color!", ["Fault"])
                        elif detected == "unknown":
                            # log and error handling: unknown object
                            self.__logger.log(
                                "The detected object is probably not a disk!", ["Fault"])

                        # If no exception was found, push the disk off the belt
                        if no_error:
                            time.sleep(
                                Constants.COLOR_TO_ROBOT_INTERVAL_S.value)
                            self.__robot.arm_push_off()
                            self.__logger.log(
                                "Disk is being pushed off.", ["Robot"])

                            if self.__protocol is not None:
                                self.__protocol.picked_up(color)

            # Possible shutdown requirement
            if (datetime.datetime.now() - time_start).seconds >= Constants.ROBOT_RUNNING_S.value:
                self.__logger.log("Robot has reached running time limit of " + str(Constants.ROBOT_RUNNING_S.value)
                                  + " seconds and will shutdown now.", ["System"])
                break

            # Wait before sensing the gate again
            time.sleep(Constants.GATE_SENSOR_SENSE_INTERVAL_S.value)

    # Callback to run when the main switch is pressed
    def switch_main(self, channel):
        if not self.__running:
            self.__logger.log("Starting up system...", ["System"])
            self.startup()
            self.__logger.log("System is started up.", ["System"])
        else:
            self.__logger.log("Shutdown system...", ["System"])
            self.shutdown()
            self.__logger.log("System has shutdown.", ["System"])

    # Method to run when a motor behaves unexpectedly
    def motor_panic(self, pin):
        self.__logger.log("Motor on pin " + str(pin) +
                          " is behaving unexpectedly!", ["Fault"])
        self.__logger.log("System going in standby mode...", ["System"])
        self.standby()
        self.__logger.log("System is in standby mode.", ["System"])
        self.__logger.log("For recovery: fix the motor on pin " +
                          str(pin) + " and press the main switch.", ["Fault recovery"])

    # Start functionality
    def startup(self):
        self.__gate_led.on()
        self.__color_led.off()
        self.__robot.arm_move_back()
        self.__main_belt.forward(Constants.MAIN_BELT_MOTOR_POWER.value)
        self.__sorting_belt.white()
        time.sleep(0.1)  # wait for gate light to turn on
        self.__running = True

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
