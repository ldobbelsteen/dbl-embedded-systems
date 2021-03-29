# Contains belt (for main belt), and this file contains SortingBelt (inherits belt).
import motor
from constants import Constants


# Main belt where all disks come through
class Belt:
    _motor: motor.Motor = None

    def __init__(self, mtr: motor.Motor):
        self._motor = mtr

    def forward(self, power: int):
        # change(true = forward & false = backward, power = quantity of speed)
        self._motor.change(True, power)

    def backward(self, power: int):
        self._motor.change(False, power)

    def stop(self):
        self._motor.stop()


# The belt that is used to sort (after being picked from the main belt)
# inherits Belt
class SortingBelt(Belt):
    def white(self):
        super().forward(Constants.SORTING_BELT_MOTOR_POWER.value)

    def black(self):
        super().backward(Constants.SORTING_BELT_MOTOR_POWER.value)
