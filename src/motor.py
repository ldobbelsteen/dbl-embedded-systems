from typing import Callable
import RPi.GPIO as GPIO
from time import sleep
from constants import Constants


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
                    GPIO.BOTH,
                    callback=self.vib_state_changed,
                    bouncetime=Constants.VIB_SENSOR_DEBOUNCE.value)

            self.__pwm = GPIO.PWM(self.__enable_pin, 100)

    # Handle change in the state of a vibration sensor
    def vib_state_changed(self, channel):
        state = GPIO.input(self.__vib_sens_pin) == GPIO.LOW

        # During the sensor's debounce time, check if its state changes a few times.
        # If it does change, the state is unstable and the callback is rejected
        check_count = 10
        for _ in range(check_count):
            sleep(Constants.VIB_SENSOR_DEBOUNCE_MS.value / check_count)
            if state != GPIO.input(self.__vib_sens_pin) == GPIO.LOW:
                return

        # If the state is stable, check if it coincides with the expected state.
        # If it doesn't, run the panic function.
        if state != self.__moving:
            self.__panic_func()

    def change(self, forward: bool, power: int):
        if self.__loaded:
            power = self.__power_check(power)
            self.stop()
            GPIO.output(self.__forward_pin, forward)
            GPIO.output(self.__backward_pin, not forward)
            self.__start(power)

    def __start(self, power):
        if self.__loaded:
            self.__pwm.start(power)
            self.__running = True

    def stop(self):
        if self.__loaded:
            self.__pwm.stop()
            self.__running = False

    # robustness checking if the power is a valid value between 0 and 100.
    # why return only 0 and only 100?
    @staticmethod
    def __power_check(power: int):
        if power < 0:
            return 0
        elif power > 100:
            return 100
        return power

    @staticmethod
    def print_panic(pin: int):
        print("Motor on pin " + str(pin) + " is behaving unexpectedly!")
