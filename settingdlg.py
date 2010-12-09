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
from utils import getcfg
from Ui_settingdlg import Ui_Dialog

# FIXME; ugly name and location
def get_font_info(config):
    family = config.fontfamily or "default"
    size   = config.fontsize or "default"
    return family, size

def stringlize_font_info(family, size):
    template = u"Font family: %s\nFont size: %s"
    return template % (family, size)



class SettingDlg(QtGui.QDialog, Ui_Dialog):
    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self, parent)
        self.setupUi(self)

        self.config = getcfg()
        self.loadlastCheckbox.setChecked(self.config.loadlasttime)
        self.openRemoteCheckbox.setChecked(self.config.openremote)

        self.searchext = self.config.searchext

        self.loadlasttime = self.config.loadlasttime
        self.openremote = self.config.openremote

        self.fontfamily = self.config.fontfamily
        self.fontsize = self.config.fontsize

        text = stringlize_font_info(*get_font_info(self.config))
        self.label.setText(text)

        self.connect(self.pushButton, QtCore.SIGNAL('clicked()'), self.fontSelect)
        self.connect(self.loadlastCheckbox, QtCore.SIGNAL('clicked()'), self.onLoadLast)
        self.connect(self.openRemoteCheckbox, QtCore.SIGNAL('clicked()'), self.onOpenRemote)
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
        if not item :
            return
        ext = str(item.text())
        nit = QListWidgetItem(self.list_search)
        nit.setText(ext)
        self.list_unsearch.takeItem(self.list_unsearch.row(item))
        self.searchext[ext] = True

    def onUnSlctExt(self):
        item = self.list_search.currentItem()
        if not item :
            return
        ext = str(item.text())
        nit = QListWidgetItem(self.list_unsearch)
        nit.setText(ext)
        self.list_search.takeItem(self.list_search.row(item))
        self.searchext[ext] = False

    def onLoadLast(self):
        if self.loadlastCheckbox.isChecked():
            self.loadlasttime = True
        else:
            self.loadlasttime = False

    def onOpenRemote(self):
        self.openremote = True if self.openRemoteCheckbox.isChecked() else False
        self.msglabel.setText(u'重启后生效')


    def fontSelect(self):
        font, ok = QtGui.QFontDialog.getFont(self)
        if ok:
            self.fontfamily = font.family()
            self.fontsize = font.pixelSize()
            if self.fontsize == -1:
                self.fontsize = font.pointSize()
            text = stringlize_font_info(self.fontfamily, self.fontsize)
            self.label.setText(text)


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    Dialog = SettingDlg()
    Dialog.show()
    sys.exit(app.exec_())

