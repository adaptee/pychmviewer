# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/john/git/pychmviewer/settingdlg.ui'
#
# Created: Wed Jun  3 17:25:07 2009
#      by: PyQt4 UI code generator 4.4.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(514, 516)
        self.verticalLayout = QtGui.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.tabWidget = QtGui.QTabWidget(Dialog)
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtGui.QWidget()
        self.tab.setObjectName("tab")
        self.loadlastCheckbox = QtGui.QCheckBox(self.tab)
        self.loadlastCheckbox.setGeometry(QtCore.QRect(100, 80, 161, 23))
        self.loadlastCheckbox.setObjectName("loadlastCheckbox")
        self.openRemoteCheckbox = QtGui.QCheckBox(self.tab)
        self.openRemoteCheckbox.setGeometry(QtCore.QRect(100, 150, 141, 23))
        self.openRemoteCheckbox.setObjectName("openRemoteCheckbox")
        self.msglabel = QtGui.QLabel(self.tab)
        self.msglabel.setGeometry(QtCore.QRect(110, 250, 171, 16))
        self.msglabel.setObjectName("msglabel")
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QtGui.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.label = QtGui.QLabel(self.tab_2)
        self.label.setGeometry(QtCore.QRect(10, 70, 241, 91))
        self.label.setObjectName("label")
        self.pushButton = QtGui.QPushButton(self.tab_2)
        self.pushButton.setGeometry(QtCore.QRect(260, 100, 105, 25))
        self.pushButton.setObjectName("pushButton")
        self.tabWidget.addTab(self.tab_2, "")
        self.tab_3 = QtGui.QWidget()
        self.tab_3.setObjectName("tab_3")
        self.label_msg_search = QtGui.QLabel(self.tab_3)
        self.label_msg_search.setGeometry(QtCore.QRect(10, 20, 175, 31))
        self.label_msg_search.setObjectName("label_msg_search")
        self.label_ext = QtGui.QLabel(self.tab_3)
        self.label_ext.setGeometry(QtCore.QRect(10, 60, 132, 16))
        self.label_ext.setObjectName("label_ext")
        self.pushButton_slct = QtGui.QPushButton(self.tab_3)
        self.pushButton_slct.setGeometry(QtCore.QRect(150, 160, 105, 31))
        self.pushButton_slct.setObjectName("pushButton_slct")
        self.pushButton_deslct = QtGui.QPushButton(self.tab_3)
        self.pushButton_deslct.setGeometry(QtCore.QRect(150, 244, 105, 31))
        self.pushButton_deslct.setObjectName("pushButton_deslct")
        self.label_2 = QtGui.QLabel(self.tab_3)
        self.label_2.setGeometry(QtCore.QRect(270, 80, 111, 16))
        self.label_2.setObjectName("label_2")
        self.list_unsearch = QtGui.QListWidget(self.tab_3)
        self.list_unsearch.setGeometry(QtCore.QRect(10, 110, 131, 251))
        self.list_unsearch.setObjectName("list_unsearch")
        self.list_search = QtGui.QListWidget(self.tab_3)
        self.list_search.setGeometry(QtCore.QRect(300, 110, 141, 251))
        self.list_search.setObjectName("list_search")
        self.tabWidget.addTab(self.tab_3, "")
        self.verticalLayout.addWidget(self.tabWidget)
        self.buttonBox = QtGui.QDialogButtonBox(Dialog)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(Dialog)
        self.tabWidget.setCurrentIndex(2)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), Dialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "Dialog", None, QtGui.QApplication.UnicodeUTF8))
        self.loadlastCheckbox.setText(QtGui.QApplication.translate("Dialog", "打开上一次的标签页", None, QtGui.QApplication.UnicodeUTF8))
        self.openRemoteCheckbox.setText(QtGui.QApplication.translate("Dialog", "打开外部链接", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), QtGui.QApplication.translate("Dialog", "启动", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("Dialog", "TextLabel", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton.setText(QtGui.QApplication.translate("Dialog", "选择", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), QtGui.QApplication.translate("Dialog", "字体", None, QtGui.QApplication.UnicodeUTF8))
        self.label_msg_search.setText(QtGui.QApplication.translate("Dialog", "默认使用自己的搜索引擎，\n"
"支持正则表达式搜索（python）", None, QtGui.QApplication.UnicodeUTF8))
        self.label_ext.setText(QtGui.QApplication.translate("Dialog", "选择要搜索的文件的后缀", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_slct.setText(QtGui.QApplication.translate("Dialog", ">>>", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_deslct.setText(QtGui.QApplication.translate("Dialog", "<<<", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("Dialog", "要搜索的文件的后缀", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), QtGui.QApplication.translate("Dialog", "搜索", None, QtGui.QApplication.UnicodeUTF8))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    Dialog = QtGui.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())

