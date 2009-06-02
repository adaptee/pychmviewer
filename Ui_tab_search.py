# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/john/git/pychmviewer/tab_search.ui'
#
# Created: Sat May 30 20:10:11 2009
#      by: PyQt4 UI code generator 4.4.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_TabSearch(object):
    def setupUi(self, TabSearch):
        TabSearch.setObjectName("TabSearch")
        TabSearch.resize(236, 409)
        self.vboxlayout = QtGui.QVBoxLayout(TabSearch)
        self.vboxlayout.setSpacing(6)
        self.vboxlayout.setMargin(9)
        self.vboxlayout.setObjectName("vboxlayout")
        self.hboxlayout = QtGui.QHBoxLayout()
        self.hboxlayout.setSpacing(6)
        self.hboxlayout.setMargin(0)
        self.hboxlayout.setObjectName("hboxlayout")
        self.label = QtGui.QLabel(TabSearch)
        self.label.setObjectName("label")
        self.hboxlayout.addWidget(self.label)
        self.vboxlayout.addLayout(self.hboxlayout)
        self.hboxlayout1 = QtGui.QHBoxLayout()
        self.hboxlayout1.setSpacing(6)
        self.hboxlayout1.setMargin(0)
        self.hboxlayout1.setObjectName("hboxlayout1")
        self.searchBox = QtGui.QComboBox(TabSearch)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(2)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.searchBox.sizePolicy().hasHeightForWidth())
        self.searchBox.setSizePolicy(sizePolicy)
        self.searchBox.setEditable(True)
        self.searchBox.setMaxCount(10)
        self.searchBox.setObjectName("searchBox")
        self.hboxlayout1.addWidget(self.searchBox)
        self.btnGo = QtGui.QPushButton(TabSearch)
        self.btnGo.setObjectName("btnGo")
        self.hboxlayout1.addWidget(self.btnGo)
        self.vboxlayout.addLayout(self.hboxlayout1)
        self.tree = QtGui.QTreeWidget(TabSearch)
        self.tree.setRootIsDecorated(False)
        self.tree.setItemsExpandable(False)
        self.tree.setAllColumnsShowFocus(True)
        self.tree.setColumnCount(2)
        self.tree.setObjectName("tree")
        self.vboxlayout.addWidget(self.tree)

        self.retranslateUi(TabSearch)
        QtCore.QMetaObject.connectSlotsByName(TabSearch)

    def retranslateUi(self, TabSearch):
        TabSearch.setWindowTitle(QtGui.QApplication.translate("TabSearch", "Form1", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("TabSearch", "Type in word(s) to search for:", None, QtGui.QApplication.UnicodeUTF8))
        self.btnGo.setText(QtGui.QApplication.translate("TabSearch", "&Go", None, QtGui.QApplication.UnicodeUTF8))
        self.tree.setSortingEnabled(False)
        self.tree.headerItem().setText(0, QtGui.QApplication.translate("TabSearch", "Title", None, QtGui.QApplication.UnicodeUTF8))
        self.tree.headerItem().setText(1, QtGui.QApplication.translate("TabSearch", "Location", None, QtGui.QApplication.UnicodeUTF8))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    TabSearch = QtGui.QWidget()
    ui = Ui_TabSearch()
    ui.setupUi(TabSearch)
    TabSearch.show()
    sys.exit(app.exec_())

