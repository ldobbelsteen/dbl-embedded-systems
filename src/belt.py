# Contains belt (for main belt), and this file contains SortingBelt (inherits belt).
import motor
from constants import Constants


# Main belt where all disks come through
class Belt:
    _motor: motor.Motor = None  # The motor of the belt

    def __init__(self, mtr: motor.Motor):
        self._motor = mtr

    # Puts the motor in forward motion
    def forward(self, power: int):
        # change(true = forward & false = backward, power = quantity of speed)
        self._motor.change(True, power)

    # Puts the motor in backwards motion
    def backward(self, power: int):
        self._motor.change(False, power)

    # Stops the motor of the belt
    def stop(self):
        self._motor.stop()


# The belt that is used to sort (after being picked from the main belt)
# inherits Belt
class SortingBelt(Belt):
    # Puts the motor in motion for a white disk
    def white(self):
        super().forward(Constants.SORTING_BELT_MOTOR_POWER.value)

    # Puts the motor in motion for a black disk
    def black(self):
        super().backward(Constants.SORTING_BELT_MOTOR_POWER.value)
