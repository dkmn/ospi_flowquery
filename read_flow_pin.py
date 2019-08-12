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

print ("Overall start time: %.2f sec" % overall_start_time)

for loop_counter in range(0, 50000000):
    current_value = GPIO.input(GPIO_PIN_NUMBER)
    if current_value != last_value:
        last_value = current_value
        transition_count += 1
        if transition_count % 2 == 0:
            nowish = time.time()
            print ("Loop counter: %d" %  loop_counter)
            time_window_end = nowish
            print ("Now: %.2f Window start: %.2f" % (nowish, time_window_begin))
            print ("Now: %.2f Short window start: %.2f" %  (nowish,time_window_short_begin))
            est_flow_rate_window_recent = (60.0/(nowish - time_window_short_begin)) * (volume_multiplier)
            est_flow_rate_window_total = (60.0/(nowish - time_window_begin)) * transition_count * (volume_multiplier / 2.0)
            total_flow_to_date = transition_count * volume_multiplier / 2.0
            print ("Estimated flow rate recent (gal/min): %.2f" % est_flow_rate_window_recent)
            print ("Estimated flow rate total (gal/min): %.2f" % est_flow_rate_window_total)
            print ("Total volume to date: %.2f" % total_flow_to_date)
            avg_flow_rate_to_date = (60.0 * total_flow_to_date) / (nowish - overall_start_time)
            print ("Average flow rate since script start: %.2f" %  avg_flow_rate_to_date)
            print ("Current transition count: %d" % transition_count)
            print ("Current value: %d" % current_value)
            time_window_short_begin = nowish
    time.sleep(0.25) 
