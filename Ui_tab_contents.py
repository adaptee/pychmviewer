# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/john/git/pychmviewer/tab_contents.ui'
#
# Created: Sat May 30 03:23:59 2009
#      by: PyQt4 UI code generator 4.4.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_TabContents(object):
    def setupUi(self, TabContents):
        TabContents.setObjectName("TabContents")
        TabContents.resize(257, 424)
        self.vboxlayout = QtGui.QVBoxLayout(TabContents)
        self.vboxlayout.setSpacing(6)
        self.vboxlayout.setMargin(9)
        self.vboxlayout.setObjectName("vboxlayout")
        self.tree = QtGui.QTreeWidget(TabContents)
        self.tree.setObjectName("tree")
        self.tree.headerItem().setText(0, "1")
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

