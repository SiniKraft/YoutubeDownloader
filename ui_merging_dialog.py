# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'merging_dialogFJETZn.ui'
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
        self.textBrowser = QTextBrowser(MergingDialog)
        self.textBrowser.setObjectName(u"textBrowser")
        self.textBrowser.setGeometry(QRect(20, 70, 461, 351))
        self.label = QLabel(MergingDialog)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(100, 10, 401, 41))
        font = QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
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
        self.textBrowser.setHtml(QCoreApplication.translate("MergingDialog", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:'MS Shell Dlg 2'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>", None))
        self.label.setText(QCoreApplication.translate("MergingDialog", u"Merging audio and video ...", None))
    # retranslateUi

