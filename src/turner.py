#!/usr/bin/python -u

import sys
import RPi.GPIO as GPIO
import time

e= 26  #GPIO pin for retract - Board pin37
r = 20 #GPIO pin for extract - Board pin 38
t = 35 #time to retract
te = 20 #time to extend
p = 7200  #turning period - 2 hrs

startTime = time.time()

GPIO.setmode(GPIO.BCM)
GPIO.setup(r, GPIO.OUT)
GPIO.setup(e, GPIO.OUT)
GPIO.output(e, GPIO.HIGH)
GPIO.output(r, GPIO.HIGH)

def extend():
    print (time.strftime("%c") + ": extending")
    GPIO.output(e, GPIO.LOW)
    time.sleep(te)
    GPIO.output(e, GPIO.HIGH)

def retract():
    print (time.strftime("%c") + ": retracting")
    GPIO.output(r, GPIO.LOW)
    time.sleep(t)
    GPIO.output(r, GPIO.HIGH)

	
print (time.strftime("%c") + ": Start Time")

try:
    while True:
        retract()
        time.sleep(p)
	extend()
        time.sleep(p)


finally:
    GPIO.cleanup()
