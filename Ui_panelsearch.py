# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'panelsearch.ui'
#
# Created: Wed Dec 15 21:20:09 2010
#      by: PyQt4 UI code generator 4.8.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_PanelSearch(object):
    def setupUi(self, PanelSearch):
        PanelSearch.setObjectName(_fromUtf8("PanelSearch"))
        PanelSearch.resize(236, 409)
        self.vboxlayout = QtGui.QVBoxLayout(PanelSearch)
        self.vboxlayout.setSpacing(6)
        self.vboxlayout.setMargin(9)
        self.vboxlayout.setObjectName(_fromUtf8("vboxlayout"))
        self.hboxlayout = QtGui.QHBoxLayout()
        self.hboxlayout.setSpacing(6)
        self.hboxlayout.setMargin(0)
        self.hboxlayout.setObjectName(_fromUtf8("hboxlayout"))
        self.labelPrompt = QtGui.QLabel(PanelSearch)
        self.labelPrompt.setObjectName(_fromUtf8("labelPrompt"))
        self.hboxlayout.addWidget(self.labelPrompt)
        self.vboxlayout.addLayout(self.hboxlayout)
        self.hboxlayout1 = QtGui.QHBoxLayout()
        self.hboxlayout1.setSpacing(6)
        self.hboxlayout1.setMargin(0)
        self.hboxlayout1.setObjectName(_fromUtf8("hboxlayout1"))
        self.searchBox = QtGui.QComboBox(PanelSearch)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(2)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.searchBox.sizePolicy().hasHeightForWidth())
        self.searchBox.setSizePolicy(sizePolicy)
        self.searchBox.setEditable(True)
        self.searchBox.setMaxCount(10)
        self.searchBox.setObjectName(_fromUtf8("searchBox"))
        self.hboxlayout1.addWidget(self.searchBox)
        self.buttonGo = QtGui.QPushButton(PanelSearch)
        self.buttonGo.setObjectName(_fromUtf8("buttonGo"))
        self.hboxlayout1.addWidget(self.buttonGo)
        self.vboxlayout.addLayout(self.hboxlayout1)
        self.tree = QtGui.QTreeWidget(PanelSearch)
        self.tree.setRootIsDecorated(False)
        self.tree.setItemsExpandable(False)
        self.tree.setAllColumnsShowFocus(True)
        self.tree.setColumnCount(2)
        self.tree.setObjectName(_fromUtf8("tree"))
        self.vboxlayout.addWidget(self.tree)

        self.retranslateUi(PanelSearch)
        QtCore.QMetaObject.connectSlotsByName(PanelSearch)

    def retranslateUi(self, PanelSearch):
        PanelSearch.setWindowTitle(QtGui.QApplication.translate("PanelSearch", "Form1", None, QtGui.QApplication.UnicodeUTF8))
        self.labelPrompt.setText(QtGui.QApplication.translate("PanelSearch", "Type in word(s) to search for:", None, QtGui.QApplication.UnicodeUTF8))
        self.buttonGo.setText(QtGui.QApplication.translate("PanelSearch", "&Go", None, QtGui.QApplication.UnicodeUTF8))
        self.tree.setSortingEnabled(False)
        self.tree.headerItem().setText(0, QtGui.QApplication.translate("PanelSearch", "Title", None, QtGui.QApplication.UnicodeUTF8))
        self.tree.headerItem().setText(1, QtGui.QApplication.translate("PanelSearch", "Location", None, QtGui.QApplication.UnicodeUTF8))

