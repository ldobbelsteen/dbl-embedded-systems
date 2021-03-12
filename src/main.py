import belt
import led
import time
import motor
import robot
import switch
import phototransistor
import RPi.GPIO as GPIO
from constants import Constants

def main():

    main_belt = belt.Belt(motor.Motor(
        Constants.MB_F_PIN.value,
        Constants.MB_B_PIN.value,
        Constants.MB_E_PIN.value,
    ))

    sorting_belt = belt.SortingBelt(motor.Motor(
        Constants.SB_F_PIN.value,
        Constants.SB_B_PIN.value,
        Constants.SB_E_PIN.value,
    ))

    main_robot = robot.Robot(
        motor.Motor(
            Constants.R_F_PIN.value,
            Constants.R_B_PIN.value,
            Constants.R_E_PIN.value,
        ),
        switch.Switch(Constants.S_S_PIN.value),
        switch.Switch(Constants.S_A_PIN.value),
    )

    photo = phototransistor.Phototransistor(
        Constants.PH_CLK_PIN.value,
        Constants.PH_DOUT_PIN.value,
        Constants.PH_DIN_PIN.value,
        Constants.PH_CS_PIN.value,
    )

    gate_light = led.Led(Constants.LED_G_PIN.value)
    color_light = led.Led(Constants.LED_C_PIN.value)

    # Basic controller logic that has been tested and works
    main_belt.forward(Constants.MAIN_BELT_POWER.value)
    gate_light.on()
    color_light.off()
    try:
        while True:
            gate_reading = photo.get_reading(1)
            if gate_reading < Constants.LIGHT_GATE_VALUE.value:
                color_light.on()
                time.sleep(0.2)
                color_reading = photo.get_reading(0)
                color = photo.get_color(color_reading)
                color_light.off()
                if color == 1:
                    sorting_belt.white()
                elif color == 0:
                    sorting_belt.black()
                else:
                    continue
                time.sleep(0.4)
                main_robot.arm_push_off()
                time.sleep(1)
            time.sleep(0.05)
    finally:
        gate_light.off()
        color_light.off()

if __name__ == '__main__':
    try:
        main()
    finally:
        GPIO.cleanup()
