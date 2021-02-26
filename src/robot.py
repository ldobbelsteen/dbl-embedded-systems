import RPi.GPIO as GPIO


class Robot:
    def __init__(self):
        pass

    def disable(self):
        GPIO.cleanup()
