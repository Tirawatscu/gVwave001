import  RPi.GPIO as GPIO
import pyadda
from adc_consts import *
import time
import numpy as np
import csv
import sys

# Raspberry pi pin numbering setup
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
PIN_DRDY = 11
GPIO.setup(PIN_DRDY, GPIO.IN)

# define gain, sampling rate, and scan mode
gain = ADS1256_GAIN['1']
samplingRate = ADS1256_DRATE['30000']
scanMode = ADS1256_SMODE['DIFFERENTIAL']


def interruptInterpreter(ch):
	pyadda.collectData()
	volts = pyadda.readAllChannelsVolts(adcChannels)
	data.append([timeStamp, volts[0], volts[1], volts[2], volts[3]])

# setup ads1256 chip
pyadda.startADC(gain, samplingRate, scanMode)


meanSampleRate = 0
counter = 0
adcChannels = 8 - 4 * scanMode
#Create a numpy array to store the data 4 channels x 1000 samples
data = []
timeStamp = 0
startTime = time.time()
prevTime = time.time()
GPIO.add_event_detect(PIN_DRDY, GPIO.FALLING)
noSample = int(sys.argv[1])

with open('test_temp_data.csv', 'w') as f:
	f.write('Time (s)')
	for i in range(1, 4):
		f.write(",Ch {}".format(i))
	f.write('\n')

while True:
	trig = time.time()
	if trig - prevTime >= 1/256:
		meanSampleRate += 1/(trig-prevTime)
		timeStamp += trig - prevTime
		prevTime = time.time()
		interruptInterpreter(PIN_DRDY)
		counter += 1
		
	if counter == noSample:
		print(meanSampleRate/noSample)
		break

#Write data to a csv file
with open('test_temp_data.csv', 'a') as f:
	writer = csv.writer(f)
	writer.writerows(data)
