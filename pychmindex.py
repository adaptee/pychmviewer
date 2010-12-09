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
from PyQt4.QtGui import QTreeWidgetItem

import globalvalue
from utils import getchmfile
from Ui_tab_index import Ui_TabIndex

class PyChmIdxView(QtGui.QWidget, Ui_TabIndex):
    '''
    signal 'openUrl' will be emited(with param url:unicode) when the index item be doubleclicked
    '''
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.setupUi(self)
        self.tree.headerItem().setHidden(True)
        self.connect(self.tree, QtCore.SIGNAL('itemDoubleClicked(QTreeWidgetItem*,int)'), self.onDoubleClicked)
        self.connect(self.text, QtCore.SIGNAL('textChanged(const QString&)'), self.onTextChanged)
        self.connect(self.text, QtCore.SIGNAL('returnPressed()'), self.onReturnPressed)

        self.lastitem = None
        self.dataloaded = False

        chmfile = getchmfile()
        if chmfile and chmfile.index :
            self.loaddata(chmfile.index)

    def clear(self):
        '''
        clear the data in the index view
        '''
        self.tree.clear()
        self.text.clear()
        self.dataloaded = False

    def onTextChanged(self, v):
        '''
        inner method for search item
        '''
        items = self.tree.findItems(v, QtCore.Qt.MatchStartsWith)
        if items:
            #FIXME; I feel somthing wrong here
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
        #FIXME; I feel somthing wrong here
        if self.lastitem :
            item = self.lastitem
            self.emit(QtCore.SIGNAL('openUrl'), item.entry.url)

    def onDoubleClicked(self, item, _col):
        if item :
            url = item.entry.url
            self.emit(QtCore.SIGNAL('openUrl'), url)

    def loaddata(self, tree):
        "load data for topics tree."
        if self.dataloaded:
            return

        if tree:
            self.clear()

            self._loadNode(node=tree, parent=None)

            self.tree.update()
            self.dataloaded = True

    def _loadNode(self, node, parent):
        # special case for the root of tree
        if not parent:
            parent = self.tree

        prev = None
        for child in node.children:
            # insert below `parent`, after `prev`
            item = QTreeWidgetItem(parent, prev)

            item.entry = child
            item.setText(0, child.name)
            #if child.url :
                #self.url2item[child.url] = item

            self._loadNode(child, item)

            prev = item

if __name__  ==  "__main__":
    import sys

    from pychmfile import PyChmFile
    from session import system_encoding

    if len(sys.argv) > 1:

        globalvalue.chmpath = sys.argv[1].decode(system_encoding)
        globalvalue.chmFile = PyChmFile()
        globalvalue.chmFile.loadFile(globalvalue.chmpath)

        app = QtGui.QApplication(sys.argv)
        IDX = PyChmIdxView()
        IDX.show()
        sys.exit(app.exec_())


