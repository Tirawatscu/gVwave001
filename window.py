# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'untitled.ui'
#
# Created by: PyQt5 UI code generator 5.15.7
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(872, 570)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setGeometry(QtCore.QRect(-1, -1, 871, 531))
        self.tabWidget.setTabPosition(QtWidgets.QTabWidget.West)
        self.tabWidget.setDocumentMode(True)
        self.tabWidget.setTabBarAutoHide(True)
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.groupBox = QtWidgets.QGroupBox(self.tab)
        self.groupBox.setGeometry(QtCore.QRect(30, 20, 291, 131))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.groupBox.setFont(font)
        self.groupBox.setFlat(False)
        self.groupBox.setCheckable(False)
        self.groupBox.setObjectName("groupBox")
        self.label = QtWidgets.QLabel(self.groupBox)
        self.label.setGeometry(QtCore.QRect(20, 40, 60, 16))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.groupBox)
        self.label_2.setGeometry(QtCore.QRect(20, 70, 60, 16))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.groupBox)
        self.label_3.setGeometry(QtCore.QRect(20, 100, 60, 16))
        self.label_3.setObjectName("label_3")
        self.Station_in = QtWidgets.QLineEdit(self.groupBox)
        self.Station_in.setGeometry(QtCore.QRect(100, 30, 161, 31))
        self.Station_in.setObjectName("Station_in")
        self.Lat_in = QtWidgets.QLineEdit(self.groupBox)
        self.Lat_in.setGeometry(QtCore.QRect(100, 60, 161, 31))
        self.Lat_in.setObjectName("Lat_in")
        self.Long_in = QtWidgets.QLineEdit(self.groupBox)
        self.Long_in.setGeometry(QtCore.QRect(100, 90, 161, 31))
        self.Long_in.setObjectName("Long_in")
        self.groupBox_2 = QtWidgets.QGroupBox(self.tab)
        self.groupBox_2.setGeometry(QtCore.QRect(30, 160, 291, 151))
        self.groupBox_2.setObjectName("groupBox_2")
        self.Duration_in = QtWidgets.QComboBox(self.groupBox_2)
        self.Duration_in.setGeometry(QtCore.QRect(140, 30, 131, 31))
        self.Duration_in.setObjectName("Duration_in")
        self.Duration_in.addItem("")
        self.Duration_in.addItem("")
        self.Duration_in.addItem("")
        self.Duration_in.addItem("")
        self.Duration_in.addItem("")
        self.Duration_in.addItem("")
        self.Duration_in.addItem("")
        self.Duration_in.addItem("")
        self.Duration_in.addItem("")
        self.Duration_in.addItem("")
        self.label_4 = QtWidgets.QLabel(self.groupBox_2)
        self.label_4.setGeometry(QtCore.QRect(10, 35, 101, 21))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(self.groupBox_2)
        self.label_5.setGeometry(QtCore.QRect(20, 110, 101, 30))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.label_5.setFont(font)
        self.label_5.setObjectName("label_5")
        self.Radius_in = QtWidgets.QLineEdit(self.groupBox_2)
        self.Radius_in.setGeometry(QtCore.QRect(140, 110, 131, 31))
        self.Radius_in.setText("")
        self.Radius_in.setPlaceholderText("")
        self.Radius_in.setObjectName("Radius_in")
        self.label_6 = QtWidgets.QLabel(self.groupBox_2)
        self.label_6.setGeometry(QtCore.QRect(40, 70, 71, 30))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.label_6.setFont(font)
        self.label_6.setObjectName("label_6")
        self.Sample = QtWidgets.QLineEdit(self.groupBox_2)
        self.Sample.setGeometry(QtCore.QRect(140, 70, 131, 31))
        self.Sample.setText("")
        self.Sample.setPlaceholderText("")
        self.Sample.setObjectName("Sample")
        self.groupBox_3 = QtWidgets.QGroupBox(self.tab)
        self.groupBox_3.setGeometry(QtCore.QRect(340, 20, 481, 501))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.groupBox_3.setFont(font)
        self.groupBox_3.setObjectName("groupBox_3")
        self.RunButton = QtWidgets.QPushButton(self.groupBox_3)
        self.RunButton.setGeometry(QtCore.QRect(20, 30, 111, 51))
        self.RunButton.setObjectName("RunButton")
        self.Wave1 = PlotWidget(self.groupBox_3)
        self.Wave1.setGeometry(QtCore.QRect(20, 80, 441, 121))
        self.Wave1.setObjectName("Wave1")
        self.Wave2 = PlotWidget(self.groupBox_3)
        self.Wave2.setGeometry(QtCore.QRect(20, 220, 441, 121))
        self.Wave2.setObjectName("Wave2")
        self.Wave3 = PlotWidget(self.groupBox_3)
        self.Wave3.setGeometry(QtCore.QRect(20, 360, 441, 121))
        self.Wave3.setObjectName("Wave3")
        self.StartButton = QtWidgets.QPushButton(self.tab)
        self.StartButton.setGeometry(QtCore.QRect(30, 470, 291, 51))
        self.StartButton.setObjectName("StartButton")
        self.tabWidget.addTab(self.tab, "")
        self.Logger = QtWidgets.QWidget()
        self.Logger.setObjectName("Logger")
        self.tableWidget = QtWidgets.QTableWidget(self.Logger)
        self.tableWidget.setGeometry(QtCore.QRect(0, 40, 171, 441))
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)
        self.groupBox_4 = QtWidgets.QGroupBox(self.Logger)
        self.groupBox_4.setGeometry(QtCore.QRect(190, 20, 631, 61))
        self.groupBox_4.setObjectName("groupBox_4")
        self.label_8 = QtWidgets.QLabel(self.groupBox_4)
        self.label_8.setGeometry(QtCore.QRect(10, 30, 51, 16))
        self.label_8.setObjectName("label_8")
        self.line = QtWidgets.QFrame(self.groupBox_4)
        self.line.setGeometry(QtCore.QRect(110, 20, 20, 31))
        self.line.setFrameShape(QtWidgets.QFrame.VLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.label_9 = QtWidgets.QLabel(self.groupBox_4)
        self.label_9.setGeometry(QtCore.QRect(130, 30, 21, 16))
        self.label_9.setObjectName("label_9")
        self.label_10 = QtWidgets.QLabel(self.groupBox_4)
        self.label_10.setGeometry(QtCore.QRect(220, 30, 31, 16))
        self.label_10.setObjectName("label_10")
        self.line_2 = QtWidgets.QFrame(self.groupBox_4)
        self.line_2.setGeometry(QtCore.QRect(320, 20, 20, 31))
        self.line_2.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.label_11 = QtWidgets.QLabel(self.groupBox_4)
        self.label_11.setGeometry(QtCore.QRect(340, 30, 31, 16))
        self.label_11.setObjectName("label_11")
        self.line_3 = QtWidgets.QFrame(self.groupBox_4)
        self.line_3.setGeometry(QtCore.QRect(440, 20, 20, 31))
        self.line_3.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_3.setObjectName("line_3")
        self.label_12 = QtWidgets.QLabel(self.groupBox_4)
        self.label_12.setGeometry(QtCore.QRect(460, 30, 51, 16))
        self.label_12.setObjectName("label_12")
        self.groupBox_5 = QtWidgets.QGroupBox(self.Logger)
        self.groupBox_5.setGeometry(QtCore.QRect(190, 90, 631, 431))
        self.groupBox_5.setObjectName("groupBox_5")
        self.Wave1_2 = PlotWidget(self.groupBox_5)
        self.Wave1_2.setGeometry(QtCore.QRect(10, 40, 601, 121))
        self.Wave1_2.setObjectName("Wave1_2")
        self.Wave1_3 = PlotWidget(self.groupBox_5)
        self.Wave1_3.setGeometry(QtCore.QRect(10, 170, 601, 121))
        self.Wave1_3.setObjectName("Wave1_3")
        self.Wave1_4 = PlotWidget(self.groupBox_5)
        self.Wave1_4.setGeometry(QtCore.QRect(10, 300, 601, 121))
        self.Wave1_4.setObjectName("Wave1_4")
        self.pushButton_3 = QtWidgets.QPushButton(self.Logger)
        self.pushButton_3.setGeometry(QtCore.QRect(0, 481, 171, 41))
        self.pushButton_3.setObjectName("pushButton_3")
        self.tabWidget.addTab(self.Logger, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.tabWidget.addTab(self.tab_2, "")
        self.tab_3 = QtWidgets.QWidget()
        self.tab_3.setObjectName("tab_3")
        self.pushButton_4 = QtWidgets.QPushButton(self.tab_3)
        self.pushButton_4.setGeometry(QtCore.QRect(670, 470, 161, 51))
        self.pushButton_4.setObjectName("pushButton_4")
        self.tabWidget.addTab(self.tab_3, "")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 872, 24))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuAbout = QtWidgets.QMenu(self.menubar)
        self.menuAbout.setObjectName("menuAbout")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionNew_Workspace = QtWidgets.QAction(MainWindow)
        self.actionNew_Workspace.setObjectName("actionNew_Workspace")
        self.actionOpen = QtWidgets.QAction(MainWindow)
        self.actionOpen.setObjectName("actionOpen")
        self.menuFile.addAction(self.actionNew_Workspace)
        self.menuFile.addAction(self.actionOpen)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuAbout.menuAction())

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.groupBox.setTitle(_translate("MainWindow", "Location"))
        self.label.setText(_translate("MainWindow", "Station"))
        self.label_2.setText(_translate("MainWindow", "Lat"))
        self.label_3.setText(_translate("MainWindow", "Long"))
        self.groupBox_2.setTitle(_translate("MainWindow", "GroupBox"))
        self.Duration_in.setItemText(0, _translate("MainWindow", "30 s"))
        self.Duration_in.setItemText(1, _translate("MainWindow", "1 min"))
        self.Duration_in.setItemText(2, _translate("MainWindow", "2 min"))
        self.Duration_in.setItemText(3, _translate("MainWindow", "5 min"))
        self.Duration_in.setItemText(4, _translate("MainWindow", "10 min"))
        self.Duration_in.setItemText(5, _translate("MainWindow", "15 min"))
        self.Duration_in.setItemText(6, _translate("MainWindow", "20 min"))
        self.Duration_in.setItemText(7, _translate("MainWindow", "30 min"))
        self.Duration_in.setItemText(8, _translate("MainWindow", "1 hr"))
        self.Duration_in.setItemText(9, _translate("MainWindow", "2 hr"))
        self.label_4.setText(_translate("MainWindow", "Time Duration"))
        self.label_5.setText(_translate("MainWindow", "Array Radius"))
        self.label_6.setText(_translate("MainWindow", "Samples"))
        self.groupBox_3.setTitle(_translate("MainWindow", "Test Panel"))
        self.RunButton.setText(_translate("MainWindow", "Run Test"))
        self.StartButton.setText(_translate("MainWindow", "Start"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("MainWindow", "Configuration"))
        self.groupBox_4.setTitle(_translate("MainWindow", "GroupBox"))
        self.label_8.setText(_translate("MainWindow", "Station"))
        self.label_9.setText(_translate("MainWindow", "Lat"))
        self.label_10.setText(_translate("MainWindow", "Long"))
        self.label_11.setText(_translate("MainWindow", "Rad."))
        self.label_12.setText(_translate("MainWindow", "Sample"))
        self.groupBox_5.setTitle(_translate("MainWindow", "GroupBox"))
        self.pushButton_3.setText(_translate("MainWindow", "Plot Dispersion Curve"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.Logger), _translate("MainWindow", "Logger"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("MainWindow", "DC Plot"))
        self.pushButton_4.setText(_translate("MainWindow", "Generate Report"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), _translate("MainWindow", "Soil Profile"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.menuAbout.setTitle(_translate("MainWindow", "About"))
        self.actionNew_Workspace.setText(_translate("MainWindow", "New workspace"))
        self.actionOpen.setText(_translate("MainWindow", "Import project"))
from pyqtgraph import PlotWidget


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
