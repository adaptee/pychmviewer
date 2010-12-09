# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/mnt/personal/code/pychmviewer/tab_contents.ui'
#
# Created: Fri Dec 10 02:38:12 2010
#      by: PyQt4 UI code generator 4.8.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_TabContents(object):
    def setupUi(self, TabContents):
        TabContents.setObjectName(_fromUtf8("TabContents"))
        TabContents.resize(257, 424)
        self.vboxlayout = QtGui.QVBoxLayout(TabContents)
        self.vboxlayout.setSpacing(6)
        self.vboxlayout.setMargin(9)
        self.vboxlayout.setObjectName(_fromUtf8("vboxlayout"))
        self.tree = QtGui.QTreeWidget(TabContents)
        self.tree.setObjectName(_fromUtf8("tree"))
        self.tree.headerItem().setText(0, _fromUtf8("1"))
        self.tree.header().setVisible(False)
        self.tree.header().setDefaultSectionSize(0)
        self.tree.header().setMinimumSectionSize(0)
        self.tree.header().setStretchLastSection(False)
        self.vboxlayout.addWidget(self.tree)

        self.retranslateUi(TabContents)
        QtCore.QMetaObject.connectSlotsByName(TabContents)

    def retranslateUi(self, TabContents):
        TabContents.setWindowTitle(QtGui.QApplication.translate("TabContents", "Content", None, QtGui.QApplication.UnicodeUTF8))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    TabContents = QtGui.QWidget()
    ui = Ui_TabContents()
    ui.setupUi(TabContents)
    TabContents.show()
    sys.exit(app.exec_())

