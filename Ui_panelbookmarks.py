# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'panelbookmarks.ui'
#
# Created: Tue Dec 14 06:39:32 2010
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
        self.buttonAddBookmark = QtGui.QPushButton(PanelBookmarks)
        self.buttonAddBookmark.setObjectName(_fromUtf8("buttonAddBookmark"))
        self.hboxlayout.addWidget(self.buttonAddBookmark)
        self.buttonEditBookmark = QtGui.QPushButton(PanelBookmarks)
        self.buttonEditBookmark.setObjectName(_fromUtf8("buttonEditBookmark"))
        self.hboxlayout.addWidget(self.buttonEditBookmark)
        self.buttonDelBookmark = QtGui.QPushButton(PanelBookmarks)
        self.buttonDelBookmark.setObjectName(_fromUtf8("buttonDelBookmark"))
        self.hboxlayout.addWidget(self.buttonDelBookmark)
        self.vboxlayout.addLayout(self.hboxlayout)

        self.retranslateUi(PanelBookmarks)
        QtCore.QMetaObject.connectSlotsByName(PanelBookmarks)

    def retranslateUi(self, PanelBookmarks):
        self.buttonAddBookmark.setText(QtGui.QApplication.translate("PanelBookmarks", "&Add", None, QtGui.QApplication.UnicodeUTF8))
        self.buttonEditBookmark.setText(QtGui.QApplication.translate("PanelBookmarks", "Edi&t", None, QtGui.QApplication.UnicodeUTF8))
        self.buttonDelBookmark.setText(QtGui.QApplication.translate("PanelBookmarks", "&Del", None, QtGui.QApplication.UnicodeUTF8))

