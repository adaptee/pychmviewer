#!/usr/bin/python
# coding: utf8
#########################################################################
# Author: Xinyu.Xiang(John)
# email: zorrohunter@gmail.com
# Created Time: 2009年05月30日 星期六 03时26分16秒
# File Name: pychmindex.py
# Description:
#########################################################################
from PyQt4.QtGui import QTreeWidgetItem
from PyQt4 import QtCore, QtGui

import globalvalue
from pychmselecttopic import PyChmSlctTopicDlg
from utils import getchmfile, getmainwindow
from Ui_tab_index import Ui_TabIndex

class PyChmIdxView(QtGui.QWidget, Ui_TabIndex):
    '''
    signal 'openUrl' will be emited(with param url:unicode) when the index item be doubleclicked
    '''
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.setupUi(self)
        self.tree.headerItem().setHidden(True)
        self.lastitem = None
        self.dataloaded = False
        self.connect(self.tree, QtCore.SIGNAL('itemDoubleClicked(QTreeWidgetItem*,int)'), self.onDoubleClicked)
        self.connect(self.text, QtCore.SIGNAL('textChanged(const QString&)'), self.onTextChanged)
        self.connect(self.text, QtCore.SIGNAL('returnPressed()'), self.onReturnPressed)

        chmfile = getchmfile()

        if not chmfile or self.dataloaded :
            return
        if chmfile.hasIndex :
            self.loaddata(chmfile.index)

    def clear(self):
        '''
        clear the data in the index view
        '''
        self.tree.clear()
        self.dataloaded = False
        self.text.clear()

    def onTextChanged(self, v):
        '''
        inner method for search item
        '''
        items = self.tree.findItems(v, QtCore.Qt.MatchStartsWith)
        if items:
            self.tree.setCurrentItem(items[0])
            self.tree.scrollToItem(items[0])
            self.lastitem = items[0]
        else:
            self.lastitem = None

    def onReturnPressed(self):
        '''
        inner method for openurl
        '''
        if self.lastitem :
            item = self.lastitem
            if len(item.entry.urls) == 1:
                self.emit(QtCore.SIGNAL('openUrl'), item.entry.urls[0][1])
                return
            elif len(item.entry.urls)>1:
                main_window = getmainwindow()
                dlg = PyChmSlctTopicDlg(main_window)
                titles = [a for a, b in item.entry.urls]
                urls = [b for a, b in item.entry.urls]
                url = dlg.getUrl(titles, urls)
                if url :
                    self.emit(QtCore.SIGNAL('openUrl'), url)
                    return url

    def onDoubleClicked(self, item, col):
        '''
        inner method for openurl
        '''
        if item is None:
            return
        if item.isExpanded():
            item.setExpanded(False)
        if len(item.entry.urls) == 1:
            self.emit(QtCore.SIGNAL('openUrl'), item.entry.urls[0][1])
            return
        elif len(item.entry.urls)>1:
            main_window = getmainwindow()
            dlg = PyChmSlctTopicDlg(main_window)
            titles = [a for a, b in item.entry.urls]
            urls = [b for a, b in item.entry.urls]
            url = dlg.getUrl(titles, urls)
            if url:
                self.emit(QtCore.SIGNAL('openUrl'), url)
                return url

    def loaddata(self, data):
        '''
        load data for index tree.
        data is list of TableEntry(define in pychmfile.py
        '''
        if self.dataloaded:
            return
        if not data :
            return
        self.dataloaded = True
        self.tree.clear()
        lastchild = []
        rootentry = []
        for i in xrange(len(data)):
            indent = data[i].indent
            if indent >= len(rootentry):
                maxindent = len(rootentry)-1
                lastchild.append(None)
                rootentry.append(None)
                if indent > 0 and maxindent < 0:
                    print 'error, first entry isn\'t the root entry'
                if (indent-maxindent) > 1:
                    j = maxindent
                    while j < indent:
                        if len(lastchild)<=j+1:
                            lastchild.append(None)
                            rootentry.append(None)
                        lastchild[j+1] = lastchild[j]
                        rootentry[j+1] = rootentry[j]
                        j += 1
                lastchild[indent] = None
                rootentry[indent] = None
            if indent == 0:
                item = QTreeWidgetItem(self.tree, lastchild[indent])
                item.entry = data[i]
                item.setText(0, data[i].key)
            else:
                if rootentry[indent-1] is None:
                    print 'error no root entry'
                item = QTreeWidgetItem(rootentry[indent-1], lastchild[indent])
                item.entry = data[i]
                item.setText(0, data[i].key)
            item.setExpanded(True)
            lastchild[indent] = item
            rootentry[indent] = item
        self.tree.update()


if __name__  ==  "__main__":
    import sys
    import locale
    from pychmfile import PyChmFile

    default_encoding = locale.getdefaultlocale()[1]

    if len(sys.argv) > 1:

        globalvalue.chmpath = sys.argv[1].decode(default_encoding)
        globalvalue.chmFile = PyChmFile()
        globalvalue.chmFile.loadFile(globalvalue.chmpath)

        app = QtGui.QApplication(sys.argv)
        IDX = PyChmIdxView()
        IDX.show()
        sys.exit(app.exec_())


