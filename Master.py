#import Pyqt5 modules
from multiprocessing import Event
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QDialog, QTableWidgetItem
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot, QThread, pyqtSignal, QObject
#import window.py class
from window import Ui_gVwave
from projectDialog import Ui_Dialog
import json
import pandas as pd
import numpy as np
#import other modules
import os
import sys
from PyPOP import POP
import pyqtgraph as pg
import swprepost
import matplotlib.pyplot as plt
import matplotlib as mpl
import pyqtgraph as pg
import subprocess
import time
import threading
import LicenseTool as LT
from gVseismModule import gVseismModule

class Worker(QObject):
    finished = pyqtSignal()
    progress = pyqtSignal(int)
    def __init__(self, gain, samplingRate, scanMode, sample, filePath):
        super().__init__()
        self.gV = gVseismModule(gain, samplingRate, scanMode, sample, filePath)

    def run(self):
        #subprocess.call(['sudo python gVseism/runTest.py 2000'], shell=True)
        self.gV.runTest()
        self.finished.emit()

    def record(self):
        self.gV.recordWave()
        self.finished.emit()

class analysisThread(QObject):
    finished = pyqtSignal()
    progress = pyqtSignal(int)
    def __init__(self, param, target, iter, model):
        super().__init__()
        self.param = param
        self.target = target
        self.iter = iter
        self.model = model

    def run(self):
        subprocess.check_call(['{}/RunDinver.sh'.format(os.path.dirname(__file__)), self.param, self.target, self.iter, self.model])
        self.finished.emit()

class MyApp(QMainWindow):
    def __init__(self, parent=None):
        super(MyApp, self).__init__(parent)
        self.ui = Ui_gVwave()
        self.ui.setupUi(self)
        self.showFullScreen()
        self.ui.Wave1.setBackground('w')
        self.ui.actionNew_Workspace.triggered.connect(self.menuFile)
        self.ui.actionOpen.triggered.connect(self.getfile)
        self.timeDuration = {
            '30 s' : 30,
            '1 min' : 60,
            '2 min' : 120,
            '5 min' : 300,
            '10 min' : 600,
            '15 min' : 900,
            '30 min' : 1800,
            '1 hr' : 3600,
            '2 hr' : 7200,
        }

        #set font size in pyqtplot
        self.ui.Wave1.setLabel('left', 'Voltage', units='V')
        self.ui.Wave1.setLabel('bottom', 'Time', units='s')
        self.ui.Wave2.setBackground('w')
        self.ui.Wave2.setLabel('left', 'Voltage', units='V')
        self.ui.Wave3.setBackground('w')
        self.ui.Wave3.setLabel('left', 'Voltage', units='V')
        self.ui.tableWidget.setColumnCount(1)
        self.ui.tableWidget.setColumnWidth(0, 250)
        self.ui.tableWidget.cellClicked.connect(self.rowSelected)
        self.ui.dsPlot.clicked.connect(self.dsPlot)
        #Initialize Input text box
        self.ui.Station_in.setText('Location')
        self.ui.Lat_in.setText('0')
        self.ui.Long_in.setText('0')
        self.ui.Radius_in.setText('3')
        self.ui.Sample.setText(str(self.timeDuration[self.ui.Duration_in.currentText()]*128))
        #Disable all buttons and input text box
        self.ui.Station_in.setEnabled(False)
        self.ui.Lat_in.setEnabled(False)
        self.ui.Long_in.setEnabled(False)
        self.ui.Radius_in.setEnabled(False)
        self.ui.StartButton.setEnabled(False)
        self.ui.Duration_in.setEnabled(False)
        self.ui.ID_in.setEnabled(False)
        self.ui.Sample.setEnabled(False)
        self.ui.menuFile.setEnabled(False)
        #Set callback lable (Text, Combobox etc. here)
        self.ui.Duration_in.currentTextChanged.connect(self.updateSample)
        self.ui.StartButton.clicked.connect(self.startFunction)
        self.ui.PrevLogger.clicked.connect(self.prevLogger)
        self.ui.Analyse.clicked.connect(self.analFunction)
        self.ui.Analyzing.clicked.connect(self.inversion)
        self.ui.RunButton.clicked.connect(self.runTest)
        self.ui.maxYDs.valueChanged.connect(self.adjustRangeDs)
        self.ui.maxXDs.valueChanged.connect(self.adjustRangeDs)
        self.ui.minXDs.valueChanged.connect(self.adjustRangeDs)
        self.ui.minXanal.valueChanged.connect(self.adjustRangeAnal)
        self.ui.maxXanal.valueChanged.connect(self.adjustRangeAnal)

        self.ui.VsProfile.setLabel('bottom', 'Shear wave velocity', units='m/s')
        self.ui.VsProfile.setLabel('left', 'Depth', units='m')
        self.ui.VsProfile.setBackground('w')
        self.ui.VpProfile.setLabel('bottom', 'Compression wave velocity', units='m/s')
        self.ui.VpProfile.setLabel('left', 'Depth', units='m')
        self.ui.VpProfile.setBackground('w')
        self.ui.densityProfile.setLabel('bottom', 'Density', units='g/m3')
        self.ui.densityProfile.setLabel('left', 'Depth', units='m')
        self.ui.densityProfile.setBackground('w')

        self.ui.VsProfile_2.setLabel('bottom', 'Shear wave velocity', units='m/s')
        self.ui.VsProfile_2.setLabel('left', 'Depth', units='m')
        self.ui.VsProfile_2.setBackground('w')
        self.ui.VpProfile_2.setLabel('bottom', 'Compression wave velocity', units='m/s')
        self.ui.VpProfile_2.setLabel('left', 'Depth', units='m')
        self.ui.VpProfile_2.setBackground('w')
        self.ui.densityProfile_2.setLabel('bottom', 'Density', units='g/m3')
        self.ui.densityProfile_2.setLabel('left', 'Depth', units='m')
        self.ui.densityProfile_2.setBackground('w')

        self.ui.nLayer.setText('3')
        self.ui.thickness.setText('1')
        self.ui.iteration.setText('10000')
        self.ui.lr.setEnabled(False)
        self.ui.dF.setEnabled(False)
        self.ui.reverseLayer.setChecked(True)
        self.ui.progressBar.setFormat('Ready')

        #check folder Storage exist or not if not create it
        if not os.path.exists(os.path.join(os.path.dirname(__file__), 'Storage')):
            os.makedirs(os.path.join(os.path.dirname(__file__), 'Storage'))
        if not os.path.exists(os.path.join(os.path.dirname(__file__), 'Workspace')):
            os.makedirs(os.path.join(os.path.dirname(__file__), 'Workspace'))
        '''if not os.path.exists('Header'):
            os.makedirs('Header')'''
        self.storagePath = os.path.join(os.path.dirname(__file__), 'Storage')
        self.workspacePath = os.path.join(os.path.dirname(__file__), 'Workspace')
        #self.ui.LicenseKey.setText('IgMxIyEjMyQhNCMi')
        self.ui.Activation.clicked.connect(self.submitLicense)
        self.checkLicense()
        
    def checkLicense(self):
        #check license key file exist or not
        if os.path.exists(os.path.join(os.path.dirname(__file__), 'LicenseKey.txt')):
            #read license key from file
            with open(os.path.join(os.path.dirname(__file__), 'LicenseKey.txt'), 'r') as f:
                self.licenseKey = f.read()
                self.ui.LicenseKey.setText(self.licenseKey)
                #check license key valid or not
                if LT.check_key(self.licenseKey):
                    self.ui.menuFile.setEnabled(True)
                    self.ui.progressBar.setFormat('Activated')
                    self.ui.Activation.setEnabled(False)
                else:
                    self.ui.progressBar.setFormat('License key is not valid')
                    self.ui.progressBar.setValue(0)
    
    def submitLicense(self):
        if not os.path.exists(os.path.join(os.path.dirname(__file__), 'LicenseKey.txt')):
            with open(os.path.join(os.path.dirname(__file__), 'LicenseKey.txt'), 'w') as f:
                f.write(self.ui.LicenseKey.text())
                
        else:
            with open(os.path.join(os.path.dirname(__file__), 'LicenseKey.txt'), 'w') as f:
                f.write(self.ui.LicenseKey.text())
                
        self.licenseKey = self.ui.LicenseKey.text()
        if LT.check_key(self.licenseKey):
            self.ui.menuFile.setEnabled(True)
            self.ui.progressBar.setFormat('Activated')
            self.ui.Activation.setEnabled(False)
        else:
            self.ui.progressBar.setFormat('License key is not valid')
            self.ui.progressBar.setValue(0)
    
    def prevLogger(self):
        self.ui.tabWidget.setCurrentIndex(1)

    def updateSample(self):
        self.ui.Sample.setText(str(self.timeDuration[self.ui.Duration_in.currentText()]*128))

    def UpdateConfig(self):
        self.Station = self.ui.Station_in.text()
        self.Lat     = self.ui.Lat_in.text()
        self.Long    = self.ui.Long_in.text()
        self.Radius  = self.ui.Radius_in.text()
        print("Station :", self.Station)
        print("Location : Lat ", self.Lat, "Long ", self.Long)
        print("Array radius : ",self.Radius," m")


    def menuFile(self):
        self.newProjectDialog = NewProject_dialog()
        #newProjectDialog.show()
        self.Station = self.newProjectDialog.getName()
        self.ui.Station_in.setText(self.Station)
        if self.Station != '':
            self.ui.Lat_in.setEnabled(True)
            self.ui.Long_in.setEnabled(True)
            self.ui.Radius_in.setEnabled(True)
            self.ui.StartButton.setEnabled(True)
            self.ui.Duration_in.setEnabled(True)
            self.ui.ID_in.setEnabled(False)
            saveConfigState = True
        else:
            self.ui.Lat_in.setEnabled(False)
            self.ui.Long_in.setEnabled(False)
            self.ui.Radius_in.setEnabled(False)
            self.ui.StartButton.setEnabled(False)
            self.ui.Duration_in.setEnabled(False)
            self.ui.ID_in.setEnabled(False)
            saveConfigState = False
        if  saveConfigState:
            if not os.path.exists(os.path.join(self.storagePath, self.Station)):
                os.makedirs(os.path.join(self.storagePath, self.Station))
                with open(self.workspacePath+"/"+self.Station+'.json', 'w') as f:
                    json.dump([], f, indent=4)
                self.ui.ID_in.setText('000')

    def getfile(self):
        fname = QFileDialog.getOpenFileName(self, "Import json", self.workspacePath, "JSON Files (*.json)")[0]
        self.ui.Station_in.setText(fname.split('/')[-1].split('.')[0])
        if fname != '':
            self.ui.Lat_in.setEnabled(True)
            self.ui.Long_in.setEnabled(True)
            self.ui.Radius_in.setEnabled(True)
            self.ui.StartButton.setEnabled(True)
            self.ui.Duration_in.setEnabled(True)
            self.ui.ID_in.setEnabled(False)
            saveState = True
        else:
            self.ui.Lat_in.setEnabled(False)
            self.ui.Long_in.setEnabled(False)
            self.ui.Radius_in.setEnabled(False)
            self.ui.StartButton.setEnabled(False)
            self.ui.Duration_in.setEnabled(False)
            self.ui.ID_in.setEnabled(False)
            saveState = False
        if saveState:
            self.ui.tableWidget.clear()
            self.ui.tableWidget.setHorizontalHeaderLabels(['Event'])
            # Load json file
            with open(fname, 'r') as f:
                self.data = json.load(f)
            self.ui.ID_in.setText("{0:03}".format(len(self.data)))
            #delete all row in table
            self.ui.tableWidget.setRowCount(0)
            for row in range(len(self.data)):
                insertedItem = self.data[row]['Station']+'_'+str(self.data[row]['id'])
                currentRow = self.ui.tableWidget.rowCount()
                self.ui.tableWidget.insertRow(currentRow)
                self.ui.tableWidget.setItem(currentRow, 0, QTableWidgetItem(insertedItem))

    def rowSelected(self):
        currentRow = self.ui.tableWidget.currentRow()
        self.ui.station_Out.setText(self.data[currentRow]['Station'])
        self.ui.id_Out.setText(str(self.data[currentRow]['id']))
        self.ui.lat_Out.setText(str(self.data[currentRow]['Lat']))
        self.ui.long_Out.setText(str(self.data[currentRow]['Long']))
        self.ui.rad_Out.setText(str(self.data[currentRow]['Radius']))
        self.ui.sample_Out.setText(str(self.data[currentRow]['Duration']))

        #Concatenate Station and Id to get file name .csv
        self.fileName = self.data[currentRow]['Station']+'_'+str(self.data[currentRow]['id'])+'.csv'
        self.filePath = os.path.join(self.storagePath, self.data[currentRow]['Station'], self.fileName)
        if os.path.isfile(self.filePath):
            self.ui.dsPlot.setEnabled(True)
            #Load data from .csv file without header using pandas
            self.df = pd.read_csv(self.filePath)
            print(self.df)
            self.Freq = 128
            self.time = np.arange(0, int(len(self.df)/self.Freq), 1/self.Freq)
            self.ui.Wave1_2.clear()
            self.ui.Wave1_2.plot(self.time, self.df['Ch 1'], pen='r')
            self.ui.Wave1_2.setLabel('left', 'Amplitude', units='V')
            self.ui.Wave1_3.clear()
            self.ui.Wave1_3.plot(self.time, self.df['Ch 2'], pen='g')
            self.ui.Wave1_3.setLabel('left', 'Amplitude', units='V')
            self.ui.Wave1_4.clear()
            self.ui.Wave1_4.plot(self.time, self.df['Ch 3'], pen='b')
            self.ui.Wave1_4.setLabel('left', 'Amplitude', units='V')
        else:
            self.ui.dsPlot.setEnabled(False)
            self.ui.Wave1_2.clear()
            self.ui.Wave1_3.clear()
            self.ui.Wave1_4.clear()

        #check model file exist
        file = '{}/Model/'.format(os.path.dirname(__file__))+self.ui.Station_in.text()+'/'+self.ui.Station_in.text()+'_'+str(self.ui.id_Out.text() + '.txt')
        if os.path.isfile(file):
            self.ui.ExistedModel.setEnabled(True)
        else:
            self.ui.ExistedModel.setEnabled(False)


    #------------- Save Configuration ----------------#
    #-------------------------------------------------#
    def saveConfigJson(self, Station, id, Lat, Long, Radius, Duration, Sample):
        with open(self.workspacePath+'/'+Station+'.json') as f:
            data = json.load(f)
            save = {
            'Station' : Station,
            'id' : "{0:03}".format(len(data)),
            'Lat' : Lat,
            'Long' : Long,
            'Radius' : Radius,
            'Duration' : Duration,
            'Sample' : Sample,
        }
            data.append(save)
    
        with open(self.workspacePath+"/"+self.Station+'.json', 'w') as outfile:
            json.dump(data, outfile, indent=4)
        print("Save Config")
    #-------------------------------------------------#

    #------------------- Run Test --------------------#
    #-------------------------------------------------#

    def runTest(self):
        #self.gV.runTest()
        #subprocess.call(['sudo python gVseism/runTest.py 2000'], shell=True)
        #read test_temp_data.csv and plot to Wave1_1
        self.thread = QThread()
        self.worker = Worker('1', '3750', 'DIFFERENTIAL', 1000, "test_temp_data.csv")
        self.worker.moveToThread(self.thread)
        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.onFinishedTest)
        self.thread.start()

        #Progress Bar Test in 1000 Samples with 128 Hz
        self.ui.progressBar.setValue(0)
        self.ui.progressBar.setMaximum(100)
        self.ui.progressBar.setMinimum(0)
        self.ui.progressBar.setFormat('Running Test')
        totalTime = 1000/128
        now = time.time()
        while True:
            if time.time() - now > totalTime:
                break
            self.ui.progressBar.setValue(int((time.time() - now)/totalTime*100))
            time.sleep(2)

    def onFinishedTest(self):
        self.thread.quit()
        self.thread.wait()
        self.ui.progressBar.setValue(100)
        self.ui.progressBar.setFormat('Testing Finished')
        dfTemp = pd.read_csv('test_temp_data.csv')
        time = dfTemp['Time (s)']
        self.ui.Wave1.clear()
        self.ui.Wave1.plot(time, dfTemp['Ch 1'], pen='r')
        self.ui.Wave2.clear()
        self.ui.Wave2.plot(time, dfTemp['Ch 2'], pen='g')
        self.ui.Wave3.clear()
        self.ui.Wave3.plot(time, dfTemp['Ch 3'], pen='b')

    #-------------------------------------------------#

    #--------------- Start Recording -----------------#
    #-------------------------------------------------#
    def startFunction(self):
        self.UpdateConfig()

        with open(self.workspacePath+"/"+self.Station+'.json') as f:
            data = json.load(f)

        self.saveConfigJson(self.Station, 0, float(self.Lat), float(self.Long), float(self.Radius), float(self.timeDuration[self.ui.Duration_in.currentText()]), float(self.ui.Sample.text()))
        print("Start Function")
        self.fileName = self.Station+'_'+"{0:03}".format(len(data))+'.csv'
        self.filePath = os.path.join(self.storagePath, self.Station, self.fileName)

        self.thread = QThread()
        self.worker = Worker('1', '3750', 'DIFFERENTIAL', int(self.ui.Sample.text()), self.filePath)
        self.worker.moveToThread(self.thread)
        self.thread.started.connect(self.worker.record)
        self.worker.finished.connect(self.afterRecord)
        self.thread.start()

        self.ui.Lat_in.setEnabled(False)
        self.ui.Long_in.setEnabled(False)
        self.ui.Radius_in.setEnabled(False)
        self.ui.StartButton.setEnabled(False)
        self.ui.Duration_in.setEnabled(False)
        self.ui.ID_in.setEnabled(False)

        self.ui.progressBar.setValue(0)
        self.ui.progressBar.setMaximum(100)
        self.ui.progressBar.setMinimum(0)
        self.ui.progressBar.setFormat('Recording')
        totalTime = int(self.ui.Sample.text())/128
        now = time.time()
        while True:
            if time.time() - now > totalTime:
                break
            self.ui.progressBar.setValue(int((time.time() - now)/totalTime*100))
            time.sleep(1)

    #--------------- After Recording ----------------#
    def afterRecord(self):
        self.thread.quit()
        self.thread.wait()
        self.ui.progressBar.setValue(100)
        self.ui.progressBar.setFormat('Recording Finished')
        self.ui.tableWidget.clear()
        self.ui.tableWidget.setHorizontalHeaderLabels(['Event'])
        # Load json file
        with open(self.workspacePath+"/"+self.Station+'.json', 'r') as f:
            self.data = json.load(f)
        self.ui.ID_in.setText("{0:03}".format(len(self.data)))
        #delete all row in table
        self.ui.tableWidget.setRowCount(0)
        for row in range(len(self.data)):
            insertedItem = self.data[row]['Station']+'_'+str(self.data[row]['id'])
            currentRow = self.ui.tableWidget.rowCount()
            self.ui.tableWidget.insertRow(currentRow)
            self.ui.tableWidget.setItem(currentRow, 0, QTableWidgetItem(insertedItem))
        self.ui.Lat_in.setEnabled(True)
        self.ui.Long_in.setEnabled(True)
        self.ui.Radius_in.setEnabled(True)
        self.ui.StartButton.setEnabled(True)
        self.ui.Duration_in.setEnabled(True)
        #Switch to Loggin Tab
        self.ui.tabWidget.setCurrentIndex(1)
        self.ui.tableWidget.selectRow(len(self.data)-1)
        self.ui.tableWidget.setFocus()
        self.rowSelected()

    #--------------- Stop Recording ------------------#

    def dsPlot(self):
        self.ui.tabWidget.setCurrentIndex(2)
        self.ui.dsGraph.clear()

        data = np.array([self.df["Ch 1"],self.df["Ch 2"], self.df["Ch 3"]]).T
        pop1 = POP(data, [], [], float(self.ui.rad_Out.text()), self.Freq, 2048)
        [self.F, self.C, C2, self.std] = pop1.makepop()
        #replace NAN with 0
        self.C[np.isnan(self.C)] = 0
        self.ui.dsGraph.plot(self.F, self.C, pen='r')
        self.ui.dsGraph.plot(self.F, C2, pen='b')
        self.ui.dsGraph.setXRange(0, 20)
        self.ui.dsGraph.setYRange(0, 500)
        self.ui.dsGraph.setLabel('left', 'Phase velocity', units='m/s')
        self.ui.dsGraph.setLabel('bottom', 'Frequency', units='Hz')
        #plot error barpy
        '''error = pg.ErrorBarItem(x=self.F, y=C, height=self., beam=0.1)
        self.ui.error = pg.ErrorBarItem(beam=0.5)
        # setting data to error bar item
        error.setData(x=self.F, y=C, top=C+C*self., bottom=C-C*self.)'''


        #--------------- Finding Parameter ------------#
        #Find first index that C < C2
        index = np.where(self.C[5:] < C2[5:])[0][0]
        index = int(index + np.round(0.1*index))
        #Find max Vs in C of range 0 to index
        self.maxC = np.max(self.C[5:index])
        self.minC = self.C[index]
        self.maxFreq = self.F[index]
        self.minFreq = self.F[np.argmax(self.C[5:index])]
        #Find index of max Vs in C
        maxC_index = np.where(self.C == self.maxC)[0][0]
        #Plot vertical line of max Vs and alias frequency and set alpha to 0.5
        self.minFreqAnal = self.ui.dsGraph.plot([self.F[maxC_index], self.F[maxC_index]], [0, self.ui.maxYDs.value()], pen='g', alpha=0.5)
        self.maxFreqAnal = self.ui.dsGraph.plot([self.F[index], self.F[index]], [0, self.ui.maxYDs.value()], pen='g', alpha=0.5)

        self.analFreq = np.ndarray.flatten((self.F[maxC_index: index]))
        self.analC = np.ndarray.flatten((self.C[maxC_index: index]))
        self.analstd = np.ndarray.flatten((self.std[maxC_index: index]))
        
        self.ui.dsGraph.setXRange(0, self.maxFreq+0.2*self.maxFreq)
        self.ui.minXanal.setMaximum(self.maxFreq+0.2*self.maxFreq)
        self.ui.maxXanal.setMaximum(self.maxFreq+0.2*self.maxFreq)
        
    def adjustRangeDs(self):
        self.ui.maxXDs.setMinimum(int(self.ui.minXDs.value()))
        maxY = int(self.ui.maxYDs.value())
        minX = int(self.ui.minXDs.value())
        maxX = int(self.ui.maxXDs.value())
        self.ui.minXanal.setMinimum(int(minX)*100)
        self.ui.minXanal.setMaximum(int(maxX)*100)
        self.ui.maxXanal.setMinimum(int(self.ui.minXanal.value())*100)
        self.ui.maxXanal.setMaximum(int(maxX)*100)
        #self.ui.minXanal.setValue(int(self.minFreq*100))
        #self.ui.maxXanal.setValue(int(self.maxFreq*100))
        self.ui.dsGraph.setYRange(0, maxY)
        self.ui.dsGraph.setXRange(minX, maxX)
        
    def adjustRangeAnal(self):
        self.ui.dsGraph.removeItem(self.minFreqAnal)
        self.ui.dsGraph.removeItem(self.maxFreqAnal)
        self.minFreqAnal = self.ui.dsGraph.plot([self.ui.minXanal.value()/100, self.ui.minXanal.value()/100], [0, self.ui.maxYDs.value()], pen='g', alpha=0.5)
        self.maxFreqAnal = self.ui.dsGraph.plot([self.ui.maxXanal.value()/100, self.ui.maxXanal.value()/100], [0, self.ui.maxYDs.value()], pen='g', alpha=0.5)
        self.minFreq = self.ui.minXanal.value()/100
        self.maxFreq = self.ui.maxXanal.value()/100
        
        self.ui.maxXanal.setMinimum(int(self.ui.minXanal.value())*100)
        
        
    #--------------------- Analyzation ----------------#
    def analFunction(self):
        # Finding index of min and max frequency
        FminIndex = np.argmin(np.abs(self.F - self.minFreq))
        FmaxIndex = np.argmin(np.abs(self.F - self.maxFreq))
        self.analFreq = self.F[FminIndex:FmaxIndex].flatten()
        self.analC = self.C[FminIndex:FmaxIndex].flatten()
        self.analstd = self.std[FminIndex:FmaxIndex].flatten()
        #check Target folder exist if not create
        if not os.path.exists('{}/Target/'.format(os.path.dirname(__file__))+self.ui.Station_in.text()):
            os.makedirs('{}/Target/'.format(os.path.dirname(__file__))+self.ui.Station_in.text())
        self.ui.tabWidget.setCurrentIndex(3)
        #set 2 decimal place
        self.ui.maxFreq.setText(str(self.maxFreq))
        self.ui.minFreq.setText(str(self.minFreq))
        self.ui.maxVel.setText("{0:.2f}".format(self.maxC))
        self.ui.minVel.setText("{0:.2f}".format(self.minC))

        print(len(self.analFreq))
        newFreq = np.linspace(self.analFreq[0], self.analFreq[-1], 20)
        newC = np.interp(newFreq, self.analFreq, self.analC)
        newStd = np.interp(newFreq, self.analFreq, self.analstd)

        tar = swprepost.Target(frequency=newFreq, velocity=newC, velstd=newStd)
        tar.to_target('{}/Target/'.format(os.path.dirname(__file__))+self.ui.Station_in.text()+'/'+self.ui.Station_in.text()+'_'+str(self.ui.id_Out.text()), version="3.4.2")
        
        minPseudoDepth = np.min(tar.pseudo_depth())
        self.minPsedoVs = np.min(tar.pseudo_vs())*0.8
        maxPsudoDepth = 2.5*minPseudoDepth
        self.maxPsedoVs = np.max(tar.pseudo_vs())

        self.ui.pseudoDepth.setText("{0:.2f}".format(maxPsudoDepth))
        self.ui.pseudoVs.setText("{0:.2f}".format(self.maxPsedoVs))
        print(self.minPsedoVs, minPseudoDepth, self.maxPsedoVs, maxPsudoDepth)

        self.nLayer = int(np.ceil(maxPsudoDepth))
        self.ui.nLayer.setText(str(self.nLayer))
        self.paraMethod = self.ui.Parametization.currentText()
        self.par_rev = self.ui.reverseLayer.isChecked()
        
    #--------------------- Inversion ----------------#

    def inversion(self):
            
        self.ui.analyzeStatus.setText("Status: Parameterizing")
        time.sleep(1)
        #Check Model folder exist if not create
        if not os.path.exists('{}/Model/'.format(os.path.dirname(__file__))+self.ui.Station_in.text()):
            os.makedirs('{}/Model/'.format(os.path.dirname(__file__))+self.ui.Station_in.text())

        #Check if Param  folder exist
        if not os.path.exists('{}/Param/'.format(os.path.dirname(__file__))+self.ui.Station_in.text()):
            os.makedirs('{}/Param/'.format(os.path.dirname(__file__))+self.ui.Station_in.text())

        #Construct parameter
        if self.paraMethod == "Fixed-Thickness Layer":
            param_vs = swprepost.Parameter.from_ftl(
                nlayers = self.nLayer,
                thickness = float(self.ui.thickness.text()),
                par_min = self.minPsedoVs,
                par_max = self.maxPsedoVs,
                par_rev = self.par_rev
            )
            param_vp = swprepost.Parameter.from_ftl(
                nlayers = self.nLayer,
                thickness = float(self.ui.thickness.text()),
                par_min = self.minPsedoVs*1.7,
                par_max = self.maxPsedoVs*1.7,
                par_rev = self.par_rev
            )
            param_rho = swprepost.Parameter.from_ftl(
                nlayers = self.nLayer,
                thickness = float(self.ui.thickness.text()),
                par_min = 1700,
                par_max = 2000,
                par_rev = self.par_rev
            )
            param_pr = swprepost.Parameter.from_ftl(
                nlayers = self.nLayer,
                thickness = float(self.ui.thickness.text()),
                par_min = 0.20,
                par_max = 0.30,
                par_rev = self.par_rev
            )
            param = swprepost.Parameterization(vp = param_vp, pr = param_pr, vs = param_vs, rh = param_rho)
            param.to_param('{}/Param/'.format(os.path.dirname(__file__))+self.ui.Station_in.text()+'/'+self.ui.Station_in.text()+'_'+str(self.ui.id_Out.text()), version="3.4.2")

        #Inversion
        paramFile = '{}/Param/'.format(os.path.dirname(__file__))+self.ui.Station_in.text()+'/'+self.ui.Station_in.text()+'_'+str(self.ui.id_Out.text())
        tarFile = '{}/Target/'.format(os.path.dirname(__file__))+self.ui.Station_in.text()+'/'+self.ui.Station_in.text()+'_'+str(self.ui.id_Out.text())
        modFile = '{}/Model/'.format(os.path.dirname(__file__))+self.ui.Station_in.text()+'/'+self.ui.Station_in.text()+'_'+str(self.ui.id_Out.text())
        self.ui.analyzeStatus.setText("Status: Inversion Process")

        '''try:
            subprocess.check_call(['./RunDinver.sh', paramFile, tarFile, self.ui.iteration.text(), modFile])
        except:
            os.system(f'cmd /c "RunDinver.bat {paramFile} {tarFile} {int(self.ui.iteration.text())} {modFile}"')'''

        self.thread = QThread()
        self.analWorker = analysisThread(paramFile, tarFile, self.ui.iteration.text(), modFile)
        self.analWorker.moveToThread(self.thread)
        self.thread.started.connect(self.analWorker.run)
        self.analWorker.finished.connect(self.onFinishAnal)
        self.thread.start()
        self.ui.analyzeStatus.setText("Status: Inversion Processing")

    def onFinishAnal(self):
        self.thread.quit()
        self.thread.wait()
        #Plot Inversion result
        fname = '{}/Model/'.format(os.path.dirname(__file__))+self.ui.Station_in.text()+'/'+self.ui.Station_in.text()+'_'+str(self.ui.id_Out.text() + '.txt')
        suite = swprepost.GroundModelSuite.from_geopsy(fname=fname, nmodels="all")
        median = suite.median(nbest=50)
        

        if not self.ui.Inplaced.isChecked():
            self.ui.VpProfile.clear()
            self.ui.VsProfile.clear()
            self.ui.densityProfile.clear()

        numColor = 15
        misfitRange = suite.misfit_range()
        misfits = suite.misfits
        #map colormap to misfit range
        c = np.arange(1, numColor + 1)

        norm = mpl.colors.Normalize(vmin=misfitRange[0], vmax=misfitRange[1])
        cmap = mpl.cm.ScalarMappable(norm=norm, cmap=mpl.cm.hot)
        cmap.set_array([])
        #reverse the color map
        #cmap to 0-255

        for idx, i in reversed(list(enumerate(misfits))):
            color = cmap.to_rgba(i)
            self.ui.VsProfile.plot(suite[idx].vs2, suite[idx].depth, pen=pg.mkPen(pg.mkColor(int(color[0]*255), int(color[1]*255), int(color[2]*255)), width=3))
            self.ui.VpProfile.plot(suite[idx].vp2, suite[idx].depth, pen=pg.mkPen(pg.mkColor(int(color[0]*255), int(color[1]*255), int(color[2]*255)), width=3))
            self.ui.densityProfile.plot(suite[idx].rh2, suite[idx].depth, pen=pg.mkPen(pg.mkColor(int(color[0]*255), int(color[1]*255), int(color[2]*255)), width=3))
        self.ui.VsProfile.setYRange(float(self.ui.pseudoDepth.text()), 0)
        self.ui.VsProfile.invertY(True)
        self.ui.VsProfile.showGrid(x=True, y=True)
        self.ui.VpProfile.setYRange(float(self.ui.pseudoDepth.text()), 0)
        self.ui.VpProfile.invertY(True)
        self.ui.VpProfile.showGrid(x=True, y=True)
        self.ui.densityProfile.setYRange(float(self.ui.pseudoDepth.text()), 0)
        self.ui.densityProfile.invertY(True)
        self.ui.densityProfile.showGrid(x=True, y=True)
        
        self.ui.VsProfile_2.plot(median.vs2, median.depth, pen='r', linewidth=2)
        self.ui.VsProfile_2.setYRange(float(self.ui.pseudoDepth.text()), 0)
        self.ui.VsProfile_2.invertY(True)
        self.ui.VsProfile_2.showGrid(x=True, y=True)

        self.ui.VpProfile_2.plot(median.vp2, median.depth, pen='r', linewidth=2)
        self.ui.VpProfile_2.setYRange(float(self.ui.pseudoDepth.text()), 0)
        self.ui.VpProfile_2.invertY(True)
        self.ui.VpProfile_2.showGrid(x=True, y=True)

        self.ui.densityProfile_2.plot(median.rh2, median.depth, pen='r', linewidth=2)
        self.ui.densityProfile_2.setYRange(float(self.ui.pseudoDepth.text()), 0)
        self.ui.densityProfile_2.invertY(True)
        self.ui.densityProfile_2.showGrid(x=True, y=True)

        self.ui.analyzeStatus.setText("Status: Done")
        self.ui.analyzeStatus_2.setText(f"Misfit: {np.min(suite.misfits):.4f}")
        

class NewProject_dialog(QDialog):
    def __init__(self, parent=None):
        super(NewProject_dialog, self).__init__(parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

    def getName(self):
        if self.exec_() == QDialog.Accepted:
            return self.ui.projectName.text()
        else:
            return ""


if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    myapp = MyApp()
    myapp.show()
    sys.exit(app.exec_())

# New comment for testing

