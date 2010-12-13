# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'panelbookmarks.ui'
#
# Created: Tue Dec 14 06:35:23 2010
#      by: PyQt4 UI code generator 4.8.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_PanelBookmarks(object):
    def setupUi(self, PanelBookmarks):
        PanelBookmarks.setObjectName(_fromUtf8("PanelBookmarks"))
        PanelBookmarks.resize(257, 296)
        PanelBookmarks.setWindowTitle(_fromUtf8(""))
        self.vboxlayout = QtGui.QVBoxLayout(PanelBookmarks)
        self.vboxlayout.setMargin(9)
        self.vboxlayout.setSpacing(6)
        self.vboxlayout.setObjectName(_fromUtf8("vboxlayout"))
        self.list = QtGui.QListWidget(PanelBookmarks)
        self.list.setObjectName(_fromUtf8("list"))
        self.vboxlayout.addWidget(self.list)
        self.hboxlayout = QtGui.QHBoxLayout()
        self.hboxlayout.setMargin(0)
        self.hboxlayout.setSpacing(6)
        self.hboxlayout.setObjectName(_fromUtf8("hboxlayout"))
        self.btnAdd = QtGui.QPushButton(PanelBookmarks)
        self.btnAdd.setObjectName(_fromUtf8("btnAdd"))
        self.hboxlayout.addWidget(self.btnAdd)
        self.btnEdit = QtGui.QPushButton(PanelBookmarks)
        self.btnEdit.setObjectName(_fromUtf8("btnEdit"))
        self.hboxlayout.addWidget(self.btnEdit)
        self.btnDel = QtGui.QPushButton(PanelBookmarks)
        self.btnDel.setObjectName(_fromUtf8("btnDel"))
        self.hboxlayout.addWidget(self.btnDel)
        self.vboxlayout.addLayout(self.hboxlayout)

        self.retranslateUi(PanelBookmarks)
        QtCore.QMetaObject.connectSlotsByName(PanelBookmarks)

    def retranslateUi(self, PanelBookmarks):
        self.btnAdd.setText(QtGui.QApplication.translate("PanelBookmarks", "&Add", None, QtGui.QApplication.UnicodeUTF8))
        self.btnEdit.setText(QtGui.QApplication.translate("PanelBookmarks", "Edi&t", None, QtGui.QApplication.UnicodeUTF8))
        self.btnDel.setText(QtGui.QApplication.translate("PanelBookmarks", "&Del", None, QtGui.QApplication.UnicodeUTF8))

