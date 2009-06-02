# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/john/git/pychmviewer/tab_index.ui'
#
# Created: Sat May 30 02:03:54 2009
#      by: PyQt4 UI code generator 4.4.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_TabIndex(object):
    def setupUi(self, TabIndex):
        TabIndex.setObjectName("TabIndex")
        TabIndex.resize(173, 382)
        self.vboxlayout = QtGui.QVBoxLayout(TabIndex)
        self.vboxlayout.setMargin(9)
        self.vboxlayout.setSpacing(6)
        self.vboxlayout.setObjectName("vboxlayout")
        self.text = QtGui.QLineEdit(TabIndex)
        self.text.setObjectName("text")
        self.vboxlayout.addWidget(self.text)
        self.tree = QtGui.QTreeWidget(TabIndex)
        self.tree.setIndentation(10)
        self.tree.setRootIsDecorated(False)
        self.tree.setAllColumnsShowFocus(True)
        self.tree.setColumnCount(1)
        self.tree.setObjectName("tree")
        self.vboxlayout.addWidget(self.tree)

        self.retranslateUi(TabIndex)
        QtCore.QMetaObject.connectSlotsByName(TabIndex)

    def retranslateUi(self, TabIndex):
        TabIndex.setWindowTitle(QtGui.QApplication.translate("TabIndex", "Form1", None, QtGui.QApplication.UnicodeUTF8))
        self.tree.headerItem().setText(0, QtGui.QApplication.translate("TabIndex", "1", None, QtGui.QApplication.UnicodeUTF8))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    TabIndex = QtGui.QWidget()
    ui = Ui_TabIndex()
    ui.setupUi(TabIndex)
    TabIndex.show()
    sys.exit(app.exec_())

