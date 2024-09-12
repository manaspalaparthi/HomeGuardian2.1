import RPi.GPIO as GPIO
import os

pin_id = 6

GPIO.setmode(GPIO.BCM)
GPIO.setup(pin_id, GPIO.OUT)

def Infrared_on():
    GPIO.output(pin_id,GPIO.HIGH)


def Infrared_off():
    GPIO.output(pin_id,GPIO.LOW)




Infrared_off()