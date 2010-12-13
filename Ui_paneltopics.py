# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'paneltopics.ui'
#
# Created: Tue Dec 14 06:13:08 2010
#      by: PyQt4 UI code generator 4.8.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_PanelTopics(object):
    def setupUi(self, PanelTopics):
        PanelTopics.setObjectName(_fromUtf8("PanelTopics"))
        PanelTopics.resize(257, 424)
        self.vboxlayout = QtGui.QVBoxLayout(PanelTopics)
        self.vboxlayout.setSpacing(6)
        self.vboxlayout.setMargin(9)
        self.vboxlayout.setObjectName(_fromUtf8("vboxlayout"))
        self.tree = QtGui.QTreeWidget(PanelTopics)
        self.tree.setHeaderHidden(True)
        self.tree.setObjectName(_fromUtf8("tree"))
        self.tree.headerItem().setText(0, _fromUtf8("1"))
        self.vboxlayout.addWidget(self.tree)

        self.retranslateUi(PanelTopics)
        QtCore.QMetaObject.connectSlotsByName(PanelTopics)

    def retranslateUi(self, PanelTopics):
        PanelTopics.setWindowTitle(QtGui.QApplication.translate("PanelTopics", "Topics", None, QtGui.QApplication.UnicodeUTF8))

