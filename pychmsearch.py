#!/usr/bin/python
# vim: set fileencoding=utf-8 :

" Provides the search panel. "

from PyQt4 import QtCore, QtGui
from PyQt4.QtGui import QTreeWidgetItem

from Ui_panelsearch import Ui_PanelSearch

class PyChmSearchView(QtGui.QWidget, Ui_PanelSearch):
    " Implements the search panel. "
    def __init__(self, mainwin, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.setupUi(self)
        self.searchBox.setFocus()
        self.connect(self.buttonGo,
                     QtCore.SIGNAL('clicked()'),
                     self.search)
        self.connect(self.searchBox.lineEdit(),
                     QtCore.SIGNAL('returnPressed()'),
                     self.search)
        self.connect(self.tree,
                     QtCore.SIGNAL('itemDoubleClicked(QTreeWidgetItem*,int)'),
                     self.onDoubleClicked)

        self.mainwin = mainwin

    def onDoubleClicked(self, item, _col):
        "Open the page connected with the clicked item. "
        if item :
            self.emit(QtCore.SIGNAL('openURL'), item.url)

    def onTabSwitched(self):
        " Update contents to fit with current file. "
        #FIXME; currently, I have no better idea
        self.clear()

    def clear(self):
        " Clear current contents. "
        self.tree.clear()
        self.searchBox.lineEdit().clear()

    def search(self):
        " Search all pages within current file by specified keyword. "
        text = self.searchBox.lineEdit().text()
        text = unicode(text).strip()

        if text :
            self._search(text)

    def _search(self, pattern):
        " Implement the search feature. "
        chmfile  = self.mainwin.currentView.chmfile
        maxmimum = len( chmfile.getSearchableURLs() )

        progress = QtGui.QProgressDialog(u'Searching ...',
                                         u'Abort',
                                         0,
                                         maxmimum,
                                         self,
                                         )
        progress.forceShow()

        results = chmfile.search(pattern)
        matches = []

        for index, result in enumerate(results):
            if result:
                matches.append(result)
            progress.setValue(index + 1)
            if (index + 1) % 16 == 0 and progress.wasCanceled() :
                break

        self._showSearchResults(matches)

    def _showSearchResults(self, results):
        " update the tree view with the result of search. "
        self.tree.clear()
        for url, name in results:
            item = QTreeWidgetItem(self.tree)
            item.url = url
            item.setText(0, name)
            item.setText(1, url)
        self.tree.update()

