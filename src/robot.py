import time
import motor
import switch
import RPi.GPIO as GPIO
from constants import Constants


class Robot:
    __motor: motor.Motor = None
    __switch_arrival: switch.Switch = None
    __switch_start: switch.Switch = None

    def __init__(self, mtr: motor.Motor, s_arrival: switch.Switch, s_start: switch.Switch):
        self.__motor = mtr
        self.__switch_arrival = s_arrival
        self.__switch_start = s_start
        GPIO.add_event_detect(self.__switch_arrival.get_pin(), GPIO.RISING, callback=self.arm_arrived)
        GPIO.add_event_detect(self.__switch_start.get_pin(), GPIO.RISING, callback=self.arm_back)
        if not self.__switch_start.pressed():
            self.arm_move_back()
            time.sleep(2)

    def arm_push_off(self):
        self.__motor.change(True, Constants.ROBOT_MOTOR_POWER.value)
        
    def arm_move_back(self):
        self.__motor.change(False, Constants.ROBOT_MOTOR_POWER.value)

    def arm_arrived(self, channel):
        self.__motor.stop()
        self.arm_move_back()

    def arm_back(self, channel):
        self.__motor.stop()
