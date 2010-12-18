#!/usr/bin/env python
# vim: set fileencoding=utf-8 :

from PyQt4 import QtCore, QtGui
from PyQt4.QtGui import QTreeWidgetItem

class AbstractTreeView(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.setupUi(self)

        self.connect(self.tree,
                     QtCore.SIGNAL('itemDoubleClicked(QTreeWidgetItem*,int)'),
                     self.onDoubleClicked,
                    )

    def keyPressEvent(self, keyevent):
        # when 'enter' is pressed, simulated double click action
        if keyevent.key() == QtCore.Qt.Key_Return:
            self.onDoubleClicked( self.tree.currentItem(), 0)
        else:
            keyevent.ignore()

    def clear(self):
        self.tree.clear()

    def onDoubleClicked(self, item, _col):
        if item :
            url = item.entry.url
            self.emit(QtCore.SIGNAL('openURL'), url)

    def loadData(self, tree):
        # always clear current state
        self.clear()

        if tree:
            self.loadNode(node=tree, parent=None)
            self.tree.update()

    def loadNode(self, node, parent):
        # special case for the root of tree
        if not parent:
            parent = self.tree

        prev = None
        for child in node.children:
            # insert below `parent`, after `prev`
            item = QTreeWidgetItem(parent, prev)

            item.entry = child
            item.setText(0, child.name or child.keyword )
            #if child.url :
                #self.url2item[child.url] = item

            self.loadNode(child, item)

            prev = item
