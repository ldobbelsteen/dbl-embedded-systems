import RPi.GPIO as GPIO
import controller

if __name__ == '__main__':
    try:
        GPIO.setmode(GPIO.BCM)
        controller.Controller().start()
    finally:
        GPIO.cleanup()
