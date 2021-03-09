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
import switch


class Controller:
    __robot: robot.Robot = None
    __sorting_belt: belt.SortingBelt = None
    __phototransistor: phototransistor.Phototransistor = None
    __led: led.Led = None
    __protocol: protocol.Protocol = None

    def __init__(self):
        self.__robot = robot.Robot(motor.Motor(Constants.R_F_PIN.value, Constants.R_B_PIN.value, Constants.R_E_PIN.value),
                                   switch.Switch(Constants.S_A_PIN), switch.Switch(Constants.S_S_PIN))
        self.__sorting_belt = belt.SortingBelt(motor.Motor(Constants.SB_F_PIN.value, Constants.SB_B_PIN.value,
                                                           Constants.SB_E_PIN.value))
        self.__phototransistor = phototransistor.Phototransistor(Constants.PH_CLK_PIN.value, Constants.PH_DOUT_PIN.value,
                                                                 Constants.PH_DIN_PIN.value, Constants.PH_CS_PIN.value)
        self.__led = led.Led(Constants.LED_PIN.value)
        if not Constants.ISOLATED.value:
            self.__protocol = protocol.Protocol()

        self.__led.on()
        self.run()

    def run(self):
        time_start = datetime.datetime.now()
        if not Constants.ISOLATED.value:
            self.__protocol.heartbeat()
            last_heartbeat = datetime.datetime.now()

        while True:
            color = self.__phototransistor.get_color(self.__phototransistor.get_reading(0))
            if color != -1:
                if not Constants.ISOLATED.value and not self.__protocol.can_pickup():
                    time.sleep(1)
                else:
                    self.__robot.arm_push_off()
                    if color == 0:
                        self.__sorting_belt.black()
                    elif color == 1:
                        self.__sorting_belt.white()

                    if not Constants.ISOLATED.value:
                        self.__protocol.picked_up_object()
                        self.__protocol.determined_object(color)
                    time.sleep(1)
            else:
                time.sleep(0.05)

            if not Constants.ISOLATED.value and (datetime.datetime.now() - last_heartbeat).seconds >= 3:
                self.__protocol.heartbeat()
                last_heartbeat = datetime.datetime.now()

            if (datetime.datetime.now() - time_start).seconds >= 180:  # possible shutdown requirement
                break
        self.shutdown()

    def shutdown(self):
        self.__robot.arm_move_back()
        self.__led.off()
        self.__sorting_belt.stop()
        GPIO.cleanup()
