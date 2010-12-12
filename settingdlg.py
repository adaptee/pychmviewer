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

from Ui_settingdlg import Ui_Dialog

def get_fontinfo(config):
    family = config.fontfamily or "default"
    size   = config.fontsize or "default"
    return stringlize_fontinfo(family, size)

def stringlize_fontinfo(family, size):
    template = u"Font family: %s\nFont size: %s"
    return template % (family, size)


class SettingDlg(QtGui.QDialog, Ui_Dialog):
    def __init__(self, mainwin, parent=None):
        QtGui.QDialog.__init__(self, parent)
        self.setupUi(self)

        self.config  = mainwin.session.config

        self.loadlasttime = self.config.loadlasttime
        self.openremote = self.config.openremote

        self.fontfamily = self.config.fontfamily
        self.fontsize = self.config.fontsize


        self.loadlastCheckbox.setChecked(self.loadlasttime)
        self.openRemoteCheckbox.setChecked(self.openremote)
        self.label.setText( get_fontinfo(self.config) )

        self.connect(self.pushButton, QtCore.SIGNAL('clicked()'), self.selectFont)
        self.connect(self.loadlastCheckbox, QtCore.SIGNAL('clicked()'), self.onLoadLast)
        self.connect(self.openRemoteCheckbox, QtCore.SIGNAL('clicked()'), self.onOpenRemote)

    def onLoadLast(self):
        self.loadlasttime = self.loadlastCheckbox.isChecked()

    def onOpenRemote(self):
        self.openremote = self.openRemoteCheckbox.isChecked()

    def selectFont(self):
        font, ok = QtGui.QFontDialog.getFont(self)
        if ok:
            self.fontfamily = font.family()
            self.fontsize = font.pixelSize()
            if self.fontsize == -1 :
                self.fontsize = font.pointSize()
            fontinfo = stringlize_fontinfo(self.fontfamily, self.fontsize)
            self.label.setText(fontinfo)

if __name__ == "__main__":
    raise NotImplementedError("")
