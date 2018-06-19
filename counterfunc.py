#!/usr/bin/python
import time, datetime, csv, sys
import RPi.GPIO as GPIO

from papirus import *

SW1 = 21
SW2 = 16
SW3 = 20
SW4 = 19
SW5 = -1

global counter
counter = 0

def write_to_csv():
    global counter
    current_day = datetime.datetime.now()
    record_date = current_day.strftime('%Y-%m-%d')

    with open(record_date, 'wr') as file_object:
        write = csv.writer(file_object)
        write.writerows([[counter / 2]])

def sensor_ops(channel):
    global counter
    timestamp = time.time()
    stamp = datetime.datetime.fromtimestamp(timestamp).strftime('%H:%M:%S')
    sensor = GPIO.input(channel)
    
    if sensor == GPIO.LOW:
        #No Magnet Detected.
        print 'Door Open' + stamp
        counter += 1
        write_to_csv()
        blink_led(22)
        led_off(27)
        print 'Door Opened  %s Times.' % (counter)
    if sensor == GPIO.HIGH:
        #Magnet Detected.
        blink_led(27)
        led_off(22)
        print 'Door Closed.'
        time.sleep(0.25)
        led_off(27)
        
def blink_led(pin):
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.HIGH)
    time.sleep(0.25)
    
def led_off(pin):
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)
    time.sleep(0.25)
    
if __name__ == '__main__':
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(4, GPIO.IN)
    GPIO.add_event_detect(4, GPIO.BOTH, callback = sensor_ops, bouncetime=200)

    try:
        while True:
            time.sleep(0.1)               
    except KeyboardInterrupt:
        GPIO.cleanup()
