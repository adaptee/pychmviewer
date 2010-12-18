#!/usr/bin/python
# vim: set fileencoding=utf-8 :

from PyQt4 import QtCore, QtGui

from treeview import AbstractTreeView
from Ui_panelindex import Ui_PanelIndex

class PyChmIndexView(AbstractTreeView, Ui_PanelIndex ):
    def __init__(self, mainwin=None, parent=None):
        AbstractTreeView.__init__(self, parent)

        self.connect(self.text,
                     QtCore.SIGNAL('textChanged(const QString&)'),
                     self.onTextChanged)
        self.connect(self.text,
                     QtCore.SIGNAL('returnPressed()'),
                     self.onReturnPressed)

        self.mainwin  = mainwin

        if mainwin.currentView:
            chmfile = mainwin.currentView.chmfile
            if chmfile and chmfile.index :
                self.loadIndex(chmfile.index)


        self.lastitem = None

    def onTabSwitched(self):
        self.clear()

        if self.mainwin.currentView:
            chmfile = self.mainwin.currentView.chmfile
            self.loadIndex(chmfile.index)

    def clear(self):
        '''
        clear the data in the index view
        '''
        AbstractTreeView.clear(self)
        self.text.clear()

    loadIndex = AbstractTreeView.loadData

    def onTextChanged(self, text):
        "search index tree at real time"
        items = self.tree.findItems(text, QtCore.Qt.MatchStartsWith)
        if items:
            item = items[0]
            self.tree.setCurrentItem(item)
            self.tree.scrollToItem(item)

    def onReturnPressed(self):
        raise NotImplementedError("")


if __name__  ==  "__main__":
    raise NotImplementedError()


