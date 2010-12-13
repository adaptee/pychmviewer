# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'panelindex.ui'
#
# Created: Tue Dec 14 06:24:01 2010
#      by: PyQt4 UI code generator 4.8.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_PanelIndex(object):
    def setupUi(self, PanelIndex):
        PanelIndex.setObjectName(_fromUtf8("PanelIndex"))
        PanelIndex.resize(173, 382)
        self.vboxlayout = QtGui.QVBoxLayout(PanelIndex)
        self.vboxlayout.setSpacing(6)
        self.vboxlayout.setMargin(9)
        self.vboxlayout.setObjectName(_fromUtf8("vboxlayout"))
        self.text = QtGui.QLineEdit(PanelIndex)
        self.text.setObjectName(_fromUtf8("text"))
        self.vboxlayout.addWidget(self.text)
        self.tree = QtGui.QTreeWidget(PanelIndex)
        self.tree.setHeaderHidden(True)
        self.tree.setIndentation(10)
        self.tree.setRootIsDecorated(False)
        self.tree.setAllColumnsShowFocus(True)
        self.tree.setColumnCount(1)
        self.tree.setObjectName(_fromUtf8("tree"))
        self.vboxlayout.addWidget(self.tree)

        self.retranslateUi(PanelIndex)
        QtCore.QMetaObject.connectSlotsByName(PanelIndex)

    def retranslateUi(self, PanelIndex):
        PanelIndex.setWindowTitle(QtGui.QApplication.translate("PanelIndex", "Index", None, QtGui.QApplication.UnicodeUTF8))
        self.tree.headerItem().setText(0, QtGui.QApplication.translate("PanelIndex", "1", None, QtGui.QApplication.UnicodeUTF8))

