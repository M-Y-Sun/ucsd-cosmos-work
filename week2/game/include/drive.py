import sys

import RPi.GPIO as GPIO

# define GPIO pins
GPIO_AIN1 = 17
GPIO_AIN2 = 27
GPIO_PWMA = 22
GPIO_PWMB = 13
GPIO_BIN1 = 5
GPIO_BIN2 = 6

GPIO.setmode(GPIO.BCM)  # use BCM pin numbers

# set pins as output
GPIO.setup(GPIO_AIN1, GPIO.OUT)
GPIO.setup(GPIO_AIN2, GPIO.OUT)
GPIO.setup(GPIO_PWMA, GPIO.OUT)
GPIO.setup(GPIO_BIN1, GPIO.OUT)
GPIO.setup(GPIO_BIN2, GPIO.OUT)
GPIO.setup(GPIO_PWMB, GPIO.OUT)

# stop the motors on init
GPIO.output(GPIO_AIN1, False)
GPIO.output(GPIO_AIN2, False)
GPIO.output(GPIO_BIN1, False)
GPIO.output(GPIO_BIN2, False)

PWM_FREQ = 50

PWMA = GPIO.PWM(GPIO_PWMA, PWM_FREQ)
PWMB = GPIO.PWM(GPIO_PWMB, PWM_FREQ)

PWMA.start(100)
PWMB.start(100)


def pwm_cleanup():
    PWMA.stop()
    PWMB.stop()


def stop(msg=None):
    GPIO.output(GPIO_AIN1, False)
    GPIO.output(GPIO_AIN2, False)
    GPIO.output(GPIO_BIN1, False)
    GPIO.output(GPIO_BIN2, False)
    if msg != None:
        print(msg)


def fwd(bdc, adc, msg=None):
    if adc < -100 or bdc < -100 or adc > 100 or bdc > 100:
        sys.stderr.write("PWM duty cycle must be in the range [-100,100]")
        return

    PWMA.ChangeDutyCycle(abs(adc))
    PWMB.ChangeDutyCycle(abs(bdc))

    apos = adc > 0
    bpos = bdc > 0
    GPIO.output(GPIO_AIN1, apos)
    GPIO.output(GPIO_AIN2, not apos)
    GPIO.output(GPIO_BIN1, bpos)
    GPIO.output(GPIO_BIN2, not bpos)

    if msg != None:
        print(msg)
