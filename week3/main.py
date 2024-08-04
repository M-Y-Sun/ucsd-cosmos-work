from time import sleep
from adafruit_servokit import ServoKit

dur = 1

kit = ServoKit(channels=16)

kit.servo[0].set_pulse_width_range(400, 2300)
kit.servo[2].set_pulse_width_range(400,2300)
kit.servo[13].set_pulse_width_range(400, 2300)
kit.servo[15].set_pulse_width_range(400,2300)

# channels 0 and 2 are the front legs and channels 13 and 15 are the back legs

fwd = True
while True:
    try:
        # move the vertical front and back servos in the opposite direction
        kit.servo[0].angle = 0 if fwd else 70
        kit.servo[15].angle = 180 if not fwd else 120
        sleep(dur)
        # move the horizontal front and back servos in the opposite direction
        kit.servo[2].angle = 140 if not fwd else 70
        kit.servo[13].angle = 70 if fwd else 140
        sleep(dur)

        fwd = False if fwd else True  # swap the direction
    except KeyboardInterrupt:
        # reset servos to their horizontal position
        kit.servo[0].angle = 45
        kit.servo[2].angle = 90
        kit.servo[13].angle = 100
        kit.servo[15].angle = 150
