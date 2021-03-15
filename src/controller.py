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
        self.__robot = robot.Robot(motor.Motor(Constants.R_F_PIN.value, Constants.R_B_PIN.value, Constants.R_E_PIN.value),
                                   switch.Switch(Constants.S_S_PIN.value), switch.Switch(Constants.S_A_PIN.value))
        self.__sorting_belt = belt.SortingBelt(motor.Motor(Constants.SB_F_PIN.value, Constants.SB_B_PIN.value,
                                                           Constants.SB_E_PIN.value))
        self.__main_belt = belt.Belt(motor.Motor(Constants.MB_F_PIN.value, Constants.MB_B_PIN.value,
                                                 Constants.MB_E_PIN.value))
        self.__phototransistor = phototransistor.Phototransistor(Constants.PH_CLK_PIN.value, Constants.PH_DOUT_PIN.value,
                                                                 Constants.PH_DIN_PIN.value, Constants.PH_CS_PIN.value)
        self.__gate_led = led.Led(Constants.LED_G_PIN.value)
        self.__color_led = led.Led(Constants.LED_C_PIN.value)
        self.__main_switch = switch.Switch(Constants.MAIN_SWITCH_PIN.value)
        GPIO.add_event_detect(self.__main_switch.get_pin(), GPIO.RISING, callback=self.switch_main, bouncetime=200)
        self.__logger = logger.Logger()
        if not Constants.ISOLATED.value:
            self.__protocol = protocol.Protocol(self.__logger)
            self.__protocol.login()
            self.__logger.set_protocol(self.__protocol)

        for i in Constants.VIB_SENSORS_PINS.value:
            GPIO.setup(i, GPIO.IN)
            GPIO.add_event_detect(i, GPIO.RISING, callback=self.motor_disabled, bouncetime=500)

        self.run()

    def run(self):
        time_start = datetime.datetime.now()
        if not Constants.ISOLATED.value:
            self.__protocol.heartbeat()
            last_heartbeat = datetime.datetime.now()

        while not self.__running:
            time.sleep(0.05)
        self.__main_belt.forward(Constants.MAIN_BELT_POWER.value)
        self.__gate_led.on()
        self.__color_led.off()
        try:
            while True:
                if self.__running:
                    gate_reading = self.__phototransistor.get_reading(1)
                    if gate_reading < Constants.LIGHT_GATE_VALUE.value:
                        if Constants.ISOLATED.value or self.__protocol.can_pickup():
                            self.__color_led.on()
                            time.sleep(0.2)
                            color_reading = self.__phototransistor.get_reading(0)
                            color = self.__phototransistor.get_color(color_reading)
                            self.__color_led.off()
                            if color == 1:
                                self.__sorting_belt.white()
                            elif color == 0:
                                self.__sorting_belt.black()
                            else:
                                continue  # log and error handling: disk has wrong color
                            time.sleep(0.4)
                            self.__robot.arm_push_off()

                            if not Constants.ISOLATED.value:
                                self.__protocol.picked_up_object()
                                self.__protocol.determined_object(color)

                        time.sleep(1)

                    time.sleep(0.05)

                    if not Constants.ISOLATED.value and (datetime.datetime.now() - last_heartbeat).seconds >= 3:
                        self.__protocol.heartbeat()
                        last_heartbeat = datetime.datetime.now()

                    if (datetime.datetime.now() - time_start).seconds >= 180:  # possible shutdown requirement
                        break
                else:
                    time.sleep(0.05)
        finally:
            self.shutdown()

    def motor_disabled(self, channel):
        time.sleep(0.5)
        if GPIO.input(channel) == GPIO.HIGH:
            self.__logger.log("Motor " + str(channel) + " has been disabled.")
            self.__running = False

    def switch_main(self):
        self.__running = not self.__running

    def shutdown(self):
        self.__gate_led.off()
        self.__color_led.off()
        self.__robot.arm_move_back()
        self.__sorting_belt.stop()
        self.__main_belt.stop()
