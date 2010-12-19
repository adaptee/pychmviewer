#!/usr/bin/python
# vim: set fileencoding=utf-8 :

" Provides the index panel. "

from PyQt4 import QtCore

from treeview import AbstractTreeView
from Ui_panelindex import Ui_PanelIndex

class PyChmIndexView(AbstractTreeView, Ui_PanelIndex ):
    " Implements the index panel. "
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
        " Update the index panel to fit with current file "
        self.clear()

        if self.mainwin.currentView:
            chmfile = self.mainwin.currentView.chmfile
            self.loadIndex(chmfile.index)

    def clear(self):
        " Clear current contents of index panel"
        AbstractTreeView.clear(self)
        self.text.clear()

    loadIndex = AbstractTreeView.loadData

    def onTextChanged(self, text):
        " Search the index at real time"
        items = self.tree.findItems(text, QtCore.Qt.MatchStartsWith)
        if items:
            item = items[0]
            self.tree.setCurrentItem(item)
            self.tree.scrollToItem(item)

    def onReturnPressed(self):
        " What to do when user press Enter in the input field?"
        raise NotImplementedError("")



