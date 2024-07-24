import sys

if __name__ != "__main__":
    sys.stderr.write("file must be ran as a script")
    sys.exit()

from adafruit_servokit import ServoKit
from evdev import InputDevice, categorize

import include.drive as drive
from include.gpspecs import *

gamepad = InputDevice("/dev/input/event0")
print("[  \033[37;1mINFO\033[0m  ] ", gamepad, "\n")

CH1 = 8
CH2 = 9
kit = ServoKit(channels=16)
kit.servo[CH1].set_pulse_width_range(400, 2300)
kit.servo[CH2].set_pulse_width_range(400, 2300)


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


# TODO: FINISH
def sv_t1(bcode, angle, chn):
    button = GP_comp(False, -1, -1)
    try:
        button, _ = read_event()
    except:
        pass

    if button.pressed:
        print("[    \033[32;1mOK\033[0m   ] button pressed")
        if button.code == bcode:
            kit.servo[chn].angle = angle
            print(
                "[    \033[32;1mOK\033[0m   ] channel {0} to angle:\t{1}".format(
                    chn, angle
                )
            )


spdfac = 1
init = False
print("Press `Right Bumper' to initialize")

try:
    while True:
        button = GP_comp(False, -1, -1)
        stick = GP_comp(False, -1, -1)

        try:
            button, stick = read_event()

        # ignore the exception (will throw error with value 11)
        except:
            continue

        if button.pressed and button.code == GP_BUT_RB and button.val == GP_BUT_P:
            init = True
            print("[    \033[32;1mOK\033[0m   ] initialize gamepad")

        spd = 100  # 40 * spdfac
        if init:
            if stick.pressed:
                if stick.code == GP_STK_VT:

                    # up
                    if stick.val == GP_STK_UP_P:
                        while True:
                            drive.fw(spd, spd)
                            print("[    \033[32;1mOK\033[0m   ] up pressed")

                            substick = GP_comp(False, -1, -1)
                            subbut = GP_comp(False, -1, -1)
                            while subbut.val == -1 and substick.val != GP_STK_R:
                                try:
                                    subbut, substick = read_event()
                                except:
                                    continue

                            if substick.val == GP_STK_R:
                                print("stopped")
                                drive.stop()
                                break

                            if subbut.val == GP_BUT_P:
                                if subbut.code == GP_BUT_LB:
                                    drive.fw(0, spd)
                                    print(
                                        "[    \033[32;1mOK\033[0m   ] up + LB pressed"
                                    )
                                elif subbut.code == GP_BUT_RB:
                                    drive.fw(spd, 0)
                                    print(
                                        "[    \033[32;1mOK\033[0m   ] up + RB pressed"
                                    )
                                else:
                                    continue

                                while subbut.val != GP_BUT_R:
                                    try:
                                        subbut, _ = read_event()
                                    except:
                                        continue
                                drive.fw(spd, spd)

                    # down
                    elif stick.val == GP_STK_DN_P:
                        while True:
                            drive.fw(-spd, -spd)
                            print("[    \033[32;1mOK\033[0m   ] down pressed")

                            substick = GP_comp(False, -1, -1)
                            subbut = GP_comp(False, -1, -1)
                            while subbut.val == -1 and substick.val != GP_STK_R:
                                try:
                                    subbut, substick = read_event()
                                except:
                                    continue
                            if substick.val == GP_STK_R:
                                drive.stop()
                                break

                            if subbut.val == GP_BUT_P:
                                if subbut.code == GP_BUT_LB:
                                    drive.fw(0, -spd)
                                    print(
                                        "[    \033[32;1mOK\033[0m   ] down + LB pressed"
                                    )
                                elif subbut.code == GP_BUT_RB:
                                    drive.fw(-spd, 0)
                                    print(
                                        "[    \033[32;1mOK\033[0m   ] down + RB pressed"
                                    )
                                else:
                                    continue

                                while subbut.val != GP_BUT_R:
                                    try:
                                        subbut, _ = read_event()
                                    except:
                                        continue
                                drive.fw(-spd, -spd)

                    else:
                        drive.stop()
                        print("[    \033[32;1mOK\033[0m   ] stick released")

            elif button.pressed and button.val == GP_BUT_P:
                print("[    \033[32;1mOK\033[0m   ] button pressed")
                # A:  servo 1 to 0 deg
                # B:  servo 1 to 180 deg
                # X:  servo 2 to 0 deg
                # Y:  servo 2 to 180 deg
                # LB: turn left
                # RB: turn right

                # move left
                if button.code == GP_BUT_LB:
                    while True:
                        drive.fw(int(-spd / 1.3), int(spd / 1.3))
                        print("[    \033[32;1mOK\033[0m   ] LB pressed")

                        subbut = GP_comp(False, -1, -1)
                        substick = GP_comp(False, -1, -1)
                        while substick.val == -1 and subbut.val != GP_BUT_R:
                            try:
                                subbut, substick = read_event()
                            except:
                                continue
                        if subbut.val == GP_BUT_R:
                            drive.stop()
                            break

                        if substick.code == GP_STK_VT:
                            if substick.val == GP_STK_UP_P:
                                drive.fw(0, spd)
                                print("[    \033[32;1mOK\033[0m   ] up + LB pressed")
                            elif substick.val == GP_STK_DN_P:
                                drive.fw(0, -spd)
                                print("[    \033[32;1mOK\033[0m   ] down + LB pressed")
                            else:
                                continue

                            while substick.val != GP_STK_R:
                                try:
                                    _, substick = read_event()
                                except:
                                    continue
                            drive.fw(spd / 1.3, -spd / 1.3)

                # move right
                elif button.code == GP_BUT_RB:
                    while True:
                        drive.fw(spd / 1.3, -spd / 1.3)
                        print("[    \033[32;1mOK\033[0m   ] RB pressed")

                        subbut = GP_comp(False, -1, -1)
                        substick = GP_comp(False, -1, -1)
                        while substick.val == -1 and subbut.val != GP_BUT_R:
                            try:
                                subbut, substick = read_event()
                            except:
                                continue
                        if subbut.val == GP_BUT_R:
                            drive.stop()
                            break

                        if substick.code == GP_STK_VT:
                            if substick.val == GP_STK_UP_P:
                                drive.fw(spd, 0)
                                print("[    \033[32;1mOK\033[0m   ] up + RB pressed")
                            elif substick.val == GP_STK_DN_P:
                                drive.fw(-spd, 0)
                                print("[    \033[32;1mOK\033[0m   ] down + RB pressed")
                            else:
                                continue

                            while substick.val != GP_STK_R:
                                try:
                                    _, substick = read_event()
                                except:
                                    continue
                            drive.fw(-spd / 1.3, spd / 1.3)

                elif button.code == GP_BUT_A:
                    kit.servo[CH1].angle = 40
                    print(
                        "[    \033[32;1mOK\033[0m   ] channel {0} to angle:\t{1}".format(
                            CH1, 20
                        )
                    )
                elif button.code == GP_BUT_B:
                    kit.servo[CH1].angle = 180
                    print(
                        "[    \033[32;1mOK\033[0m   ] channel {0} to angle:\t{1}".format(
                            CH1, 160
                        )
                    )
                elif button.code == GP_BUT_X:
                    kit.servo[CH2].angle = 0
                    print(
                        "[    \033[32;1mOK\033[0m   ] channel {0} to angle:\t{1}".format(
                            CH2, 20
                        )
                    )
                elif button.code == GP_BUT_Y:
                    kit.servo[CH2].angle = 120
                    print(
                        "[    \033[32;1mOK\033[0m   ] channel {0} to angle:\t{1}".format(
                            CH2, 160
                        )
                    )
            else:
                print(
                    "[    \033[32;1mOK\033[0m   ] button released: clear throttle and reset speed"
                )
                spdfac = 1


except KeyboardInterrupt:
    drive.pwm_cleanup()
    kit.servo[CH1].angle = 0
    kit.servo[CH2].angle = 130
    gamepad.close()
