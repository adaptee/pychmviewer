#!/usr/bin/python
# coding: utf8
#########################################################################
# Author: Xinyu.Xiang(John)
# email: zorrohunter@gmail.com
# Created Time: 2009年06月02日 星期二 06时45分13秒
# File Name: about.py
# Description: 
#########################################################################
from Ui_about import Ui_Dialog
from PyQt4 import QtCore, QtGui
class aboutdlg(QtGui.QDialog,Ui_Dialog):
    def __init__(self,parent=None):
        QtGui.QDialog.__init__(self,parent)
        self.setupUi(self)