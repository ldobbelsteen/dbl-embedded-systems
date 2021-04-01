# Class Led, contains Led light initialization + on + off commands.
import RPi.GPIO as GPIO


class Led:
    __led_pin: int = -1
    __loaded: bool = False

    def __init__(self, led_pin: int = -1):
        # check if given pin is not negative
        self.__loaded = led_pin > -1
        self.__led_pin = led_pin
        if self.__loaded:
            GPIO.setup(led_pin, GPIO.OUT)

    # Puts the led on
    def on(self):
        if self.__loaded:
            GPIO.output(self.__led_pin, 1)

    # Puts the led off
    def off(self):
        if self.__loaded:
            GPIO.output(self.__led_pin, 0)
