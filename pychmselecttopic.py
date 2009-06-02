#!/usr/bin/python
# coding: utf8
#########################################################################
# Author: Xinyu.Xiang(John)
# email: zorrohunter@gmail.com
# Created Time: 2009年05月30日 星期六 04时10分22秒
# File Name: pychmselecttopic.py
# Description: 
#########################################################################
from Ui_dialog_topicselector import Ui_DialogTopicSelector
from PyQt4 import QtCore, QtGui

class PyChmSlctTopicDlg(QtGui.QDialog,Ui_DialogTopicSelector):
    '''
    the dialog is for multiselection entry (in index tree or topics tree)
    '''
    def __init__(self,parent):
        QtGui.QDialog.__init__(self,parent)
        self.setupUi(self)
        self.connect(self.list,QtCore.SIGNAL('itemDoubleClicked(QListWidgetItem*)'),self.onDoubleClicked)

    def onDoubleClicked(self,item):
        if item!=None:
            accept()

    def getUrl(self,titles,urllist):
        for x in titles:
            self.list.addItem(x)
        if self.exec_()==QtGui.QDialog.Accepted and self.list.currentRow()!=-1:
            return urllist[self.list.currentRow()]
        return None
