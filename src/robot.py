import time
import motor
from constants import Constants


class Robot:
    __motor: motor.Motor = None
    __switch_arrival = None
    __switch_start = None

    def __init__(self, mtr: motor.Motor):
        self.__motor = mtr

    def arm_push_off(self):
        self.__motor.change(True, Constants.ROBOT_MOTOR_POWER)
        while True:
            if self.arm_arrived():
                break
            time.sleep(0.01)
        self.__motor.stop()

    def arm_move_back(self):
        self.__motor.change(False, Constants.ROBOT_MOTOR_POWER)
        while True:
            if self.arm_arrived():
                break
            time.sleep(0.01)
        self.__motor.stop()

    def arm_arrived(self):
        pass

    def arm_back(self):
        pass
