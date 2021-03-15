import RPi.GPIO as GPIO
import controller

if __name__ == '__main__':
    try:
        controller.Controller().run()
    finally:
        GPIO.cleanup()
