# This script is under prioritization of Mamostza. Don't rewrite, copy, or use for the commercial way
# Acknowledged by Tirawat^2

import numpy as np
from numpy import fft, unwrap, angle, sqrt, var, mean, std, pi
import pandas as pd
import sys

class POP():
    def __init__(self,data_v,data_x,data_y,radius,freq,length):
        self.data = data_v
        self.data_x = data_x
        self.data_y = data_y
        self.radius = radius
        self.freq = freq
        self.length = 2 * int(length/2)
        self.F = self.freq / self.length * np.arange(0, self.length/2)
        self.stdKR1 = np.zeros((int(length/2), 1))

    def makepop(self):
        TL = self.data.shape[0]
        segment = int(np.ceil((TL-self.length)/self.length*2))
        KR = np.zeros((int(self.length/2), segment))
        for idx, i in enumerate(np.arange(0, TL-self.length, self.length/2, dtype=int)):
           P = unwrap(angle(fft.fft(self.data[i:i+self.length,:]* np.hanning(self.length).reshape(self.length,1),axis=0)),axis=1)[0:int(self.length/2)]
           KR[:, idx] = sqrt(2*(var(P,axis=1)))
        C  = 2*pi*self.radius*self.F/mean(KR, axis=1)
        self.stdKR1[:, 0] = std(KR, axis=1)*C
        C2 = 2*pi*self.radius*self.F/(pi/1.5)
        return self.F, C, C2, self.stdKR1

