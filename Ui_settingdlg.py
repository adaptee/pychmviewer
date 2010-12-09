# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/mnt/personal/code/pychmviewer/settingdlg.ui'
#
# Created: Fri Dec 10 02:38:11 2010
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
        Dialog.resize(400, 300)
        self.verticalLayout = QtGui.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.groupBoxdata = QtGui.QGroupBox(Dialog)
        self.groupBoxdata.setObjectName(_fromUtf8("groupBoxdata"))
        self.loadlastCheckbox = QtGui.QCheckBox(self.groupBoxdata)
        self.loadlastCheckbox.setGeometry(QtCore.QRect(50, 40, 161, 23))
        self.loadlastCheckbox.setObjectName(_fromUtf8("loadlastCheckbox"))
        self.openRemoteCheckbox = QtGui.QCheckBox(self.groupBoxdata)
        self.openRemoteCheckbox.setGeometry(QtCore.QRect(50, 70, 141, 23))
        self.openRemoteCheckbox.setObjectName(_fromUtf8("openRemoteCheckbox"))
        self.msglabel = QtGui.QLabel(self.groupBoxdata)
        self.msglabel.setGeometry(QtCore.QRect(80, 100, 181, 16))
        self.msglabel.setText(_fromUtf8(""))
        self.msglabel.setObjectName(_fromUtf8("msglabel"))
        self.verticalLayout.addWidget(self.groupBoxdata)
        self.groupBoxfont = QtGui.QGroupBox(Dialog)
        self.groupBoxfont.setObjectName(_fromUtf8("groupBoxfont"))
        self.pushButton = QtGui.QPushButton(self.groupBoxfont)
        self.pushButton.setGeometry(QtCore.QRect(270, 70, 105, 25))
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.label = QtGui.QLabel(self.groupBoxfont)
        self.label.setGeometry(QtCore.QRect(20, 30, 241, 91))
        self.label.setObjectName(_fromUtf8("label"))
        self.verticalLayout.addWidget(self.groupBoxfont)
        self.buttonBox = QtGui.QDialogButtonBox(Dialog)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(Dialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), Dialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "settings", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBoxdata.setTitle(QtGui.QApplication.translate("Dialog", "启动", None, QtGui.QApplication.UnicodeUTF8))
        self.loadlastCheckbox.setText(QtGui.QApplication.translate("Dialog", "打开上一次的标签页", None, QtGui.QApplication.UnicodeUTF8))
        self.openRemoteCheckbox.setText(QtGui.QApplication.translate("Dialog", "打开外部链接", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBoxfont.setTitle(QtGui.QApplication.translate("Dialog", "字体", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton.setText(QtGui.QApplication.translate("Dialog", "选择", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("Dialog", "TextLabel", None, QtGui.QApplication.UnicodeUTF8))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    Dialog = QtGui.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())

