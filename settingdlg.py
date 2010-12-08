#!/usr/bin/python
# coding: utf8
#########################################################################
# Author: Xinyu.Xiang(John)
# email: zorrohunter@gmail.com
# Created Time: 2009年06月02日 星期二 05时17分07秒
# File Name: settingdlg.py
# Description:
#########################################################################

from PyQt4 import QtCore, QtGui
from PyQt4.QtGui import QListWidgetItem

import globalvalue
from Ui_settingdlg import Ui_Dialog

class SettingDlg(QtGui.QDialog, Ui_Dialog):
    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self, parent)
        self.setupUi(self)
        self.loadlastCheckbox.setChecked(globalvalue.globalcfg.loadlasttime)
        self.openRemoteCheckbox.setChecked(globalvalue.globalcfg.openremote)

        self.sengine_own = globalvalue.globalcfg.sengine_own
        self.searchext = globalvalue.globalcfg.searchext
        if self.sengine_own:
            self.check_searchengine.setChecked(False)
            self.pushButton_slct.setEnabled(True)
            self.pushButton_deslct.setEnabled(True)
        else:
            self.check_searchengine.setChecked(True)
            self.pushButton_slct.setEnabled(False)
            self.pushButton_deslct.setEnabled(False)

        self.loadlasttime = globalvalue.globalcfg.loadlasttime
        self.openremote = globalvalue.globalcfg.openremote

        text = u'font family: '
        if globalvalue.globalcfg.fontfamily:
            text = text + globalvalue.globalcfg.fontfamily
        else:
            text = text + u'default'
        self.fontfamily = globalvalue.globalcfg.fontfamily
        text = text + u"\nfont size:"
        if globalvalue.globalcfg.fontsize:
            text = text + str(globalvalue.globalcfg.fontsize)
        else:
            text = text + u'default'
        self.label.setText(text)

        self.fontsize = globalvalue.globalcfg.fontsize
        self.connect(self.pushButton, QtCore.SIGNAL('clicked()'), self.fontSelect)
        self.connect(self.loadlastCheckbox, QtCore.SIGNAL('clicked()'), self.onLoadLast)
        self.connect(self.openRemoteCheckbox, QtCore.SIGNAL('clicked()'), self.onOpenRemote)
        self.connect(self.check_searchengine, QtCore.SIGNAL('clicked()'), self.onSlctEngine)
        self.connect(self.pushButton_slct, QtCore.SIGNAL('clicked()'), self.onSlctExt)
        self.connect(self.pushButton_deslct, QtCore.SIGNAL('clicked()'), self.onUnSlctExt)
        for a, b in self.searchext.iteritems():
            if b:
                item = QListWidgetItem(self.list_search)
                item.setText(a)
            else:
                item = QListWidgetItem(self.list_unsearch)
                item.setText(a)

    def onSlctExt(self):
        item = self.list_unsearch.currentItem()
        if item is None:
            return
        ext = str(item.text())
        nit = QListWidgetItem(self.list_search)
        nit.setText(ext)
        self.list_unsearch.takeItem(self.list_unsearch.row(item))
        self.searchext[ext] = True

    def onUnSlctExt(self):
        item = self.list_search.currentItem()
        if item is None:
            return
        ext = str(item.text())
        nit = QListWidgetItem(self.list_unsearch)
        nit.setText(ext)
        self.list_search.takeItem(self.list_search.row(item))
        self.searchext[ext] = False


    def onSlctEngine(self):
        if self.check_searchengine.isChecked():
            self.sengine_own = False
            self.pushButton_slct.setEnabled(False)
            self.pushButton_deslct.setEnabled(False)
        else:
            self.sengine_own = True
            self.pushButton_slct.setEnabled(True)
            self.pushButton_deslct.setEnabled(True)

    def onLoadLast(self):
        if self.loadlastCheckbox.isChecked():
            self.loadlasttime = True
        else:
            self.loadlasttime = False

    def onOpenRemote(self):
        if self.openRemoteCheckbox.isChecked():
            self.openremote = True
        else:
            self.openremote = False
        self.msglabel.setText(u'重启后生效')


    def fontSelect(self):
        font, ok = QtGui.QFontDialog.getFont(self)
        if ok:
            self.fontfamily = font.family()
            self.fontsize = font.pixelSize()
            if self.fontsize == -1:
                self.fontsize = font.pointSize()
            text = u'font family: ' + self.fontfamily + u'\nfont size: ' + str(self.fontsize)
            self.label.setText(text)


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    Dialog = SettingDlg()
    Dialog.show()
    sys.exit(app.exec_())

