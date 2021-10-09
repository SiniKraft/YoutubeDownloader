# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'path_dialognRADyW.ui'
##
## Created by: Qt User Interface Compiler version 5.15.5
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *  # type: ignore
from PySide2.QtGui import *  # type: ignore
from PySide2.QtWidgets import *  # type: ignore


class Ui_PathDialog(object):
    def setupUi(self, PathDialog):
        if not PathDialog.objectName():
            PathDialog.setObjectName(u"PathDialog")
        PathDialog.setEnabled(True)
        PathDialog.resize(362, 111)
        PathDialog.setMinimumSize(QSize(362, 111))
        PathDialog.setMaximumSize(QSize(362, 111))
        self.verticalLayoutWidget = QWidget(PathDialog)
        self.verticalLayoutWidget.setObjectName(u"verticalLayoutWidget")
        self.verticalLayoutWidget.setGeometry(QRect(20, 9, 321, 91))
        self.verticalLayout = QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.label = QLabel(self.verticalLayoutWidget)
        self.label.setObjectName(u"label")
        font = QFont()
        font.setPointSize(12)
        self.label.setFont(font)

        self.verticalLayout.addWidget(self.label)

        self.lineEdit = QLineEdit(self.verticalLayoutWidget)
        self.lineEdit.setObjectName(u"lineEdit")
        font1 = QFont()
        font1.setFamily(u"Arial")
        font1.setPointSize(10)
        self.lineEdit.setFont(font1)

        self.verticalLayout.addWidget(self.lineEdit)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)

        self.buttonBox = QDialogButtonBox(self.verticalLayoutWidget)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.verticalLayout.addWidget(self.buttonBox)


        self.retranslateUi(PathDialog)
        self.buttonBox.accepted.connect(PathDialog.accept)
        self.buttonBox.rejected.connect(PathDialog.reject)

        QMetaObject.connectSlotsByName(PathDialog)
    # setupUi

    def retranslateUi(self, PathDialog):
        PathDialog.setWindowTitle(QCoreApplication.translate("PathDialog", u"Dialog", None))
        self.label.setText(QCoreApplication.translate("PathDialog", u"Enter where you want to download videos :", None))
    # retranslateUi

