#!/usr/bin/python -u

import os
import time
import RPi.GPIO as GPIO
import dht11

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

# Temp sensors will use
# PIN2 = POWER
# PIN6 = GROUND
# PIN7 = DATA
heater1 = 16 #pin36
heater2 = 19 #pin 35
humidity_pin = 15 #pin10

overheat1 = 0
underheat1 = 0

GPIO.setmode(GPIO.BCM)
GPIO.setup(heater1, GPIO.OUT)
GPIO.setup(heater2, GPIO.OUT)
GPIO.setup(humidity_pin, GPIO.OUT)

bottom_sensor = '/sys/bus/w1/devices/28-0516a359e5ff/w1_slave'
top_sensor = '/sys/bus/w1/devices/28-0516a4a43fff/w1_slave'
humidity_sensor = dht11.DHT11(pin=humidity_pin)

firstRun = False
heaterOn = False


def temp_raw(sensor):
    f = open(sensor, 'r')
    lines = f.readlines()
    f.close()
    return lines

def read_temp(sensor):
    lines = temp_raw(sensor)
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = temp.raw()
    temp_output = lines[1].find('t=')
    if temp_output != -1:
        temp_string = lines[1].strip()[temp_output+2:]
        temp_c = float(temp_string) / 1000.0
        temp_f = temp_c * 9.0 / 5.0 + 32.0
        return temp_f

def getSleepTime(t1):

    if t1 > 95:
        return 10
    elif t1 > 90:
        return 15
    elif t1 > 80:
        return 10
    elif t1 > 65:
        return 30
    else:
        return 60

def heaterControl(state, heater, isOn):
    if state:
        if isOn == False:
            GPIO.output(heater1, GPIO.LOW)
            GPIO.output(heater2, GPIO.LOW)
        if heater1 == heater1:
            print("Heater1: On")
    else:
        GPIO.output(heater1, GPIO.HIGH)
        GPIO.output(heater2, GPIO.HIGH)
        if heater1 == heater1:
            print("Heater1: Off")


try:
    while True:

        bottom = read_temp(bottom_sensor)
        top = read_temp(top_sensor)

        print(time.strftime("%c"))
        print("Top: " + str(top))
        print("Bottom: " + str(bottom))

        if bottom < 99.5 and top < 100.0:
            heaterControl(True, heater1, heaterOn)
            heaterOn = True
        else:
            heaterControl(False, heater1, heaterOn)
            heaterOn = False

        humidity = humidity_sensor.read()
        if humidity.is_valid():
	    h_temp = humidity.temperature * 9/5 + 32.0
            h = humidity.humidity
            print("H Temp: %d F" % h_temp)
            print("Humidity: %d %%" % h)


        timeToSleep = getSleepTime(bottom)
        print("Sleep Time: " + str(timeToSleep) + "\n")
        time.sleep(timeToSleep)

finally:
    GPIO.cleanup()
