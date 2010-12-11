#!/usr/bin/python
# coding: utf8
#########################################################################
# Author: Xinyu.Xiang(John)
# email: zorrohunter@gmail.com
# Created Time: 2009年05月30日 星期六 20时10分26秒
# File Name: pychmsearch.py
# Description:
#########################################################################

from PyQt4 import QtCore, QtGui
from PyQt4.QtGui import QTreeWidgetItem

from utils import getchmfile, setchmfile
from Ui_tab_search import Ui_TabSearch


class PyChmSearchView(QtGui.QWidget, Ui_TabSearch):
    def __init__(self, mainwin=None, parent=None):
        QtGui.QWidget.__init__(self, parent)

        self.setupUi(self)
        self.searchBox.setFocus()

        self.connect(self.go, QtCore.SIGNAL('clicked()'), self.search)
        self.connect(self.searchBox.lineEdit(), QtCore.SIGNAL('returnPressed()'), self.search)
        self.connect(self.tree, QtCore.SIGNAL('itemDoubleClicked(QTreeWidgetItem*,int)'), self.onDoubleClicked)

        #experimental
        self.mainwin = mainwin

    def onDoubleClicked(self, item, _col):
        if item :
            self.emit(QtCore.SIGNAL('openUrl'), item.url)

    def clear(self):
        self.tree.clear()
        self.searchBox.lineEdit().clear()

    def search(self):
        text = self.searchBox.lineEdit().text()
        text = unicode(text).strip()

        if text :
            self._search(text)

    def _search(self, pattern):
        chmfile  = getchmfile()
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

        counter = 1
        for result in results:
            progress.setValue(counter)
            counter += 1
            if counter % 16 == 0 and progress.wasCanceled() :
                break

            if result:
                matches.append(result)

        self._showSearchResults(matches)

    def _showSearchResults(self, results):
        self.tree.clear()
        for url, name in results:
            item = QTreeWidgetItem(self.tree)
            item.url = url
            item.setText(0, name)
            item.setText(1, url)
        self.tree.update()


if __name__ == "__main__":

    import sys

    from pychmfile import PyChmFile
    from session import system_encoding

    if len(sys.argv) > 1:

        path = sys.argv[1].decode(system_encoding)
        chmfile = PyChmFile(path)
        setchmfile(chmfile)

        app = QtGui.QApplication(sys.argv)
        sch = PyChmSearchView()
        sch.show()
        sys.exit(app.exec_())


