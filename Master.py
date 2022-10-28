#import Pyqt5 modules
from multiprocessing import Event
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QDialog, QInputDialog, QDialogButtonBox, QTableWidgetItem
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
            '1 hour' : 3600,
            '2 hour' : 7200,
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
        #check folder Storage exist or not if not create it
        if not os.path.exists('Storage'):
            os.makedirs('Storage')
        '''if not os.path.exists('Header'):
            os.makedirs('Header')'''
        self.storagePath = os.path.join(os.getcwd(), 'Storage')

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
            self.ui.ID_in.setEnabled(True)
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
                with open('Storage/'+self.Station+'/'+self.Station+'.json', 'w') as f:
                    json.dump([], f, indent=4)

    def getfile(self):
        fname = QFileDialog.getOpenFileName(self, "Import json", "./Storage/", "JSON Files (*.json)")[0]
        self.ui.Station_in.setText(fname.split('/')[-1].split('.')[0])
        if fname != '':
            self.ui.Lat_in.setEnabled(True)
            self.ui.Long_in.setEnabled(True)
            self.ui.Radius_in.setEnabled(True)
            self.ui.StartButton.setEnabled(True)
            self.ui.Duration_in.setEnabled(True)
            self.ui.ID_in.setEnabled(True)
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

        
        
        
    #--------------- Start Recording -----------------#
    #-------------------------------------------------#
    def saveConfigJson(self, Station, id, Lat, Long, Radius, Duration, Sample):
        with open('Storage/'+Station+'/'+Station+'.json') as f:
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
    
        with open('Storage/'+self.Station+'/'+self.Station+'.json', 'w') as outfile:
            json.dump(data, outfile, indent=4)
        print("Save Config")
    #-------------------------------------------------#

    #--------------- Start Recording -----------------#
    #-------------------------------------------------#
    def startFunction(self):
        self.UpdateConfig()
        self.saveConfigJson(self.Station, 0, float(self.Lat), float(self.Long), float(self.Radius), float(self.timeDuration[self.ui.Duration_in.currentText()]), float(self.ui.Sample.text()))
        print("Start Function")

    #--------------- Stop Recording ------------------#

    def dsPlot(self):
        self.ui.tabWidget.setCurrentIndex(2)

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

