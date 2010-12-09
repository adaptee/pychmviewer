#!/usr/bin/python
# coding: utf8
#########################################################################
# Author: Xinyu.Xiang(John)
# email: zorrohunter@gmail.com
# Created Time: 2009年05月29日 星期五 23时52分15秒
# File Name: pychmtopics.py
# Description:
#########################################################################
from PyQt4 import QtCore, QtGui
from PyQt4.QtGui import QTreeWidgetItem

import globalvalue
from pychmselecttopic import PyChmSlctTopicDlg
from utils import remove_comment, getchmfile, getmainwindow
from Ui_tab_contents import Ui_TabContents


def normalize_key(key):
    if key and key[0] != u'/':
        key = u'/' + key

    return remove_comment(key)


class PyChmTopicsView(QtGui.QWidget, Ui_TabContents):
    '''
    signal 'openUrl' will be emited(with param url:unicode) when the index item be doubleclicked
    '''

    class __UrlDict(object):
        '''
        for inner use
        '''
        def __init__(self):
            self.cmap = {}

        def get(self, key, default):
            key = normalize_key(key)
            return self.cmap.get(key, default)

        def __getitem__(self, key):
            key = normalize_key(key)
            return self.cmap[key]

        def __setitem__(self, key, value):
            key = normalize_key(key)

            if not key in self.cmap:
                self.cmap[key] = value

    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.setupUi(self)
        self.urlmap = PyChmTopicsView.__UrlDict()
        self.tree.headerItem().setHidden(True)
        self.dataloaded = False
        self.connect(self.tree, QtCore.SIGNAL('itemDoubleClicked(QTreeWidgetItem*,int)'), self.onDoubleClicked)

        chmfile = getchmfile()
        if not chmfile or self.dataloaded:
            return
        if chmfile.topic :
            self.loaddata(chmfile.topic)

    def locateUrl(self, url):
        '''
        this method is to locate the item who has the given url
        '''
        item = self.urlmap.get(url, None)
        if item :
            self._updateParentStatus(item)
            self.tree.setCurrentItem(item)
            self.tree.scrollToItem(item)


    def _updateParentStatus(item):
        parent = item.parent()
        while parent :
            parent.setExpanded(True)
            parent = parent.parent()

    def onDoubleClicked(self, item, col):
        '''
        inner method
        '''
        if not item :
            return
        if len(item.entry.urls) == 1:
            self.emit(QtCore.SIGNAL('openUrl'), item.entry.urls[0][1])
            return
        elif len(item.entry.urls) > 1:
            main_window = getmainwindow()
            dialog = PyChmSlctTopicDlg(main_window)
            # FIXME; zip(*item.entry.urls) is a better solution ?
            titles = [a for a, b in item.entry.urls]
            urls = [b for a, b in item.entry.urls]

            url = dialog.getUrl(titles, urls)

            if url:
                self.emit(QtCore.SIGNAL('openUrl'), url)
                return url


    def clear(self):
        '''
        clear the data in the index view
        '''
        self.tree.clear()
        self.dataloaded = False

    def loaddata(self, data):
        '''
        load data for topics tree.
        data is list of TableEntry(define in pychmfile.py
        '''
        if self.dataloaded:
            return

        self.tree.clear()
        if not data:
            return

        self.urlmap = PyChmTopicsView.__UrlDict()

        lastchild = []
        rootentry = []

        for i in xrange(len(data)):
            indent = data[i].indent
            if indent >= len(rootentry):
                maxindent = len(rootentry) - 1
                lastchild.append(None)
                rootentry.append(None)
                if indent > 0 and maxindent < 0:
                    print 'error, first entry isn\'t the root entry'
                if (indent - maxindent) > 1:
                    j = maxindent
                    while j < indent:
                        if len(lastchild) <= j+1:
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
            for nm, url in data[i].urls:
                self.urlmap[url] = item
            lastchild[indent] = item
            rootentry[indent] = item

        self.tree.update()

        self.dataloaded = True

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
        TC = PyChmTopicsView()
        TC.show()
        sys.exit(app.exec_())


