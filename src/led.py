import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)


class Led:
    __led_pin = -1
    __loaded = False

    def __init__(self, led_pin: int = -1):
        self.__loaded = led_pin > -1
        self.__led_pin = led_pin
        if self.__loaded:
            GPIO.setup(led_pin, GPIO.OUT)

    def on(self):
        if self.__loaded:
            GPIO.output(self.__led_pin, 1)

    def off(self):
        if self.__loaded:
            GPIO.output(self.__led_pin, 0)
