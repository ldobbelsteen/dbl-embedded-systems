import RPi.GPIO as GPIO
import motor
import phototransistor
import led
import time

def main():

    # Test first motor
    motor1 = motor.Motor(16, 20, 21)
    motor1.change_w_dur(True, 70, 1)
    motor1.change_w_dur(False, 80, 1)

    # Test second motor
    motor2 = motor.Motor(9, 11, 10)
    motor2.change_w_dur(True, 90, 1)
    motor2.change_w_dur(False, 60, 1)

    # Test running both motors simultaneously
    motor1.change(False, 80)
    motor2.change(True, 100)
    time.sleep(1)
    motor1.stop()
    motor2.stop()

    # Test controlling light
    led1 = led.Led(26)
    led1.on()
    time.sleep(1)
    led1.off()

    # Test phototransistor
    photo = phototransistor.Phototransistor(14, 15, 18, 23)
    while True:
        reading = photo.get_reading(0)
        color = photo.get_color(reading)
        print(reading, color)
        time.sleep(0.3)

if __name__ == '__main__':
    try:
        main()
    finally:
        GPIO.cleanup()
