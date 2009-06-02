#!/usr/bin/python
# coding: utf8
#########################################################################
# Author: Xinyu.Xiang(John)
# email: zorrohunter@gmail.com
# Created Time: 2009年05月30日 星期六 20时10分26秒
# File Name: pychmsearch.py
# Description: 
#########################################################################
from Ui_tab_search import Ui_TabSearch
from PyQt4 import QtCore, QtGui
from PyQt4.QtGui import QTreeWidgetItem
import globalvalue

class PyChmSearchView(QtGui.QWidget,Ui_TabSearch):
    def __init__(self,parent=None):
        QtGui.QWidget.__init__(self,parent)
        self.setupUi(self)
        self.searchBox.setFocus()
        self.connect(self.btnGo,QtCore.SIGNAL('clicked()'),self.onReturnPressed)
        self.connect(self.searchBox.lineEdit(),QtCore.SIGNAL('returnPressed()'),self.onReturnPressed)
        self.connect(self.tree,QtCore.SIGNAL('itemDoubleClicked(QTreeWidgetItem*,int)'),self.onDoubleClicked)

    def clear(self):
        self.tree.clear()
        self.searchBox.lineEdit().clear()

    def onReturnPressed(self):
        if not globalvalue.chmFile.IsSearchable():
            return
        text=self.searchBox.lineEdit().text()
        text=unicode(text).strip()
        if text==u'':
            return
        self.tree.clear()
        rt=globalvalue.chmFile.Search(text)
        for entry in rt:
            for url in entry.urls:
                item=QTreeWidgetItem(self.tree)            
                item.url=url
                item.setText(0,entry.key)
                item.setText(1,url)
        self.tree.update()

    def onDoubleClicked(self,item,col):
        if item==None:
            return
        self.emit(QtCore.SIGNAL('openUrl'),item.url)

if __name__ == "__main__":
    import sys
    from pychmfile import PyChmFile
    globalvalue.chmpath=u'sb.chm'
    globalvalue.chmFile=PyChmFile()
    globalvalue.chmFile.loadFile(globalvalue.chmpath)
    app = QtGui.QApplication(sys.argv)
    sch=PyChmSearchView()
    sch.show()
    sys.exit(app.exec_())


