import RPi.GPIO as GPIO


class Switch:
    __input_pin: int = -1

    def __init__(self, input_pin: int = -1):
        self.__loaded = input_pin > -1
        if self.__loaded:
            self.__input_pin = input_pin
            GPIO.setup(self.__input_pin, GPIO.IN)

    # Returns whether switch is pressed
    def pressed(self):
        if self.__loaded:
            return GPIO.input(self.__input_pin) == GPIO.HIGH
        return None

    def get_pin(self):
        if self.__loaded:
            return self.__input_pin
        return -1
