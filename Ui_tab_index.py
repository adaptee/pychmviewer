# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/mnt/personal/code/pychmviewer/tab_index.ui'
#
# Created: Fri Dec 10 02:38:13 2010
#      by: PyQt4 UI code generator 4.8.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_TabIndex(object):
    def setupUi(self, TabIndex):
        TabIndex.setObjectName(_fromUtf8("TabIndex"))
        TabIndex.resize(173, 382)
        self.vboxlayout = QtGui.QVBoxLayout(TabIndex)
        self.vboxlayout.setSpacing(6)
        self.vboxlayout.setMargin(9)
        self.vboxlayout.setObjectName(_fromUtf8("vboxlayout"))
        self.text = QtGui.QLineEdit(TabIndex)
        self.text.setObjectName(_fromUtf8("text"))
        self.vboxlayout.addWidget(self.text)
        self.tree = QtGui.QTreeWidget(TabIndex)
        self.tree.setIndentation(10)
        self.tree.setRootIsDecorated(False)
        self.tree.setAllColumnsShowFocus(True)
        self.tree.setColumnCount(1)
        self.tree.setObjectName(_fromUtf8("tree"))
        self.vboxlayout.addWidget(self.tree)

        self.retranslateUi(TabIndex)
        QtCore.QMetaObject.connectSlotsByName(TabIndex)

    def retranslateUi(self, TabIndex):
        TabIndex.setWindowTitle(QtGui.QApplication.translate("TabIndex", "Index", None, QtGui.QApplication.UnicodeUTF8))
        self.tree.headerItem().setText(0, QtGui.QApplication.translate("TabIndex", "1", None, QtGui.QApplication.UnicodeUTF8))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    TabIndex = QtGui.QWidget()
    ui = Ui_TabIndex()
    ui.setupUi(TabIndex)
    TabIndex.show()
    sys.exit(app.exec_())

