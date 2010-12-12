# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/mnt/personal/code/pychmviewer/settingdlg.ui'
#
# Created: Sun Dec 12 20:35:31 2010
#      by: PyQt4 UI code generator 4.8.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.resize(335, 329)
        self.verticalLayout = QtGui.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.verticalLayout_2 = QtGui.QVBoxLayout()
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.tabWidget = QtGui.QTabWidget(Dialog)
        self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
        self.tab = QtGui.QWidget()
        self.tab.setObjectName(_fromUtf8("tab"))
        self.verticalLayoutWidget_2 = QtGui.QWidget(self.tab)
        self.verticalLayoutWidget_2.setGeometry(QtCore.QRect(20, 40, 160, 80))
        self.verticalLayoutWidget_2.setObjectName(_fromUtf8("verticalLayoutWidget_2"))
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.verticalLayoutWidget_2)
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.loadlastCheckbox = QtGui.QCheckBox(self.verticalLayoutWidget_2)
        self.loadlastCheckbox.setObjectName(_fromUtf8("loadlastCheckbox"))
        self.verticalLayout_3.addWidget(self.loadlastCheckbox)
        self.openRemoteCheckbox = QtGui.QCheckBox(self.verticalLayoutWidget_2)
        self.openRemoteCheckbox.setObjectName(_fromUtf8("openRemoteCheckbox"))
        self.verticalLayout_3.addWidget(self.openRemoteCheckbox)
        self.tabWidget.addTab(self.tab, _fromUtf8(""))
        self.tab_2 = QtGui.QWidget()
        self.tab_2.setObjectName(_fromUtf8("tab_2"))
        self.label = QtGui.QLabel(self.tab_2)
        self.label.setGeometry(QtCore.QRect(40, 130, 241, 91))
        self.label.setObjectName(_fromUtf8("label"))
        self.pushButton = QtGui.QPushButton(self.tab_2)
        self.pushButton.setGeometry(QtCore.QRect(90, 70, 105, 25))
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.tabWidget.addTab(self.tab_2, _fromUtf8(""))
        self.verticalLayout_2.addWidget(self.tabWidget)
        self.buttonBox = QtGui.QDialogButtonBox(Dialog)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.verticalLayout_2.addWidget(self.buttonBox)
        self.verticalLayout.addLayout(self.verticalLayout_2)

        self.retranslateUi(Dialog)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), Dialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "settings", None, QtGui.QApplication.UnicodeUTF8))
        self.loadlastCheckbox.setText(QtGui.QApplication.translate("Dialog", "打开上一次的标签页", None, QtGui.QApplication.UnicodeUTF8))
        self.openRemoteCheckbox.setText(QtGui.QApplication.translate("Dialog", "打开外部链接", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), QtGui.QApplication.translate("Dialog", "启动", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("Dialog", "TextLabel", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton.setText(QtGui.QApplication.translate("Dialog", "选择字体", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), QtGui.QApplication.translate("Dialog", "字体", None, QtGui.QApplication.UnicodeUTF8))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    Dialog = QtGui.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())

