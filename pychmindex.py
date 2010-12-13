#!/usr/bin/python
# coding: utf8
#########################################################################
# Author: Xinyu.Xiang(John)
# email: zorrohunter@gmail.com
# Created Time: 2009年05月30日 星期六 03时26分16秒
# File Name: pychmindex.py
# Description:
#########################################################################
from PyQt4 import QtCore, QtGui

from treeview import AbstractTreeView
from Ui_tab_index import Ui_TabIndex

class PyChmIndexView(QtGui.QWidget, Ui_TabIndex, AbstractTreeView):
    '''
    signal 'openUrl' will be emited(with param url:unicode) when the index item be doubleclicked
    '''
    def __init__(self, mainwin=None, parent=None):
        QtGui.QWidget.__init__(self, parent)
        AbstractTreeView.__init__(self)
        self.connect(self.text, QtCore.SIGNAL('textChanged(const QString&)'), self.onTextChanged)
        self.connect(self.text, QtCore.SIGNAL('returnPressed()'), self.onReturnPressed)

        self.lastitem = None

        #experimental
        self.mainwin = mainwin

        chmfile = mainwin.currentView.chmfile
        if chmfile and chmfile.index :
            self.loadIndex(chmfile.index)

    def onTabSwitched(self):
        chmfile = self.mainwin.currentView.chmfile
        self.loadIndex(chmfile.index)

    def clear(self):
        '''
        clear the data in the index view
        '''
        AbstractTreeView.clear(self)
        self.text.clear()

    loadIndex = AbstractTreeView.loadData


    #FIXME; I feel somthing wrong these 2 functions related with `lastitem`
    def onTextChanged(self, text):
        '''
        inner method for search item
        '''
        items = self.tree.findItems(text, QtCore.Qt.MatchStartsWith)
        if items:
            item = items[0]
            self.tree.setCurrentItem(item)
            self.tree.scrollToItem(item)
            self.lastitem = item
        else:
            self.lastitem = None
    def onReturnPressed(self):
        '''
        inner method for openurl
        '''
        if self.lastitem :
            item = self.lastitem
            self.emit(QtCore.SIGNAL('openUrl'), item.entry.url)


if __name__  ==  "__main__":
    import sys

    from pychmfile import PyChmFile
    from session import system_encoding

    if len(sys.argv) > 1:

        path = sys.argv[1].decode(system_encoding)
        chmfile = PyChmFile(path)

        app = QtGui.QApplication(sys.argv)
        IDX = PyChmIndexView()
        IDX.show()
        sys.exit(app.exec_())


