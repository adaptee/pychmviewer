#!/usr/bin/python
# coding: utf8
#########################################################################
# Author: Xinyu.Xiang(John)
# email: zorrohunter@gmail.com
# Created Time: 2009年06月02日 星期二 03时10分59秒
# File Name: htmldlg.py
# Description:
#########################################################################

from PyQt4 import QtCore, QtGui

from Ui_htmlsourcedlg import Ui_Dialog

class HtmlDlg(QtGui.QDialog, Ui_Dialog):
    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self, parent)
        self.setupUi(self)
