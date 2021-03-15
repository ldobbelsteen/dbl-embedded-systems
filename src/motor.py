import RPi.GPIO as GPIO
from time import sleep


class Motor:
    __forward_pin: int = -1
    __backward_pin: int = -1
    __enable_pin: int = -1
    __pwm: GPIO.PWM = None
    __loaded: bool = False

    def __init__(self, forward_pin: int = -1, backward_pin: int = -1, enable_pin: int = -1):
        self.__loaded = (forward_pin > -1 and backward_pin > -1 and enable_pin > -1)
        if self.__loaded:
            self.__forward_pin = forward_pin
            self.__backward_pin = backward_pin
            self.__enable_pin = enable_pin

            GPIO.setup(self.__forward_pin, GPIO.OUT)
            GPIO.setup(self.__backward_pin, GPIO.OUT)
            GPIO.setup(self.__enable_pin, GPIO.OUT)

            self.__pwm = GPIO.PWM(self.__enable_pin, 100)

    def change(self, forward: bool, power: int):
        if self.__loaded:
            power = self.__power_check(power)
            self.stop()
            GPIO.output(self.__forward_pin, forward)
            GPIO.output(self.__backward_pin, not forward)
            self.__start(power)

    # change the motor with duration
    def change_w_dur(self, forward: bool, power: int, duration: int):
        if self.__loaded:
            self.change(forward, power)
            sleep(duration)
            self.stop()

    def __start(self, power):
        if self.__loaded:
            self.__pwm.start(power)

    def stop(self):
        if self.__loaded:
            self.__pwm.stop()

    # robustness checking if the power is a valid value between 0 and 100.
    # why return only 0 and only 100?
    @staticmethod
    def __power_check(power: int):
        if power < 0:
            return 0
        elif power > 100:
            return 100
        return power
