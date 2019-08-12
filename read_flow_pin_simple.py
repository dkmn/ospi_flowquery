#!/usr/bin/python

# -*- coding: utf-8 -*-
import glob
import time
import re
import os
import sys
import RPi.GPIO as GPIO
#import subprocess
#import boto3
import datetime
#from botocore.exceptions import ClientError

GPIO.setmode(GPIO.BCM)

GPIO_PIN_NUMBER=14
GPIO.setup(GPIO_PIN_NUMBER, GPIO.IN)
print ("Starting value: ", GPIO.input(GPIO_PIN_NUMBER))

transition_count = 0
last_value = GPIO.input(GPIO_PIN_NUMBER)
time_window_begin = time_window_short_begin = time_window_end = overall_start_time = time.time()	# initialize to zero-width window, current time
volume_multiplier = 1		# gal/cycle (cycle = 2 transitions)

print ("Overall start time: ", overall_start_time)

for loop_counter in range(0, 50000000):
    print ("Loop counter: ", loop_counter)
    current_value = GPIO.input(GPIO_PIN_NUMBER)
    print ("Current value: ", current_value)
    if current_value != last_value:
        last_value = current_value
        transition_count += 1
        print ("Transition count: ", transition_count)
    time.sleep(0.25)

