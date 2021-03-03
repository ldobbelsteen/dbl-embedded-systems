import RPi.GPIO as GPIO
import motor
import switch
from constants import Constants


class Robot:
    __motor: motor.Motor = None
    __switch_arrival: switch.Switch = None
    __switch_start: switch.Switch = None

    def __init__(self, mtr: motor.Motor):
        self.__motor = mtr

    def arm_push_off(self):
        self.__motor.change(True, Constants.ROBOT_MOTOR_POWER.value)
        GPIO.add_event_detect(self.__switch_arrival.get_pin(), GPIO.RISING, callback=self.arm_arrived())

    def arm_move_back(self):
        self.__motor.change(False, Constants.ROBOT_MOTOR_POWER.value)
        GPIO.add_event_detect(self.__switch_start.get_pin(), GPIO.RISING, callback=self.arm_back())

    def arm_arrived(self):
        self.__motor.stop()
        self.arm_move_back()

    def arm_back(self):
        self.__motor.stop()
