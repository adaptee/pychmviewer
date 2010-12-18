# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'about.ui'
#
# Created: Sat Dec 18 22:23:48 2010
#      by: PyQt4 UI code generator 4.8.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.resize(491, 273)
        self.buttonBox = QtGui.QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(180, 230, 260, 31))
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setCenterButtons(False)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.labelDetailInfo = QtGui.QLabel(Dialog)
        self.labelDetailInfo.setGeometry(QtCore.QRect(160, 30, 311, 181))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.labelDetailInfo.sizePolicy().hasHeightForWidth())
        self.labelDetailInfo.setSizePolicy(sizePolicy)
        self.labelDetailInfo.setOpenExternalLinks(True)
        self.labelDetailInfo.setObjectName(_fromUtf8("labelDetailInfo"))
        self.labelAppName = QtGui.QLabel(Dialog)
        self.labelAppName.setGeometry(QtCore.QRect(20, 40, 107, 141))
        self.labelAppName.setMaximumSize(QtCore.QSize(107, 16777215))
        self.labelAppName.setText(_fromUtf8(""))
        self.labelAppName.setPixmap(QtGui.QPixmap(_fromUtf8(":/images/pychmviewer.png")))
        self.labelAppName.setObjectName(_fromUtf8("labelAppName"))

        self.retranslateUi(Dialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), Dialog.accept)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "about", None, QtGui.QApplication.UnicodeUTF8))
        self.labelDetailInfo.setText(QtGui.QApplication.translate("Dialog", "TextLabel", None, QtGui.QApplication.UnicodeUTF8))

import images_rc
