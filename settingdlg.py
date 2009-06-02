#!/usr/bin/python
# coding: utf8
#########################################################################
# Author: Xinyu.Xiang(John)
# email: zorrohunter@gmail.com
# Created Time: 2009年06月02日 星期二 05时17分07秒
# File Name: settingdlg.py
# Description: 
#########################################################################

from Ui_settingdlg import Ui_Dialog
from PyQt4 import QtCore, QtGui
import globalvalue

class SettingDlg(QtGui.QDialog,Ui_Dialog):
    def __init__(self,parent=None):
        QtGui.QDialog.__init__(self,parent)
        self.setupUi(self)
        self.loadlastCheckbox.setChecked(globalvalue.globalcfg.loadlasttime)
        self.openRemoteCheckbox.setChecked(globalvalue.globalcfg.openremote)
        self.loadlasttime=globalvalue.globalcfg.loadlasttime
        self.openremote=globalvalue.globalcfg.openremote
        s=u'font family: '
        if globalvalue.globalcfg.fontfamily:
            s=s+globalvalue.globalcfg.fontfamily
        else:
            s=s+u'default'
        self.fontfamily=globalvalue.globalcfg.fontfamily
        s=s+u"\nfont size:"
        if globalvalue.globalcfg.fontsize:
            s=s+str(globalvalue.globalcfg.fontsize)
        else:
            s=s+u'default'
        self.fontsize=globalvalue.globalcfg.fontsize
        self.label.setText(s)
        self.connect(self.pushButton,QtCore.SIGNAL('clicked()'),self.fontSelect)
        self.connect(self.loadlastCheckbox,QtCore.SIGNAL('clicked()'),self.onLoadLast)
        self.connect(self.openRemoteCheckbox,QtCore.SIGNAL('clicked()'),self.onOpenRemote)

    def onLoadLast(self):
        if self.loadlastCheckbox.isChecked():
            self.loadlasttime=True
        else:
            self.loadlasttime=False

    def onOpenRemote(self):
        if self.openRemoteCheckbox.isChecked():
            self.openremote=True
        else:
            self.openremote=False
        #self.msglabel.setText(u'重启后生效')


    def fontSelect(self):
        font,ok=QtGui.QFontDialog.getFont(self)
        if ok:
            self.fontfamily=font.family()
            self.fontsize=font.pixelSize()
            if self.fontsize==-1:
                self.fontsize=font.pointSize()
            s=u'font family: '+self.fontfamily+u'\nfont size: '+str(self.fontsize)
            self.label.setText(s)


if __name__=="__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    Dialog =SettingDlg()
    Dialog.show()
    sys.exit(app.exec_())

