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


class Controller:
    __robot: robot.Robot = None
    __sorting_belt: belt.SortingBelt = None
    __phototransistor: phototransistor.Phototransistor = None
    __led: led.Led = None
    __protocol: protocol.Protocol = None
    __protocol_enabled: bool

    def __init__(self, protocol_enabled: bool):
        self.__robot = robot.Robot(motor.Motor(Constants.R_F_PIN, Constants.R_B_PIN, Constants.R_E_PIN))
        self.__sorting_belt = belt.SortingBelt(motor.Motor(Constants.SB_F_PIN, Constants.SB_B_PIN, Constants.SB_E_PIN))
        self.__phototransistor = phototransistor.Phototransistor(Constants.PH_CLK_PIN, Constants.PH_DOUT_PIN,
                                                                 Constants.PH_DIN_PIN, Constants.PH_CS_PIN)
        self.__led = led.Led(Constants.LED_PIN)
        self.__protocol_enabled = protocol_enabled
        if protocol_enabled:
            self.__protocol = protocol.Protocol()

        self.__led.on()
        self.system()

    def system(self):
        if self.__protocol_enabled:
            self.__protocol.heartbeat()
            last_heartbeat = datetime.datetime.now()

        while True:
            color = self.__phototransistor.get_color(self.__phototransistor.get_reading(0))
            if color != -1:
                if self.__protocol_enabled and not self.__protocol.can_pickup():
                    time.sleep(1)
                else:
                    self.__robot.arm_push_off()
                    if color == 0:
                        self.__sorting_belt.black()
                    elif color == 1:
                        self.__sorting_belt.white()

                    if self.__protocol_enabled:
                        self.__protocol.picked_up_object()
                        self.__protocol.determined_object(color)
                    time.sleep(0.05)
            else:
                time.sleep(0.05)

            if self.__protocol_enabled and (datetime.datetime.now() - last_heartbeat).seconds >= 3:
                self.__protocol.heartbeat()
                last_heartbeat = datetime.datetime.now()

            if 1 != 1:  # possible shutdown requirement
                break
        self.shutdown()

    def shutdown(self):
        self.__robot.arm_move_back()
        self.__led.off()
        self.__sorting_belt.stop()
        GPIO.cleanup()
