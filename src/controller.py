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

    def __init__(self):
        self.__running = False
        self.__gate_led = led.Led(Constants.LED_G_PIN.value)
        self.__color_led = led.Led(Constants.LED_C_PIN.value)
        self.__robot = robot.Robot(
            motor.Motor(
                Constants.R_F_PIN.value,
                Constants.R_B_PIN.value,
                Constants.R_E_PIN.value,
            ),
            switch.Switch(Constants.S_S_PIN.value),
            switch.Switch(Constants.S_A_PIN.value),
        )
        self.__sorting_belt = belt.SortingBelt(
            motor.Motor(
                Constants.SB_F_PIN.value,
                Constants.SB_B_PIN.value,
                Constants.SB_E_PIN.value,
                Constants.M_2_V_PIN.value,
                self.motor_panic,
            )
        )
        self.__main_belt = belt.Belt(
            motor.Motor(
                Constants.MB_F_PIN.value,
                Constants.MB_B_PIN.value,
                Constants.MB_E_PIN.value,
            )
        )
        self.__phototransistor = phototransistor.Phototransistor(
            Constants.PH_CLK_PIN.value,
            Constants.PH_DOUT_PIN.value,
            Constants.PH_DIN_PIN.value,
            Constants.PH_CS_PIN.value,
        )
        self.__logger = logger.Logger()
        self.__main_switch = switch.Switch(Constants.MAIN_SWITCH_PIN.value)

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
                            if color == 1:
                                self.__sorting_belt.white()
                            elif color == 0:
                                self.__sorting_belt.black()
                            else:
                                continue  # log and error handling: disk has wrong color
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
        self.__main_belt.forward(Constants.MAIN_BELT_POWER.value)
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
        self.__main_belt.stop()
