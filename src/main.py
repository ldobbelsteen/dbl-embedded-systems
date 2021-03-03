import RPi.GPIO as GPIO
import belt
import motor
import phototransistor
import led
import time
import switch

def main():

    motor1 = motor.Motor(16, 20, 21)
    motor2 = motor.Motor(9, 11, 10)
    switch1 = switch.Switch(13)
    switch2 = switch.Switch(19)
    led1 = led.Led(26)
    photo1 = phototransistor.Phototransistor(14, 15, 18, 23)

    # Test sorting belt
    belt1 = belt.SortingBelt(motor1)
    belt1.white()
    time.sleep(1)
    belt1.black()
    time.sleep(1)
    belt1.stop()

    # Test arm
    motor2.change(True, 80)
    while True:
        if switch1.pressed():
            motor2.change(False, 80)
            while True:
                if switch2.pressed():
                    motor2.stop()
                    break
                time.sleep(0.01)
            break
        time.sleep(0.01)

    # Test phototransistor
    led1.on()
    time.sleep(0.5)
    reading = photo1.get_reading(0)
    color = photo1.get_color(reading)
    print(reading, color)
    time.sleep(0.5)
    led1.off()

if __name__ == '__main__':
    try:
        main()
    finally:
        GPIO.cleanup()
