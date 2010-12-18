#!/usr/bin/python
# vim: set fileencoding=utf-8 :

from PyQt4 import QtGui
from PyQt4.QtGui import QTreeWidgetItem

from utils import remove_anchor
from treeview import AbstractTreeView
from Ui_paneltopics import Ui_PanelTopics


def normalize_key(key):
    if key and key[0] != u'/':
        key = u'/' + key

    return remove_anchor(key)

class PyChmTopicsView(AbstractTreeView, Ui_PanelTopics):
    '''
    signal 'openURL' will be emited(with param url:unicode)
    when the index item be doubleclicked
    '''

    class URLDict(object):
        "map url to some item in the topicsview"
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

    def __init__(self, mainwin=None, parent=None):
        AbstractTreeView.__init__(self, parent)

        self.mainwin = mainwin
        if mainwin.currentView:
            chmfile = mainwin.currentView.chmfile
            if chmfile and chmfile.index :
                self.loadTopics(chmfile.index)

        self.url2item = PyChmTopicsView.URLDict()

    def locateTopicByURL(self, qurl):
        path = unicode(qurl.path() )
        item = self.url2item.get(path, None)
        if item :
            self._updateParentStatus(item)
            self.tree.setCurrentItem(item)
            self.tree.scrollToItem(item)

    def _updateParentStatus(self, item):
        parent = item.parent()
        while parent :
            parent.setExpanded(True)
            parent = parent.parent()

    def onTabSwitched(self):
        "update topics in correspondance with current chmfile "
        self.clear()

        if self.mainwin.currentView:
            chmfile = self.mainwin.currentView.chmfile
            self.loadTopics(chmfile.topics)

    def clear(self):
        "clear underlying data  "
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

            self.loadNode(child, item)

            prev = item

if __name__  ==  "__main__":
    raise NotImplementedError()
