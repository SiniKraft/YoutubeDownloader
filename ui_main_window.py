# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main_windowFkhjff.ui'
##
## Created by: Qt User Interface Compiler version 5.15.5
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *  # type: ignore
from PySide2.QtGui import *  # type: ignore
from PySide2.QtWidgets import *  # type: ignore

import logo_rc

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(700, 730)
        MainWindow.setMinimumSize(QSize(700, 730))
        MainWindow.setMaximumSize(QSize(700, 730))
        self.actionChange_Downloads_Location = QAction(MainWindow)
        self.actionChange_Downloads_Location.setObjectName(u"actionChange_Downloads_Location")
        self.actionAbout = QAction(MainWindow)
        self.actionAbout.setObjectName(u"actionAbout")
        self.actionExit = QAction(MainWindow)
        self.actionExit.setObjectName(u"actionExit")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.listWidget = QListWidget(self.centralwidget)
        self.listWidget.setObjectName(u"listWidget")
        self.listWidget.setEnabled(False)
        self.listWidget.setGeometry(QRect(30, 500, 311, 151))
        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(130, 30, 641, 141))
        font = QFont()
        font.setFamily(u"Segoe UI")
        font.setPointSize(42)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label_2 = QLabel(self.centralwidget)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(300, 120, 211, 41))
        font1 = QFont()
        font1.setPointSize(24)
        self.label_2.setFont(font1)
        self.label_3 = QLabel(self.centralwidget)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setGeometry(QRect(30, 220, 631, 16))
        font2 = QFont()
        font2.setPointSize(14)
        self.label_3.setFont(font2)
        self.checkBox = QCheckBox(self.centralwidget)
        self.checkBox.setObjectName(u"checkBox")
        self.checkBox.setEnabled(True)
        self.checkBox.setGeometry(QRect(30, 410, 181, 17))
        font3 = QFont()
        font3.setPointSize(12)
        self.checkBox.setFont(font3)
        self.checkBox.setCursor(QCursor(Qt.ArrowCursor))
        self.checkBox.setAcceptDrops(False)
        self.checkBox.setAutoFillBackground(False)
        self.checkBox.setChecked(True)
        self.checkBox.setTristate(False)
        self.listWidget_2 = QListWidget(self.centralwidget)
        self.listWidget_2.setObjectName(u"listWidget_2")
        self.listWidget_2.setEnabled(False)
        self.listWidget_2.setGeometry(QRect(350, 500, 311, 151))
        self.checkBox_2 = QCheckBox(self.centralwidget)
        self.checkBox_2.setObjectName(u"checkBox_2")
        self.checkBox_2.setGeometry(QRect(360, 410, 181, 17))
        self.checkBox_2.setFont(font3)
        self.checkBox_2.setChecked(True)
        self.commandLinkButton = QCommandLinkButton(self.centralwidget)
        self.commandLinkButton.setObjectName(u"commandLinkButton")
        self.commandLinkButton.setEnabled(False)
        self.commandLinkButton.setGeometry(QRect(270, 660, 141, 51))
        font4 = QFont()
        font4.setFamily(u"Segoe UI")
        font4.setPointSize(14)
        self.commandLinkButton.setFont(font4)
        self.commandLinkButton.setDefault(False)
        self.label_6 = QLabel(self.centralwidget)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setGeometry(QRect(0, 40, 131, 131))
        self.label_6.setPixmap(QPixmap(u":/img/youtube_play1600.png"))
        self.label_6.setScaledContents(True)
        self.lineEdit = QLineEdit(self.centralwidget)
        self.lineEdit.setObjectName(u"lineEdit")
        self.lineEdit.setGeometry(QRect(130, 220, 451, 20))
        font5 = QFont()
        font5.setFamily(u"Arial")
        font5.setPointSize(10)
        self.lineEdit.setFont(font5)
        self.SubmitButton = QPushButton(self.centralwidget)
        self.SubmitButton.setObjectName(u"SubmitButton")
        self.SubmitButton.setGeometry(QRect(590, 220, 75, 23))
        self.thumbnail_label = QLabel(self.centralwidget)
        self.thumbnail_label.setObjectName(u"thumbnail_label")
        self.thumbnail_label.setGeometry(QRect(30, 260, 191, 121))
        self.thumbnail_label.setScaledContents(True)
        self.title_label = QLabel(self.centralwidget)
        self.title_label.setObjectName(u"title_label")
        self.title_label.setGeometry(QRect(240, 250, 381, 31))
        font6 = QFont()
        font6.setFamily(u"Segoe UI")
        font6.setPointSize(12)
        self.title_label.setFont(font6)
        self.title_label.setCursor(QCursor(Qt.ArrowCursor))
        self.progressBar = QProgressBar(self.centralwidget)
        self.progressBar.setObjectName(u"progressBar")
        self.progressBar.setGeometry(QRect(430, 670, 231, 31))
        self.progressBar.setMinimum(0)
        self.progressBar.setValue(0)
        self.progressBar.setTextVisible(False)
        self.author_label = QLabel(self.centralwidget)
        self.author_label.setObjectName(u"author_label")
        self.author_label.setGeometry(QRect(240, 270, 381, 31))
        self.author_label.setFont(font6)
        self.author_label.setCursor(QCursor(Qt.ArrowCursor))
        self.date_label = QLabel(self.centralwidget)
        self.date_label.setObjectName(u"date_label")
        self.date_label.setGeometry(QRect(240, 290, 381, 31))
        self.date_label.setFont(font6)
        self.date_label.setCursor(QCursor(Qt.ArrowCursor))
        self.views_label = QLabel(self.centralwidget)
        self.views_label.setObjectName(u"views_label")
        self.views_label.setGeometry(QRect(240, 310, 381, 31))
        self.views_label.setFont(font6)
        self.views_label.setCursor(QCursor(Qt.ArrowCursor))
        self.rating_label = QLabel(self.centralwidget)
        self.rating_label.setObjectName(u"rating_label")
        self.rating_label.setGeometry(QRect(240, 330, 381, 31))
        self.rating_label.setFont(font6)
        self.rating_label.setCursor(QCursor(Qt.ArrowCursor))
        self.delButton = QPushButton(self.centralwidget)
        self.delButton.setObjectName(u"delButton")
        self.delButton.setEnabled(True)
        self.delButton.setGeometry(QRect(670, 220, 21, 23))
        self.delButton.setFont(font4)
        self.delButton.setCheckable(False)
        self.delButton.setChecked(False)
        self.delButton.setAutoRepeat(False)
        self.clearButton = QPushButton(self.centralwidget)
        self.clearButton.setObjectName(u"clearButton")
        self.clearButton.setGeometry(QRect(240, 360, 41, 23))
        self.clearButton.setAutoDefault(False)
        self.clearButton.setFlat(False)
        self.widget = QWidget(self.centralwidget)
        self.widget.setObjectName(u"widget")
        self.widget.setGeometry(QRect(30, 440, 291, 51))
        self.bestresbtn = QRadioButton(self.widget)
        self.bestresbtn.setObjectName(u"bestresbtn")
        self.bestresbtn.setGeometry(QRect(0, 0, 281, 17))
        self.bestresbtn.setFont(font3)
        self.bestresbtn.setChecked(True)
        self.chooseresbtn = QRadioButton(self.widget)
        self.chooseresbtn.setObjectName(u"chooseresbtn")
        self.chooseresbtn.setGeometry(QRect(0, 30, 281, 17))
        self.chooseresbtn.setFont(font3)
        self.widget_2 = QWidget(self.centralwidget)
        self.widget_2.setObjectName(u"widget_2")
        self.widget_2.setGeometry(QRect(360, 440, 291, 51))
        self.bestresbtn_2 = QRadioButton(self.widget_2)
        self.bestresbtn_2.setObjectName(u"bestresbtn_2")
        self.bestresbtn_2.setGeometry(QRect(0, 0, 281, 17))
        self.bestresbtn_2.setFont(font3)
        self.bestresbtn_2.setChecked(True)
        self.chooseresbtn_2 = QRadioButton(self.widget_2)
        self.chooseresbtn_2.setObjectName(u"chooseresbtn_2")
        self.chooseresbtn_2.setGeometry(QRect(0, 30, 281, 17))
        self.chooseresbtn_2.setFont(font3)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menuBar = QMenuBar(MainWindow)
        self.menuBar.setObjectName(u"menuBar")
        self.menuBar.setGeometry(QRect(0, 0, 700, 21))
        self.menuSettings = QMenu(self.menuBar)
        self.menuSettings.setObjectName(u"menuSettings")
        MainWindow.setMenuBar(self.menuBar)

        self.menuBar.addAction(self.menuSettings.menuAction())
        self.menuSettings.addAction(self.actionChange_Downloads_Location)
        self.menuSettings.addAction(self.actionAbout)
        self.menuSettings.addAction(self.actionExit)

        self.retranslateUi(MainWindow)

        self.clearButton.setDefault(False)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.actionChange_Downloads_Location.setText(QCoreApplication.translate("MainWindow", u"Change Downloads Location ...", None))
        self.actionAbout.setText(QCoreApplication.translate("MainWindow", u"About", None))
        self.actionExit.setText(QCoreApplication.translate("MainWindow", u"Exit", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Youtube Downloader", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"by Nicklor", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"Your URL : ", None))
        self.checkBox.setText(QCoreApplication.translate("MainWindow", u"Download Video", None))
        self.checkBox_2.setText(QCoreApplication.translate("MainWindow", u"Download Audio", None))
        self.commandLinkButton.setText(QCoreApplication.translate("MainWindow", u"Download", None))
        self.label_6.setText("")
        self.SubmitButton.setText(QCoreApplication.translate("MainWindow", u"Submit", None))
        self.thumbnail_label.setText("")
        self.title_label.setText("")
        self.author_label.setText("")
        self.date_label.setText("")
        self.views_label.setText("")
        self.rating_label.setText("")
        self.delButton.setText(QCoreApplication.translate("MainWindow", u"\u00d7", None))
        self.clearButton.setText(QCoreApplication.translate("MainWindow", u"Clear", None))
        self.bestresbtn.setText(QCoreApplication.translate("MainWindow", u"Choose best resolution", None))
        self.chooseresbtn.setText(QCoreApplication.translate("MainWindow", u"Choose video to download : ", None))
        self.bestresbtn_2.setText(QCoreApplication.translate("MainWindow", u"Choose best resolution", None))
        self.chooseresbtn_2.setText(QCoreApplication.translate("MainWindow", u"Choose audio to download : ", None))
        self.menuSettings.setTitle(QCoreApplication.translate("MainWindow", u"Settings", None))
    # retranslateUi

