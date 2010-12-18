#!/usr/bin/python
# vim: set fileencoding=utf-8 :

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

        self.sessionRestore = self.config.sessionRestore
        self.openRemoteURL = self.config.openRemoteURL

        self.fontfamily = self.config.fontfamily
        self.fontsize = self.config.fontsize

        self.sessionRestoreCheckbox.setChecked(self.sessionRestore)
        self.openRemoteURLCheckbox.setChecked(self.openRemoteURL)
        self.fontInfoLabel.setText( get_fontinfo(self.config) )

        self.connect(self.selectFontButton,
                     QtCore.SIGNAL('clicked()'),
                     self.selectFont)
        self.connect(self.sessionRestoreCheckbox,
                     QtCore.SIGNAL('clicked()'),
                     self.toggleSessionRestore)
        self.connect(self.openRemoteURLCheckbox,
                     QtCore.SIGNAL('clicked()'),
                     self.toggleOpenRemoteURl)

    def toggleSessionRestore(self):
        self.sessionRestore = self.sessionRestoreCheckbox.isChecked()

    def toggleOpenRemoteURl(self):
        self.openRemoteURL = self.openRemoteURLCheckbox.isChecked()

    def selectFont(self):
        font, ok = QtGui.QFontDialog.getFont(self)
        if ok:
            self.fontfamily = font.family()
            self.fontsize = font.pixelSize()
            if self.fontsize == -1 :
                self.fontsize = font.pointSize()
            fontinfo = stringlize_fontinfo(self.fontfamily, self.fontsize)
            self.fontInfoLabel.setText(fontinfo)

