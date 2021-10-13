# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'convert_dialogotBJqN.ui'
##
## Created by: Qt User Interface Compiler version 5.15.5
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *  # type: ignore
from PySide2.QtGui import *  # type: ignore
from PySide2.QtWidgets import *  # type: ignore


class Ui_ConvertDialog(object):
    def setupUi(self, ConvertDialog):
        if not ConvertDialog.objectName():
            ConvertDialog.setObjectName(u"ConvertDialog")
        ConvertDialog.resize(375, 255)
        self.buttonBox = QDialogButtonBox(ConvertDialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setGeometry(QRect(20, 220, 341, 32))
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)
        self.label = QLabel(ConvertDialog)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(50, 10, 301, 61))
        font = QFont()
        font.setPointSize(16)
        self.label.setFont(font)
        self.gridLayoutWidget = QWidget(ConvertDialog)
        self.gridLayoutWidget.setObjectName(u"gridLayoutWidget")
        self.gridLayoutWidget.setGeometry(QRect(40, 70, 281, 131))
        self.gridLayout = QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.mp4 = QRadioButton(self.gridLayoutWidget)
        self.mp4.setObjectName(u"mp4")

        self.gridLayout.addWidget(self.mp4, 1, 0, 1, 1)

        self.mpg = QRadioButton(self.gridLayoutWidget)
        self.mpg.setObjectName(u"mpg")

        self.gridLayout.addWidget(self.mpg, 3, 0, 1, 1)

        self.mkv = QRadioButton(self.gridLayoutWidget)
        self.mkv.setObjectName(u"mkv")

        self.gridLayout.addWidget(self.mkv, 2, 0, 1, 1)

        self.avi = QRadioButton(self.gridLayoutWidget)
        self.avi.setObjectName(u"avi")

        self.gridLayout.addWidget(self.avi, 3, 1, 1, 1)

        self.wav = QRadioButton(self.gridLayoutWidget)
        self.wav.setObjectName(u"wav")

        self.gridLayout.addWidget(self.wav, 3, 2, 1, 1)

        self.ogm = QRadioButton(self.gridLayoutWidget)
        self.ogm.setObjectName(u"ogm")

        self.gridLayout.addWidget(self.ogm, 2, 1, 1, 1)

        self.ogg = QRadioButton(self.gridLayoutWidget)
        self.ogg.setObjectName(u"ogg")

        self.gridLayout.addWidget(self.ogg, 2, 2, 1, 1)

        self.webm = QRadioButton(self.gridLayoutWidget)
        self.webm.setObjectName(u"webm")

        self.gridLayout.addWidget(self.webm, 1, 1, 1, 1)

        self.mp3 = QRadioButton(self.gridLayoutWidget)
        self.mp3.setObjectName(u"mp3")

        self.gridLayout.addWidget(self.mp3, 1, 2, 1, 1)


        self.retranslateUi(ConvertDialog)
        self.buttonBox.accepted.connect(ConvertDialog.accept)
        self.buttonBox.rejected.connect(ConvertDialog.reject)

        QMetaObject.connectSlotsByName(ConvertDialog)
    # setupUi

    def retranslateUi(self, ConvertDialog):
        ConvertDialog.setWindowTitle(QCoreApplication.translate("ConvertDialog", u"Dialog", None))
        self.label.setText(QCoreApplication.translate("ConvertDialog", u"Choose an Export Format : ", None))
        self.mp4.setText(QCoreApplication.translate("ConvertDialog", u"MP4", None))
        self.mpg.setText(QCoreApplication.translate("ConvertDialog", u"MPG", None))
        self.mkv.setText(QCoreApplication.translate("ConvertDialog", u"MKV", None))
        self.avi.setText(QCoreApplication.translate("ConvertDialog", u"AVI", None))
        self.wav.setText(QCoreApplication.translate("ConvertDialog", u"WAV (audio only)", None))
        self.ogm.setText(QCoreApplication.translate("ConvertDialog", u"OGM", None))
        self.ogg.setText(QCoreApplication.translate("ConvertDialog", u"OGG (Audio only)", None))
        self.webm.setText(QCoreApplication.translate("ConvertDialog", u"WEBM", None))
        self.mp3.setText(QCoreApplication.translate("ConvertDialog", u"MP3 (Audio only)", None))
    # retranslateUi

