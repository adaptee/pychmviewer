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

        self.session_restore = self.config.session_restore
        self.openremote = self.config.openremote

        self.fontfamily = self.config.fontfamily
        self.fontsize = self.config.fontsize

        self.sessionRestoreCheckbox.setChecked(self.session_restore)
        self.openRemoteURLCheckbox.setChecked(self.openremote)
        self.fontInfoLabel.setText( get_fontinfo(self.config) )

        self.connect(self.selectFontButton, QtCore.SIGNAL('clicked()'), self.selectFont)
        self.connect(self.sessionRestoreCheckbox, QtCore.SIGNAL('clicked()'), self.toggleSessionRestore)
        self.connect(self.openRemoteURLCheckbox, QtCore.SIGNAL('clicked()'), self.toggleOpenRemoteURl)

    def toggleSessionRestore(self):
        self.session_restore = self.sessionRestoreCheckbox.isChecked()

    def toggleOpenRemoteURl(self):
        self.openremote = self.openRemoteURLCheckbox.isChecked()

    def selectFont(self):
        font, ok = QtGui.QFontDialog.getFont(self)
        if ok:
            self.fontfamily = font.family()
            self.fontsize = font.pixelSize()
            if self.fontsize == -1 :
                self.fontsize = font.pointSize()
            fontinfo = stringlize_fontinfo(self.fontfamily, self.fontsize)
            self.fontInfoLabel.setText(fontinfo)

if __name__ == "__main__":
    raise NotImplementedError("")
