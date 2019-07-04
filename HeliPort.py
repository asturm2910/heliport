#!/usr/bin/python

#############################################################################
# Program: Heli Port Light Application
# Author: Alexander Sturm
# Creation Date: 23.04.2018
# Last Modification: 24.04.2018
# Version: 1.00.00
# 
# The Application controls 12 LEDs with GPIO output. The LEDs can be used
# as warning and positioning light. 
# There is an implementation of six different ligth animations:
# - Blink
# - Running Light
# - Yellow / Red Change (switch between odd and evan lights)
# - Flash (Double short flash of all lights)
# - Red Flash (Double short flash of all odd LEDs)
# - Yellow Flash (Double short flash of all even LEDs)
# 
#############################################################################
import RPi.GPIO as GPIO
import time

BLINKEN_PAUSE = 1.0
RUNNING_PAUSE = 0.4
RED_GREEN_PAUSE = 2.0
FLASH_ON_PAUSE = 0.1
FLASH_OFF_PAUSE = 3.0
MAX_PAUSE = 0.1

LED1_PIN = 7
LED2_PIN = 21
LED3_PIN = 20
LED4_PIN = 16
LED5_PIN = 12
LED6_PIN = 8
LED7_PIN = 25
LED8_PIN = 24
LED9_PIN = 14
LED10_PIN = 15
LED11_PIN = 18
LED12_PIN = 23

TASTER_PIN = 4

YELLOW_FLASH = 100
RED_FLASH = 200

ledPins=[LED1_PIN, LED2_PIN, LED3_PIN, LED4_PIN, LED5_PIN, LED6_PIN, LED7_PIN, LED8_PIN, LED9_PIN, LED10_PIN, LED11_PIN, LED12_PIN]

def initialize(pause=2):
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(TASTER_PIN, GPIO.IN)
    for pin in ledPins:
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, GPIO.LOW)
    time.sleep(pause)


def readTaster():
    taster = GPIO.input(TASTER_PIN)
    result = False
    if taster == 1:
        tastertext = "\033[1;32;40mAn \033[0m"
        result = True
    else:
        tastertext = "\33[1;31;40mAus\033[0m"
        result = False
    
    print("\033[10;1HTasterstatus: ",tastertext)
    return result

def pause(p):
    times = int(p // MAX_PAUSE)
    restTime = p % MAX_PAUSE
    for i in range(0, times):
        time.sleep(MAX_PAUSE)
        readValue = readTaster()
        if not readValue:
            return readValue

    time.sleep(restTime)
    readValue = readTaster()
    return readValue
    

def off():
    print("\033[4;1HModus: {:20}".format("Off"))
    print("\033[5;1HWiederholung: \033[1;37;44m{:>8}\033[0m".format("0"))

    for pin in ledPins:
        GPIO.output(pin, GPIO.LOW)

def blinken():
    print("\033[4;1HModus: {:20}".format("Blinken"))
    loopcounter = 1
    leave = False

    while not leave:
        print("\033[5;1HWiederholung: \033[1;37;44m{:>8}\033[0m".format(loopcounter))
        for pin in ledPins:
            if loopcounter % 2 == 0:
                GPIO.output(pin, GPIO.HIGH)
            else:
                GPIO.output(pin, GPIO.LOW)
        if not pause(BLINKEN_PAUSE):
            leave = True
            break
        
        loopcounter += 1

def runningLight():
    print("\033[4;1HModus: {:20}".format("Lauflicht"))
    loopcounter = 1
    leave = False

    while not leave:
        print("\033[5;1HWiederholung: \033[1;37;44m{:>8}\033[0m".format(loopcounter))
        for pin in ledPins:
            for i in ledPins:
                GPIO.output(i, GPIO.LOW)
            GPIO.output(pin, GPIO.HIGH)
            if not pause(RUNNING_PAUSE):
                leave = True
                break
        loopcounter += 1


def greenRedSwitch():
    print("\033[4;1HModus: {:20}".format("Green Red Switch"))
    loopcounter = 1
    leave = False

    while not leave:
        print("\033[5;1HWiederholung: \033[1;37;44m{:>8}\033[0m".format(loopcounter))
        countVar = 0
        for pin in ledPins:
            if (countVar % 2 == 0 and loopcounter % 2 == 0):
                GPIO.output(pin, GPIO.HIGH)
            elif countVar % 2 != 0 and loopcounter % 2 != 0:
                GPIO.output(pin, GPIO.HIGH)
            else:
                GPIO.output(pin, GPIO.LOW)
            countVar += 1

        if not pause(RED_GREEN_PAUSE):
            leave = True
        
        loopcounter += 1


def flash(flashMode=0):
    if flashMode == RED_FLASH:
        print("\033[4;1HModus: {:20}".format("Red Flash"))
    elif flashMode == YELLOW_FLASH:
        print("\033[4;1HModus: {:20}".format("Yellow Flash"))
    else:
        print("\033[4;1HModus: {:20}".format("Flash"))

    loopcounter = 1
    leave = False

    while not leave:
        print("\033[5;1HWiederholung: \033[1;37;44m{:>8}\033[0m".format(loopcounter))
        for i in range(0,5):
            pinCounter = 0
            for pin in ledPins:
                if (flashMode == RED_FLASH and pinCounter % 2 == 0) or (flashMode == YELLOW_FLASH and pinCounter % 2 != 0) or flashMode == 0:
                    GPIO.output(pin, (i%2))
                else:
                    GPIO.output(pin, GPIO.LOW)
                pinCounter += 1
            if not pause(FLASH_ON_PAUSE):
                leave = True
                break
        if not pause(FLASH_OFF_PAUSE):
            leave = True
        loopcounter += 1


def alwaysOn():
    leave = False
    print("\033[4;1HModus: {:20}".format("Always On"))
    print("\033[5;1HWiederholung: \033[1;37;44m{:>8}\033[0m".format(1))
    for pin in ledPins:
        GPIO.output(pin, GPIO.HIGH)
    while not leave:
        if not pause(MAX_PAUSE):
            leave = True


def modusSwitch():
    off()
    time.sleep(2) 
    print("\033c")
    print("\033[1;33;44mHeli Port Light Application\33[0m")


print("\033c")
print("\033[1;33;44mHeli Port Light Application\33[0m")
initialize()
readTaster()
while True:
    blinken()
    modusSwitch()
    runningLight()
    modusSwitch()
    greenRedSwitch()
    modusSwitch()
    flash()
    modusSwitch()
    flash(RED_FLASH)
    modusSwitch()
    flash(YELLOW_FLASH)
    modusSwitch()
    alwaysOn()
    modusSwitch()



