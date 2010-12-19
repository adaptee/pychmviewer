#!/usr/bin/python
# vim: set fileencoding=utf-8 :

" Provides the topics panel. "

from PyQt4.QtGui import QTreeWidgetItem

from treeview import AbstractTreeView
from Ui_paneltopics import Ui_PanelTopics

class URLDict(object):
    " Map url to item. "
    def __init__(self):
        self.map = { }

    def get(self, key, default):
        " Similar to dict.get(). "
        return self.map.get(key, default)

    def __getitem__(self, key):
        return self.map[key]

    def __setitem__(self, key, value):
        " Overwriting is not allowed."
        if not key in self.map:
            self.map[key] = value

    def clear(self):
        " Clear all mappings. "
        del self.map
        self.map = { }

class PyChmTopicsView(AbstractTreeView, Ui_PanelTopics):
    " Implements the topics panel. "
    def __init__(self, mainwin=None, parent=None):
        AbstractTreeView.__init__(self, parent)

        self.mainwin = mainwin
        if mainwin.currentView:
            chmfile = mainwin.currentView.chmfile
            if chmfile and chmfile.index :
                self.loadTopics(chmfile.index)

        self.url2item = URLDict()

    def locateTopicByURL(self, qurl):
        " Locate topic by associated page URL."

        def updateParentStatus(item):
            " Update the visual state of all ancestors."
            parent = item.parent()
            while parent :
                parent.setExpanded(True)
                parent = parent.parent()

        path = unicode(qurl.path() )
        item = self.url2item.get(path, None)
        if item :
            updateParentStatus(item)
            self.tree.setCurrentItem(item)
            self.tree.scrollToItem(item)

    def onTabSwitched(self):
        " Update Topics to fit with current file. "
        self.clear()

        if self.mainwin.currentView:
            chmfile = self.mainwin.currentView.chmfile
            self.loadTopics(chmfile.topics)

    def clear(self):
        " Clear current topics"
        AbstractTreeView.clear(self)
        self.url2item.clear()

    loadTopics = AbstractTreeView.loadData

    def loadNode(self, node, parent):
        " Create one item ."
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
