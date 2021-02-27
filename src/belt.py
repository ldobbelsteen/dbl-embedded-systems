import motor


class Belt:
    _motor = None

    def __init__(self):
        self._motor = motor.Motor(1, 1, 1)

    def forward(self, power: int):
        self._motor.change(True, power)

    def backward(self, power: int):
        self._motor.change(False, power)


class SortingBelt(Belt):
    def white(self):
        super().forward(80)

    def black(self):
        super().backward(80)
