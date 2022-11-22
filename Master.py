#import Pyqt5 modules
from multiprocessing import Event
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QDialog, QInputDialog, QDialogButtonBox, QTableWidgetItem
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot
#import window.py class
from window import Ui_MainWindow
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
import subprocess
import time
import threading
import shutil
import re
import datetime
import csv

class MyApp(QMainWindow):
    def __init__(self, parent=None):
        super(MyApp, self).__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
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
        self.ui.Wave3.setBackground('w')
        self.ui.tableWidget.setColumnCount(1)
        self.ui.tableWidget.setColumnWidth(0, 250)
        self.ui.tableWidget.cellClicked.connect(self.rowSelected)
        self.ui.dsPlot.clicked.connect(self.dsPlot)
        #Initialize Input text box
        self.ui.Station_in.setText('Location')
        self.ui.Lat_in.setText('0')
        self.ui.Long_in.setText('0')
        self.ui.Radius_in.setText('3')
        self.ui.Sample.setText(str(self.timeDuration[self.ui.Duration_in.currentText()]*256))
        #Disable all buttons and input text box
        self.ui.Station_in.setEnabled(False)
        self.ui.Lat_in.setEnabled(False)
        self.ui.Long_in.setEnabled(False)
        self.ui.Radius_in.setEnabled(False)
        self.ui.StartButton.setEnabled(False)
        self.ui.Duration_in.setEnabled(False)
        self.ui.ID_in.setEnabled(False)
        self.ui.Sample.setEnabled(False)
        #Set callback lable (Text, Combobox etc. here)
        self.ui.Duration_in.currentTextChanged.connect(self.updateSample)
        self.ui.StartButton.clicked.connect(self.startFunction)
        self.ui.PrevLogger.clicked.connect(self.prevLogger)
        self.ui.Analyse.clicked.connect(self.analFunction)
        self.ui.Analyzing.clicked.connect(self.inversion)

        self.ui.VsProfile.setLabel('bottom', 'Shear wave velocity', units='m/s')
        self.ui.VsProfile.setLabel('left', 'Depth', units='m')
        self.ui.VpProfile.setLabel('bottom', 'Compression wave velocity', units='m/s')
        self.ui.VpProfile.setLabel('left', 'Depth', units='m')
        self.ui.densityProfile.setLabel('bottom', 'Density', units='kg/m3')
        self.ui.densityProfile.setLabel('left', 'Depth', units='m')
        self.ui.nLayer.setText('3')
        self.ui.thickness.setText('1')
        self.ui.iteration.setText('10000')
        self.ui.lr.setEnabled(False)
        self.ui.dF.setEnabled(False)
        self.ui.reverseLayer.setChecked(True)

        #check folder Storage exist or not if not create it
        if not os.path.exists('Storage'):
            os.makedirs('Storage')
        if not os.path.exists('Workspace'):
            os.makedirs('Workspace')
        '''if not os.path.exists('Header'):
            os.makedirs('Header')'''
        self.storagePath = os.path.join(os.getcwd(), 'Storage')
        self.workspacePath = os.path.join(os.getcwd(), 'Workspace')

    def prevLogger(self):
        self.ui.tabWidget.setCurrentIndex(1)


    def updateSample(self):
        self.ui.Sample.setText(str(self.timeDuration[self.ui.Duration_in.currentText()]*256))

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
            if not os.path.exists('Storage/'+self.Station):
                os.makedirs('Storage/'+self.Station)
                with open('Workspace/'+self.Station+'.json', 'w') as f:
                    json.dump([], f, indent=4)
                self.ui.ID_in.setText('000')

    def getfile(self):
        fname = QFileDialog.getOpenFileName(self, "Import json", "./Workspace/", "JSON Files (*.json)")[0]
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
            self.Freq = 256
            self.time = np.arange(0, int(len(self.df)/self.Freq), 1/self.Freq)
            self.ui.Wave1_2.clear()
            self.ui.Wave1_2.plot(self.time, self.df['Ch 1'], pen='r')
            self.ui.Wave1_3.clear()
            self.ui.Wave1_3.plot(self.time, self.df['Ch 2'], pen='g')
            self.ui.Wave1_4.clear()
            self.ui.Wave1_4.plot(self.time, self.df['Ch 3'], pen='b')
        else:
            self.ui.dsPlot.setEnabled(False)
            self.ui.Wave1_2.clear()
            self.ui.Wave1_3.clear()
            self.ui.Wave1_4.clear()



        
        
        
    #------------- Save Configuration ----------------#
    #-------------------------------------------------#
    def saveConfigJson(self, Station, id, Lat, Long, Radius, Duration, Sample):
        with open('Workspace/'+Station+'.json') as f:
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
    
        with open('Workspace/'+self.Station+'.json', 'w') as outfile:
            json.dump(data, outfile, indent=4)
        print("Save Config")
    #-------------------------------------------------#

    #--------------- Start Recording -----------------#
    #-------------------------------------------------#
    def startFunction(self):
        self.UpdateConfig()
        self.saveConfigJson(self.Station, 0, float(self.Lat), float(self.Long), float(self.Radius), float(self.timeDuration[self.ui.Duration_in.currentText()]), float(self.ui.Sample.text()))
        print("Start Function")
        self.ui.Lat_in.setEnabled(False)
        self.ui.Long_in.setEnabled(False)
        self.ui.Radius_in.setEnabled(False)
        self.ui.StartButton.setEnabled(False)
        self.ui.Duration_in.setEnabled(False)
        self.ui.ID_in.setEnabled(False)


    #--------------- After Recording ----------------#
        self.ui.tableWidget.clear()
        self.ui.tableWidget.setHorizontalHeaderLabels(['Event'])
        # Load json file
        with open('Workspace/'+self.Station+'.json', 'r') as f:
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

    #--------------- Stop Recording ------------------#

    def dsPlot(self):
        self.ui.tabWidget.setCurrentIndex(2)
        self.ui.dsGraph.clear()

        data = np.array([self.df["Ch 1"],self.df["Ch 2"], self.df["Ch 3"]]).T
        pop1 = POP(data, [], [], float(self.ui.rad_Out.text()), self.Freq, 2048)
        [F, C, C2, std] = pop1.makepop()
        #replace NAN with 0
        C[np.isnan(C)] = 0
        self.ui.dsGraph.plot(F, C, pen='r')
        self.ui.dsGraph.plot(F, C2, pen='b')
        self.ui.dsGraph.setXRange(0, 20)
        self.ui.dsGraph.setYRange(0, 500)
        self.ui.dsGraph.setLabel('left', 'Phase velocity', units='m/s')
        self.ui.dsGraph.setLabel('bottom', 'Frequency', units='Hz')
        #plot error barpy
        '''error = pg.ErrorBarItem(x=F, y=C, height=std, beam=0.1)
        self.ui.error = pg.ErrorBarItem(beam=0.5)
        # setting data to error bar item
        error.setData(x=F, y=C, top=C+C*std, bottom=C-C*std)'''


        #--------------- Finding Parameter ------------#
        #Find first index that C < C2
        index = np.where(C[5:] < C2[5:])[0][0]
        index = int(index + np.round(0.1*index))
        #Find max Vs in C of range 0 to index
        self.maxC = np.max(C[5:index])
        self.minC = C[index]
        self.maxFreq = F[index]
        self.minFreq = F[np.argmax(C[5:index])]
        #Find index of max Vs in C
        maxC_index = np.where(C == self.maxC)[0][0]
        #Plot vertical line of max Vs and alias frequency and set alpha to 0.5
        self.ui.dsGraph.plot([F[maxC_index], F[maxC_index]], [0, 500], pen='g', alpha=0.5)
        self.ui.dsGraph.plot([F[index], F[index]], [0, 500], pen='g', alpha=0.5)

        self.analFreq = np.ndarray.flatten((F[maxC_index: index]))
        self.analC = np.ndarray.flatten((C[maxC_index: index]))
        self.std = np.ndarray.flatten((std[maxC_index: index]))

        self.ui.dsGraph.setXRange(0, self.maxFreq+0.2*self.maxFreq)

    #--------------------- Analyzation ----------------#
    def analFunction(self):
        #check Target folder exist if not create
        if not os.path.exists('Target/'+self.ui.Station_in.text()):
            os.makedirs('Target/'+self.ui.Station_in.text())
        self.ui.tabWidget.setCurrentIndex(3)
        self.ui.VpProfile.clear()
        self.ui.VsProfile.clear()
        self.ui.densityProfile.clear()
        #set 2 decimal place
        self.ui.maxFreq.setText(str(self.maxFreq))
        self.ui.minFreq.setText(str(self.minFreq))
        self.ui.maxVel.setText("{0:.2f}".format(self.maxC))
        self.ui.minVel.setText("{0:.2f}".format(self.minC))

        print(len(self.analFreq))
        newFreq = np.linspace(self.analFreq[0], self.analFreq[-1], 20)
        newC = np.interp(newFreq, self.analFreq, self.analC)
        newStd = np.interp(newFreq, self.analFreq, self.std)

        tar = swprepost.Target(frequency=newFreq, velocity=newC, velstd=newStd)
        tar.to_target('Target/'+self.ui.Station_in.text()+'/'+self.ui.Station_in.text()+'_'+str(self.ui.id_Out.text()), version="3.4.2")
        
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
        
        #Check Model folder exist if not create
        if not os.path.exists('Model/'+self.ui.Station_in.text()):
            os.makedirs('Model/'+self.ui.Station_in.text())

        #Check if Param  folder exist
        if not os.path.exists('Param/'+self.ui.Station_in.text()):
            os.makedirs('Param/'+self.ui.Station_in.text())

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
            param.to_param('Param/'+self.ui.Station_in.text()+'/'+self.ui.Station_in.text()+'_'+str(self.ui.id_Out.text()), version="3.4.2")

        #Inversion
        paramFile = 'Param/'+self.ui.Station_in.text()+'/'+self.ui.Station_in.text()+'_'+str(self.ui.id_Out.text())
        tarFile = 'Target/'+self.ui.Station_in.text()+'/'+self.ui.Station_in.text()+'_'+str(self.ui.id_Out.text())
        modFile = 'Model/'+self.ui.Station_in.text()+'/'+self.ui.Station_in.text()+'_'+str(self.ui.id_Out.text())
        os.system(f'cmd /c "RunDinver.bat {paramFile} {tarFile} {int(self.ui.iteration.text())} {modFile}"')
        
        

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

