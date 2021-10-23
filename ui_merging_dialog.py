# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'merging_dialogbJPVjC.ui'
##
## Created by: Qt User Interface Compiler version 5.15.5
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *  # type: ignore
from PySide2.QtGui import *  # type: ignore
from PySide2.QtWidgets import *  # type: ignore


class Ui_MergingDialog(object):
    def setupUi(self, MergingDialog):
        if not MergingDialog.objectName():
            MergingDialog.setObjectName(u"MergingDialog")
        MergingDialog.resize(507, 468)
        MergingDialog.setMinimumSize(QSize(507, 468))
        MergingDialog.setMaximumSize(QSize(507, 468))
        self.plainTextEdit = QPlainTextEdit(MergingDialog)
        self.plainTextEdit.setObjectName(u"plainTextEdit")
        self.plainTextEdit.setEnabled(True)
        self.plainTextEdit.setGeometry(QRect(20, 70, 461, 351))
        font = QFont()
        font.setFamily(u"Consolas")
        font.setPointSize(9)
        self.plainTextEdit.setFont(font)
        self.plainTextEdit.setLineWrapMode(QPlainTextEdit.NoWrap)
        self.plainTextEdit.setReadOnly(True)
        self.plainTextEdit.setCenterOnScroll(True)
        self.label = QLabel(MergingDialog)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(100, 10, 401, 41))
        font1 = QFont()
        font1.setPointSize(16)
        font1.setBold(True)
        font1.setWeight(75)
        self.label.setFont(font1)
        self.progressBar = QProgressBar(MergingDialog)
        self.progressBar.setObjectName(u"progressBar")
        self.progressBar.setGeometry(QRect(20, 433, 461, 20))
        self.progressBar.setMaximum(0)
        self.progressBar.setValue(0)
        self.progressBar.setTextVisible(False)

        self.retranslateUi(MergingDialog)

        QMetaObject.connectSlotsByName(MergingDialog)
    # setupUi

    def retranslateUi(self, MergingDialog):
        MergingDialog.setWindowTitle(QCoreApplication.translate("MergingDialog", u"Dialog", None))
        self.plainTextEdit.setPlainText("")
        self.label.setText(QCoreApplication.translate("MergingDialog", u"Merging audio and video ...", None))
    # retranslateUi

