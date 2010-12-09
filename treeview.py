#!/usr/bin/env python
# vim: set fileencoding=utf-8 :

from PyQt4 import QtCore, QtGui
from PyQt4.QtGui import QTreeWidgetItem

class AbstractTreeView(object):

    def __init__(self):
        self.setupUi(self)
        self.tree.headerItem().setHidden(True)

        self.connect(self.tree,
                     QtCore.SIGNAL('itemDoubleClicked(QTreeWidgetItem*,int)'),
                     self.onDoubleClicked,
                    )

        self.dataloaded = False

    def clear(self):
        self.tree.clear()
        self.dataloaded = False

    def onDoubleClicked(self, item, _col):
        if item :
            url = item.entry.url
            self.emit(QtCore.SIGNAL('openUrl'), url)

    def loadData(self, tree):
        if self.dataloaded:
            return

        if tree:
            self.clear()

            self.loadNode(node=tree, parent=None)
            self.tree.update()

            self.dataloaded = True

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
            #if child.url :
                #self.url2item[child.url] = item

            self.loadNode(child, item)

            prev = item


