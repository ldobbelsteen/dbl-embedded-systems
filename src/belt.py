import motor
from constants import Constants


class Belt:
    _motor = None

    def __init__(self, mtr: motor.Motor):
        self._motor = mtr

    def forward(self, power: int):
        self._motor.change(True, power)

    def backward(self, power: int):
        self._motor.change(False, power)


class SortingBelt(Belt):
    def white(self):
        super().forward(Constants.SORTING_BELT_POWER)

    def black(self):
        super().backward(Constants.SORTING_BELT_POWER)
