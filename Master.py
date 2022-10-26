#import Pyqt5 modules
from multiprocessing import Event
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot
#import window.py class
from window import Ui_MainWindow
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
        #set font size in pyqtplot
        self.ui.Wave1.setLabel('left', 'Voltage', units='V')
        self.ui.Wave1.setLabel('bottom', 'Time', units='s')
        self.ui.Wave2.setBackground('w')
        self.ui.Wave3.setBackground('w')
        #Initialize Input text box
        self.ui.Station_in.setText('BH-1')
        self.ui.Lat_in.setText('0')
        self.ui.Long_in.setText('0')
        self.ui.Radius_in.setText('3')
        #Set callback lable (Text, Combobox etc. here)
        self.ui.StartButton.clicked.connect(self.UpdateConfig)
        #check folder Storage exist or not if not create it
        if not os.path.exists('Storage'):
            os.makedirs('Storage')
        storagePath = os.path.join(os.getcwd(), 'Storage')

    def UpdateConfig(self):
        self.Station = self.ui.Station_in.text()
        self.Lat     = self.ui.Lat_in.text()
        self.Long    = self.ui.Long_in.text()
        self.Radius  = self.ui.Radius_in.text()
        print("Station :", self.Station)
        print("Location : Lat ", self.Lat, "Long ", self.Long)
        print("Array radius : ",self.Radius," m")

        
        
        
    



if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    myapp = MyApp()
    myapp.show()
    sys.exit(app.exec_())

# New comment for testing

