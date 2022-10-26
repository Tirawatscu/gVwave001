#import Pyqt5 modules
from multiprocessing import Event
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QDialog, QInputDialog, QDialogButtonBox
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot
#import window.py class
from window import Ui_MainWindow
from projectDialog import Ui_Dialog
import json
#import other modules
import os
import sys
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
        self.ui.menuFile.triggered.connect(self.menuFile)
        self.timeDuration = {
            '30 s' : 30,
            '1 min' : 60,
            '2 min' : 120,
            '5 min' : 300,
            '10 min' : 600,
            '15 min' : 900,
            '30 min' : 1800,
            '1 hour' : 3600,
            '2 hour' : 7200,
        }


        #set font size in pyqtplot
        self.ui.Wave1.setLabel('left', 'Voltage', units='V')
        self.ui.Wave1.setLabel('bottom', 'Time', units='s')
        self.ui.Wave2.setBackground('w')
        self.ui.Wave3.setBackground('w')
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
        self.ui.Sample.setEnabled(False)
        #Set callback lable (Text, Combobox etc. here)
        self.ui.Duration_in.currentTextChanged.connect(self.updateSample)
        self.ui.StartButton.clicked.connect(self.startFunction)
        #check folder Storage exist or not if not create it
        if not os.path.exists('Storage'):
            os.makedirs('Storage')
        '''if not os.path.exists('Header'):
            os.makedirs('Header')'''
        storagePath = os.path.join(os.getcwd(), 'Storage')
        headerPath = os.path.join(os.getcwd(), 'Header')

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
            self.saveConfigState = True
        else:
            self.ui.Lat_in.setEnabled(False)
            self.ui.Long_in.setEnabled(False)
            self.ui.Radius_in.setEnabled(False)
            self.ui.StartButton.setEnabled(False)
            self.ui.Duration_in.setEnabled(False)
            self.saveConfigState = False
        if self.saveConfigState:
            if not os.path.exists('Storage/'+self.Station):
                os.makedirs('Storage/'+self.Station)
                #make self.Station.json file in directory Storage/+self.Station
                with open('Storage/'+self.Station+'/'+self.Station+'.json', 'w') as f:
                    json.dump([], f, indent=4)

    def saveConfigJson(self, Station, id, Lat, Long, Radius, Duration, Sample):
        with open('Storage/'+Station+'/'+Station+'.json') as f:
            data = json.load(f)
            save = {
            'Station' : Station,
            'id' : len(data),
            'Lat' : Lat,
            'Long' : Long,
            'Radius' : Radius,
            'Duration' : Duration,
            'Sample' : Sample,
        }
            data.append(save)
    
        with open('Storage/'+self.Station+'/'+self.Station+'.json', 'w') as outfile:
            json.dump(data, outfile, indent=4)
        print("Save Config")

    #--------------- Start Recording -----------------#
    #-------------------------------------------------#
    def startFunction(self):
        self.UpdateConfig()
        self.saveConfigJson(self.Station, 0, self.Lat, self.Long, self.Radius, self.ui.Duration_in.currentText(), self.ui.Sample.text())
        print("Start Function")

    #--------------- Stop Recording ------------------#

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

