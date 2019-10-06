import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)  # set up BCM GPIO numbering
GPIO.setup(17, GPIO.OUT)  # set GPIO22 as an output (LED)
GPIO.setup(18, GPIO.OUT)  # set GPIO22 as an output (ALARM)
GPIO.setup(22, GPIO.OUT)  # set GPIO22 as an output (LED)
GPIO.setup(23, GPIO.OUT)  # set GPIO22 as an output (ALARM)

while True:
    print('1\n')
    GPIO.output(17, GPIO.HIGH)
    GPIO.output(18, GPIO.HIGH)
    GPIO.output(22, GPIO.HIGH)
    GPIO.output(23, GPIO.HIGH)
    time.sleep(1)
    GPIO.output(17, GPIO.LOW)
    GPIO.output(18, GPIO.LOW)
    GPIO.output(22, GPIO.LOW)
    GPIO.output(23, GPIO.LOW)
    print('2\n')
    time.sleep(1)
