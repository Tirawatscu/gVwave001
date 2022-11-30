import RPi.GPIO as GPIO
import pyadda
from adc_consts import *
import time
import numpy as np
import csv

class gVseismModule():
    def __init__(self, gain, samplingRate, scanMode):
        self.gain = ADS1256_GAIN[gain]
        self.samplingRate = ADS1256_DRATE[samplingRate]
        self.scanMode = ADS1256_SMODE[scanMode]

        self.adcChannels = 8 - 4 * self.scanMode
        self.PIN_DRDY = 11

    def runTest(self):
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.PIN_DRDY, GPIO.IN)
        pyadda.startADC(self.gain, self.samplingRate, self.scanMode)
        with open('test_temp_data.csv', 'w') as f:
            f.write('Time (s)')
            for i in range(1, 4):
                f.write(",Ch {}".format(i))
            f.write('\n')

        data = []
        counter = 0
        meanSampleRate = 0
        timeStamp = 0
        prevTime = time.time()
        GPIO.add_event_detect(self.PIN_DRDY, GPIO.FALLING)
        while True:
            trig = time.time()
            if trig - prevTime >= 1/256:
                meanSampleRate += 1/(trig-prevTime)
                timeStamp += trig - prevTime
                prevTime = time.time()
                pyadda.collectData()
                volts = pyadda.readAllChannelsVolts(self.adcChannels)
                data.append([timeStamp, volts[0], volts[1], volts[2]])
                counter += 1

            if counter == 1000:
                print(meanSampleRate/1000)
                break
        
        with open('test_temp_data.csv', 'a') as f:
            writer = csv.writer(f)
            writer.writerows(data)
        GPIO.cleanup()