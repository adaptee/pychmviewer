#!/usr/bin/python
# coding: utf8
#########################################################################
# Author: Xinyu.Xiang(John)
# email: zorrohunter@gmail.com
# Created Time: 2009年05月29日 星期五 23时52分15秒
# File Name: pychmtopics.py
# Description:
#########################################################################
from PyQt4 import QtGui
from PyQt4.QtGui import QTreeWidgetItem

import globalvalue
from utils import remove_comment, getchmfile
from treeview import AbstractTreeView
from Ui_tab_contents import Ui_TabContents


def normalize_key(key):
    if key and key[0] != u'/':
        key = u'/' + key

    return remove_comment(key)


class PyChmTopicsView(QtGui.QWidget, Ui_TabContents, AbstractTreeView):
    '''
    signal 'openUrl' will be emited(with param url:unicode) when the index item be doubleclicked
    '''

    class URLDict(object):
        '''
        for inner use
        '''
        def __init__(self):
            self.map = { }

        def get(self, key, default):
            key = normalize_key(key)
            return self.map.get(key, default)

        def __getitem__(self, key):
            key = normalize_key(key)
            return self.map[key]

        def __setitem__(self, key, value):
            key = normalize_key(key)
            # this dict does not allow overwriting
            if not key in self.map:
                self.map[key] = value

        def clear(self):
            del self.map
            self.map = { }

    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        AbstractTreeView.__init__(self)

        self.url2item = PyChmTopicsView.URLDict()

        chmfile = getchmfile()
        if chmfile and chmfile.topics:
            self.loadTopics(chmfile.topics)

    def locateUrl(self, url):
        '''
        this method is to locate the item who has the given url
        '''
        item = self.url2item.get(url, None)
        if item :
            self._updateParentStatus(item)
            self.tree.setCurrentItem(item)
            self.tree.scrollToItem(item)

    def _updateParentStatus(self, item):
        parent = item.parent()
        while parent :
            parent.setExpanded(True)
            parent = parent.parent()

    def clear(self):
        '''
        clear the data in the index view
        '''
        AbstractTreeView.clear(self)
        self.url2item.clear()

    loadTopics = AbstractTreeView.loadData

    def loadNode(self, node, parent):
        # special case for the root of tree
        if not parent:
            parent = self.tree

        prev = None
        for child in node.children:
            # insert below `parent`, after `prev`
            item = QTreeWidgetItem(parent, prev)

            item.entry = child
            item.setText(0, child.name)
            if child.url :
                self.url2item[child.url] = item

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
        TC = PyChmTopicsView()
        TC.show()
        sys.exit(app.exec_())


