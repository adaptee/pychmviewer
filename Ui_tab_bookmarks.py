# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/john/git/pychmviewer/tab_bookmarks.ui'
#
# Created: Sun May 31 04:26:12 2009
#      by: PyQt4 UI code generator 4.4.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_TabBookmarks(object):
    def setupUi(self, TabBookmarks):
        TabBookmarks.setObjectName("TabBookmarks")
        TabBookmarks.resize(257, 296)
        self.vboxlayout = QtGui.QVBoxLayout(TabBookmarks)
        self.vboxlayout.setMargin(9)
        self.vboxlayout.setSpacing(6)
        self.vboxlayout.setObjectName("vboxlayout")
        self.list = QtGui.QListWidget(TabBookmarks)
        self.list.setObjectName("list")
        self.vboxlayout.addWidget(self.list)
        self.hboxlayout = QtGui.QHBoxLayout()
        self.hboxlayout.setMargin(0)
        self.hboxlayout.setSpacing(6)
        self.hboxlayout.setObjectName("hboxlayout")
        self.btnAdd = QtGui.QPushButton(TabBookmarks)
        self.btnAdd.setObjectName("btnAdd")
        self.hboxlayout.addWidget(self.btnAdd)
        self.btnEdit = QtGui.QPushButton(TabBookmarks)
        self.btnEdit.setObjectName("btnEdit")
        self.hboxlayout.addWidget(self.btnEdit)
        self.btnDel = QtGui.QPushButton(TabBookmarks)
        self.btnDel.setObjectName("btnDel")
        self.hboxlayout.addWidget(self.btnDel)
        self.vboxlayout.addLayout(self.hboxlayout)

        self.retranslateUi(TabBookmarks)
        QtCore.QMetaObject.connectSlotsByName(TabBookmarks)

    def retranslateUi(self, TabBookmarks):
        self.btnAdd.setText(QtGui.QApplication.translate("TabBookmarks", "&Add", None, QtGui.QApplication.UnicodeUTF8))
        self.btnEdit.setText(QtGui.QApplication.translate("TabBookmarks", "Edi&t", None, QtGui.QApplication.UnicodeUTF8))
        self.btnDel.setText(QtGui.QApplication.translate("TabBookmarks", "&Del", None, QtGui.QApplication.UnicodeUTF8))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    TabBookmarks = QtGui.QWidget()
    ui = Ui_TabBookmarks()
    ui.setupUi(TabBookmarks)
    TabBookmarks.show()
    sys.exit(app.exec_())

