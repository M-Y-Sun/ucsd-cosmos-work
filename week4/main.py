import sys

if __name__ != "__main__":
    sys.stderr.write("file must be ran as a script")
    sys.exit()

import RPi.GPIO as GPIO
from evdev import InputDevice, categorize

from include.gpspecs import *

GPIO_BS1 = 5
GPIO_BS2 = 6
GPIO_BS_PWM = 13
GPIO_S1_1 = 17
GPIO_S1_PWM = 22
GPIO_S1_2 = 27
GPIO_S2_1 = 16
GPIO_S2_2 = 20
GPIO_S2_PWM = 21

GPIO.setmode(GPIO.BCM)

GPIO.setup(GPIO_BS1, GPIO.OUT)
GPIO.setup(GPIO_BS2, GPIO.OUT)
GPIO.setup(GPIO_BS_PWM, GPIO.OUT)
GPIO.setup(GPIO_S1_1, GPIO.OUT)
GPIO.setup(GPIO_S1_2, GPIO.OUT)
GPIO.setup(GPIO_S1_PWM, GPIO.OUT)
GPIO.setup(GPIO_S2_1, GPIO.OUT)
GPIO.setup(GPIO_S2_2, GPIO.OUT)
GPIO.setup(GPIO_S2_PWM, GPIO.OUT)

GPIO.output(GPIO_BS1, False)
GPIO.output(GPIO_BS2, False)
GPIO.output(GPIO_S1_1, False)
GPIO.output(GPIO_S1_2, False)
GPIO.output(GPIO_S2_1, False)
GPIO.output(GPIO_S2_2, False)

FREQ = 50

BS_PWM = GPIO.PWM(GPIO_BS_PWM, FREQ)
S1_PWM = GPIO.PWM(GPIO_S1_PWM, FREQ)
S2_PWM = GPIO.PWM(GPIO_S2_PWM, FREQ)

BS_PWM.start(40)
S1_PWM.start(80)
S2_PWM.start(80)

gamepad = InputDevice("/dev/input/event0")
print(gamepad, "\n")


class GP_comp:
    def __init__(self, pressed, code, val):
        self.pressed = pressed
        self.code = code
        self.val = val


def read_event():
    button = GP_comp(False, -1, -1)
    stick = GP_comp(False, -1, -1)
    for event in gamepad.read():
        info = categorize(event)
        if event.type == 1:
            button.pressed = True
            button.code = info.scancode
            button.val = info.keystate
        elif event.type == 3:
            stick.pressed = True
            stick.code = info.event.code
            stick.val = info.event.value
    return button, stick


try:
    while True:
        button = GP_comp(False, -1, -1)

        try:
            button, _ = read_event()

        # ignore the exception (will throw error with value 11)
        except:
            continue

        if button.pressed and button.val == GP_BUT_P:
            # print("[    \033[32;1mOK\033[0m   ] button pressed")
            # A:  segment 1 up
            # B:  segment 1 down
            # X:  segment 2 up
            # Y:  segment 2 down
            # LB: base left
            # RB: base right

            if button.code == GP_BUT_LB:
                GPIO.output(GPIO_BS1, True)
                GPIO.output(GPIO_BS2, False if button.val == GP_BUT_P else True)
                print("[    \033[32;1mOK\033[0m   ] LB")

            elif button.code == GP_BUT_RB:
                GPIO.output(GPIO_BS1, False if button.val == GP_BUT_P else True)
                GPIO.output(GPIO_BS2, True)
                print("[    \033[32;1mOK\033[0m   ] RB")

            elif button.code == GP_BUT_A:
                GPIO.output(GPIO_S1_1, False if button.val == GP_BUT_P else True)
                GPIO.output(GPIO_S1_2, True)
                print("[    \033[32;1mOK\033[0m   ] A")

            elif button.code == GP_BUT_B:
                GPIO.output(GPIO_S1_1, True)
                GPIO.output(GPIO_S1_2, False if button.val == GP_BUT_P else True)
                print("[    \033[32;1mOK\033[0m   ] B")

            elif button.code == GP_BUT_X:
                GPIO.output(GPIO_S2_1, False if button.val == GP_BUT_P else True)
                GPIO.output(GPIO_S2_2, True)
                print("[    \033[32;1mOK\033[0m   ] X")

            elif button.code == GP_BUT_Y:
                GPIO.output(GPIO_S2_1, True)
                GPIO.output(GPIO_S2_2, False if button.val == GP_BUT_P else True)
                print("[    \033[32;1mOK\033[0m   ] Y")


except KeyboardInterrupt:
    BS_PWM.stop()
    S1_PWM.stop()
    S2_PWM.stop()
    gamepad.close()
