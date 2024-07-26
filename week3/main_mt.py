from multiprocessing import Process
from time import sleep

from adafruit_servokit import ServoKit

dur = 0.7

kit = ServoKit(channels=16)

kit.servo[0].set_pulse_width_range(400, 2300)
kit.servo[2].set_pulse_width_range(400, 2300)

kit.servo[13].set_pulse_width_range(400, 2300)
kit.servo[15].set_pulse_width_range(400, 2300)


def start_front():
    fwd = True
    while True:
        try:
            kit.servo[0].angle = 0 if fwd else 70
            sleep(dur)
            kit.servo[2].angle = 140 if not fwd else 70
            sleep(dur)
            fwd = False if fwd else True
        except KeyboardInterrupt:
            kit.servo[0].angle = 45
            kit.servo[2].angle = 90
            break


def start_back():
    fwd = True
    while True:
        try:
            kit.servo[15].angle = 180 if not fwd else 120
            sleep(dur)
            kit.servo[13].angle = 70 if fwd else 140
            sleep(dur)
            fwd = False if fwd else True
        except KeyboardInterrupt:
            kit.servo[13].angle = 100
            kit.servo[15].angle = 150
            break


if __name__ == "__main__":
    p1 = Process(target=start_front)
    p2 = Process(target=start_back)
    p1.start()
    p2.start()
