# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/mnt/personal/code/pychmviewer/dialog_topicselector.ui'
#
# Created: Fri Dec 10 02:38:10 2010
#      by: PyQt4 UI code generator 4.8.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_DialogTopicSelector(object):
    def setupUi(self, DialogTopicSelector):
        DialogTopicSelector.setObjectName(_fromUtf8("DialogTopicSelector"))
        DialogTopicSelector.resize(218, 258)
        self.vboxlayout = QtGui.QVBoxLayout(DialogTopicSelector)
        self.vboxlayout.setMargin(9)
        self.vboxlayout.setSpacing(6)
        self.vboxlayout.setObjectName(_fromUtf8("vboxlayout"))
        self.label = QtGui.QLabel(DialogTopicSelector)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName(_fromUtf8("label"))
        self.vboxlayout.addWidget(self.label)
        self.list = QtGui.QListWidget(DialogTopicSelector)
        self.list.setObjectName(_fromUtf8("list"))
        self.vboxlayout.addWidget(self.list)
        self.buttonBox = QtGui.QDialogButtonBox(DialogTopicSelector)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.NoButton|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.vboxlayout.addWidget(self.buttonBox)

        self.retranslateUi(DialogTopicSelector)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), DialogTopicSelector.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), DialogTopicSelector.reject)
        QtCore.QMetaObject.connectSlotsByName(DialogTopicSelector)

    def retranslateUi(self, DialogTopicSelector):
        DialogTopicSelector.setWindowTitle(QtGui.QApplication.translate("DialogTopicSelector", "Multiple topics", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("DialogTopicSelector", "Please select the topic to open:", None, QtGui.QApplication.UnicodeUTF8))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    DialogTopicSelector = QtGui.QDialog()
    ui = Ui_DialogTopicSelector()
    ui.setupUi(DialogTopicSelector)
    DialogTopicSelector.show()
    sys.exit(app.exec_())

