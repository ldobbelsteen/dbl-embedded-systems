import RPi.GPIO as GPIO
import motor
import phototransistor
import led
import time

if __name__ == '__main__':

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

    # Clean GPIO channels
    GPIO.cleanup()

    # Test phototransistor
    photo = phototransistor.Phototransistor(14, 15, 18, 23)
    # while True:
    #     channel = 0
    #     light = photo.get_reading(channel)
    #     percentage = round(light * 100, 1)
    #     print(str(percentage) + "%")
    #     time.sleep(0.5)

    reading = photo.get_reading(5)
    color = photo.get_color(reading)
