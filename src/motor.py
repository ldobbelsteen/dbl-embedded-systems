from constants import Constants
from threading import Timer
from typing import Callable
import RPi.GPIO as GPIO
import time

def print_panic(pin: int):
    print("Motor on pin " + str(pin) + " is behaving unexpectedly!")


class Motor:
    __forward_pin: int = -1
    __backward_pin: int = -1
    __enable_pin: int = -1
    __vib_sens_pin: int = -1
    __pwm: GPIO.PWM = None
    __loaded: bool = False
    __moving: bool = False
    __controller = None
    __panic_func: Callable = None
    __running: bool = False

    def __init__(
            self,
            forward_pin: int = -1,
            backward_pin: int = -1,
            enable_pin: int = -1,
            vib_sens_pin: int = -1,
            panic_func: Callable = print_panic,
    ):
        self.__running = False
        self.__loaded = (forward_pin > -1 and backward_pin > -1 and enable_pin > -1)
        if self.__loaded:
            self.__forward_pin = forward_pin
            self.__backward_pin = backward_pin
            self.__enable_pin = enable_pin
            self.__vib_sens_pin = vib_sens_pin
            self.__panic_func = panic_func

            GPIO.setup(self.__forward_pin, GPIO.OUT)
            GPIO.setup(self.__backward_pin, GPIO.OUT)
            GPIO.setup(self.__enable_pin, GPIO.OUT)

            # If vibration sensor is passed, detect changes in its state
            if self.__vib_sens_pin > -1:
                GPIO.setup(self.__vib_sens_pin, GPIO.IN)
                GPIO.add_event_detect(
                    self.__vib_sens_pin,
                    GPIO.FALLING,
                    callback=self.vib_fall,
                    bouncetime=Constants.VIB_SENSOR_DEBOUNCE_MS.value)

            self.__pwm = GPIO.PWM(self.__enable_pin, 100)

    # If the vibration sensor falls, check a few times if it is still low
    # (meaning it is stably so). Then if it's low and the motor is supposed
    # to be running, run the panic function.
    def vib_fall(self, channel):
        risen = False
        count = Constants.VIB_SENSOR_CHECK_COUNT.value
        total = Constants.VIB_SENSOR_DEBOUNCE_MS.value / 1000
        chunk = total / count
        def check_risen():
            if GPIO.input(self.__vib_sens_pin) == GPIO.HIGH:
                risen = True
        def check_stable():
            if not risen:
                if self.__running:
                    self.__panic_func(channel)
        for i in range(count):
            if i < count - 1:
                Timer(i * chunk, check_risen).start()
            else:
                Timer(i * chunk, check_stable).start()
        
    def change(self, forward: bool, power: int):
        if self.__loaded:
            power = self.__power_check(power)
            self.stop()
            GPIO.output(self.__forward_pin, forward)
            GPIO.output(self.__backward_pin, not forward)
            self.__start(power)

    def __start(self, power):
        if self.__loaded:
            self.__running = True
            self.__pwm.start(power)

    def stop(self):
        if self.__loaded:
            self.__running = False
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
