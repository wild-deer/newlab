# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'TL_UI.ui'
#
# Created by: PyQt5 UI code generator 5.15.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1920, 1080)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label_show_camera = QtWidgets.QLabel(self.centralwidget)
        self.label_show_camera.setGeometry(QtCore.QRect(190, 160, 1080, 720))
        self.label_show_camera.setStyleSheet("")
        self.label_show_camera.setText("")
        self.label_show_camera.setObjectName("label_show_camera")
        self.start_btn = QtWidgets.QPushButton(self.centralwidget)
        self.start_btn.setGeometry(QtCore.QRect(1440, 900, 131, 61))
        self.start_btn.setStyleSheet("font: 18pt \"Abaddon™\";")
        self.start_btn.setObjectName("start_btn")
        self.stop_btn = QtWidgets.QPushButton(self.centralwidget)
        self.stop_btn.setGeometry(QtCore.QRect(1670, 900, 131, 61))
        self.stop_btn.setStyleSheet("font: 18pt \"Abaddon™\";")
        self.stop_btn.setObjectName("stop_btn")
        self.red_time = QtWidgets.QTextBrowser(self.centralwidget)
        self.red_time.setGeometry(QtCore.QRect(1570, 250, 191, 101))
        self.red_time.setObjectName("red_time")
        self.yellow_time = QtWidgets.QTextBrowser(self.centralwidget)
        self.yellow_time.setGeometry(QtCore.QRect(1570, 420, 191, 101))
        self.yellow_time.setObjectName("yellow_time")
        self.green_time = QtWidgets.QTextBrowser(self.centralwidget)
        self.green_time.setGeometry(QtCore.QRect(1570, 590, 191, 101))
        self.green_time.setObjectName("green_time")
        self.r_title = QtWidgets.QLabel(self.centralwidget)
        self.r_title.setGeometry(QtCore.QRect(1470, 280, 61, 41))
        self.r_title.setStyleSheet("font: 18pt \"Abaddon™\";")
        self.r_title.setObjectName("r_title")
        self.y_title = QtWidgets.QLabel(self.centralwidget)
        self.y_title.setGeometry(QtCore.QRect(1470, 450, 61, 41))
        self.y_title.setStyleSheet("font: 18pt \"Abaddon™\";")
        self.y_title.setObjectName("y_title")
        self.g_title = QtWidgets.QLabel(self.centralwidget)
        self.g_title.setGeometry(QtCore.QRect(1470, 610, 61, 41))
        self.g_title.setStyleSheet("\n""font: 18pt \"Abaddon™\";")
        self.g_title.setObjectName("g_title")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(650, 30, 581, 81))
        self.label.setStyleSheet("font: 48pt \"Abaddon™\";")
        self.label.setObjectName("label")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1920, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.start_btn.setText(_translate("MainWindow", "ON"))
        self.stop_btn.setText(_translate("MainWindow", "OFF"))
        self.r_title.setText(_translate("MainWindow", "X路红灯"))
        self.y_title.setText(_translate("MainWindow", "黄灯"))
        self.g_title.setText(_translate("MainWindow", "Y路红灯"))
        self.label.setText(_translate("MainWindow", "智慧交通信号灯"))
