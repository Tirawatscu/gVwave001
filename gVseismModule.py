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

        self.meanSampleRate = 0
        self.counter = 0
        self.adcChannels = 8 - 4 * self.scanMode
        self.timeStamp = 0
        self.prevTime = time.time()
        self.PIN_DRDY = 11

        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.PIN_DRDY, GPIO.IN)

        pyadda.startADC(self.gain, self.samplingRate, self.scanMode)

    def runTest(self):
        with open('test_temp_data.csv', 'w') as f:
            f.write('Time (s)')
            for i in range(1, 4):
                f.write(",Ch {}".format(i))
            f.write('\n')


        data = []
        GPIO.add_event_detect(self.PIN_DRDY, GPIO.FALLING)
        while True:
            trig = time.time()
            if trig - self.prevTime >= 1/256:
                self.meanSampleRate += 1/(trig-self.prevTime)
                self.timeStamp += trig - self.prevTime
                self.prevTime = time.time()
                pyadda.collectData()
                volts = pyadda.readAllChannelsVolts(self.adcChannels)
                data.append([self.timeStamp, volts[0], volts[1], volts[2]])
                self.counter += 1

            if self.counter == 1000:
                print(self.meanSampleRate/1000)
                break
        
        with open('test_temp_data.csv', 'a') as f:
            writer = csv.writer(f)
            writer.writerows(data)