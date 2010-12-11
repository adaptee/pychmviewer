# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/john/git/pychmviewer/window_browser.ui'
#
# Created: Mon Jun  1 08:29:13 2009
#      by: PyQt4 UI code generator 4.4.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_TabbedBrowser(object):
    def setupUi(self, TabbedBrowser):
        TabbedBrowser.setObjectName("TabbedBrowser")
        TabbedBrowser.resize(749, 664)
        self.vboxlayout = QtGui.QVBoxLayout(TabbedBrowser)
        self.vboxlayout.setSpacing(0)
        self.vboxlayout.setMargin(0)
        self.vboxlayout.setObjectName("vboxlayout")
        self.tabWidget = QtGui.QTabWidget(TabbedBrowser)
        self.tabWidget.setObjectName("tabWidget")
        self.frontpage = QtGui.QWidget()
        self.frontpage.setObjectName("frontpage")
        self.gridlayout = QtGui.QGridLayout(self.frontpage)
        self.gridlayout.setMargin(8)
        self.gridlayout.setSpacing(6)
        self.gridlayout.setObjectName("gridlayout")
        #self.tabWidget.addTab(self.frontpage, "")
        self.vboxlayout.addWidget(self.tabWidget)
        self.frameFind = QtGui.QFrame(TabbedBrowser)
        self.frameFind.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frameFind.setFrameShadow(QtGui.QFrame.Raised)
        self.frameFind.setObjectName("frameFind")
        self.hboxlayout = QtGui.QHBoxLayout(self.frameFind)
        self.hboxlayout.setSpacing(6)
        self.hboxlayout.setMargin(0)
        self.hboxlayout.setObjectName("hboxlayout")
        self.toolClose = QtGui.QToolButton(self.frameFind)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/images/find_close.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.toolClose.setIcon(icon)
        self.toolClose.setAutoRaise(True)
        self.toolClose.setObjectName("toolClose")
        self.hboxlayout.addWidget(self.toolClose)
        self.editFind = QtGui.QLineEdit(self.frameFind)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.editFind.sizePolicy().hasHeightForWidth())
        self.editFind.setSizePolicy(sizePolicy)
        self.editFind.setMinimumSize(QtCore.QSize(150, 0))
        self.editFind.setObjectName("editFind")
        self.hboxlayout.addWidget(self.editFind)
        self.toolPrevious = QtGui.QToolButton(self.frameFind)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/images/find_previous.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.toolPrevious.setIcon(icon1)
        self.toolPrevious.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
        self.toolPrevious.setAutoRaise(True)
        self.toolPrevious.setObjectName("toolPrevious")
        self.hboxlayout.addWidget(self.toolPrevious)
        self.toolNext = QtGui.QToolButton(self.frameFind)
        self.toolNext.setMinimumSize(QtCore.QSize(0, 0))
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/images/find_next.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.toolNext.setIcon(icon2)
        self.toolNext.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
        self.toolNext.setAutoRaise(True)
        self.toolNext.setArrowType(QtCore.Qt.NoArrow)
        self.toolNext.setObjectName("toolNext")
        self.hboxlayout.addWidget(self.toolNext)
        self.checkCase = QtGui.QCheckBox(self.frameFind)
        self.checkCase.setObjectName("checkCase")
        self.hboxlayout.addWidget(self.checkCase)
        spacerItem = QtGui.QSpacerItem(81, 21, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.hboxlayout.addItem(spacerItem)
        self.vboxlayout.addWidget(self.frameFind)

        self.retranslateUi(TabbedBrowser)
        QtCore.QMetaObject.connectSlotsByName(TabbedBrowser)

    def retranslateUi(self, TabbedBrowser):
        TabbedBrowser.setWindowTitle(QtGui.QApplication.translate("TabbedBrowser", "TabbedBrowser", None, QtGui.QApplication.UnicodeUTF8))
        #self.tabWidget.setTabText(self.tabWidget.indexOf(self.frontpage), QtGui.QApplication.translate("TabbedBrowser", "Untitled", None, QtGui.QApplication.UnicodeUTF8))
        self.toolPrevious.setText(QtGui.QApplication.translate("TabbedBrowser", "Previous", None, QtGui.QApplication.UnicodeUTF8))
        self.toolNext.setText(QtGui.QApplication.translate("TabbedBrowser", "Next", None, QtGui.QApplication.UnicodeUTF8))
        self.checkCase.setText(QtGui.QApplication.translate("TabbedBrowser", "Case Sensitive", None, QtGui.QApplication.UnicodeUTF8))

import images_rc

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    TabbedBrowser = QtGui.QWidget()
    ui = Ui_TabbedBrowser()
    ui.setupUi(TabbedBrowser)
    TabbedBrowser.show()
    sys.exit(app.exec_())

