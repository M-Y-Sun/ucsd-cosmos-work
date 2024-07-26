from time import sleep

from adafruit_servokit import ServoKit

CH_F_X = 0
CH_F_Z = 2
CH_B_X = 15
CH_B_Z = 13

kit = ServoKit(channels=16)
kit.servo[CH_F_X].set_pulse_width_range(400, 2300)
kit.servo[CH_F_Z].set_pulse_width_range(400, 2300)
kit.servo[CH_B_X].set_pulse_width_range(400, 2300)
kit.servo[CH_B_Z].set_pulse_width_range(400, 2300)

kit.servo[CH_F_X].angle = 0
kit.servo[CH_F_Z].angle = 0
kit.servo[CH_B_X].angle = 180
kit.servo[CH_B_Z].angle = 180

try:
    fwd = True
    while True:
        kit.servo[CH_F_X].angle = 0 if fwd else 70
        sleep(2)
        kit.servo[CH_F_Z].angle = 140 if fwd else 60
        sleep(2)
        fwd = False if fwd else True

except KeyboardInterrupt:
    kit.servo[CH_F_X].angle = 0
    kit.servo[CH_F_Z].angle = 0
