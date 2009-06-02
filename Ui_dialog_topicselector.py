# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/john/git/pychmviewer/dialog_topicselector.ui'
#
# Created: Sat May 30 04:10:07 2009
#      by: PyQt4 UI code generator 4.4.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_DialogTopicSelector(object):
    def setupUi(self, DialogTopicSelector):
        DialogTopicSelector.setObjectName("DialogTopicSelector")
        DialogTopicSelector.resize(218, 258)
        self.vboxlayout = QtGui.QVBoxLayout(DialogTopicSelector)
        self.vboxlayout.setMargin(9)
        self.vboxlayout.setSpacing(6)
        self.vboxlayout.setObjectName("vboxlayout")
        self.label = QtGui.QLabel(DialogTopicSelector)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.vboxlayout.addWidget(self.label)
        self.list = QtGui.QListWidget(DialogTopicSelector)
        self.list.setObjectName("list")
        self.vboxlayout.addWidget(self.list)
        self.buttonBox = QtGui.QDialogButtonBox(DialogTopicSelector)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.NoButton|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.vboxlayout.addWidget(self.buttonBox)

        self.retranslateUi(DialogTopicSelector)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), DialogTopicSelector.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), DialogTopicSelector.reject)
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

