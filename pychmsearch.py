#!/usr/bin/python
# coding: utf8
#########################################################################
# Author: Xinyu.Xiang(John)
# email: zorrohunter@gmail.com
# Created Time: 2009年05月30日 星期六 20时10分26秒
# File Name: pychmsearch.py
# Description:
#########################################################################
import re

from PyQt4 import QtCore, QtGui
from PyQt4.QtGui import QTreeWidgetItem

import globalvalue
from Ui_tab_search import Ui_TabSearch
from extract_chm import getfilelist

detenc = re.compile(r'<meta\b[^<]*?charset\s*?=\s*?([\w-]+)[\s\'"]', re.I)


def filterByExt(filenames, exts):
    if not filenames or not exts:
        return filenames

    filenames = [ filename.lower() for filename in filenames  ]
    exts      = [ ext.lower() for ext in exts  ]

    results   = [ ]

    for filename in filenames:
        for ext in exts:
            if filename.lower().endswith(ext.lower()):
                results.append(filename)

    return results

def getExtensions():
    extensions= []

    for a, b in globalvalue.globalcfg.searchext.iteritems():
        if b:
            extensions.append(a)
    return extensions

def getFilenames():

    ok, filenames = getfilelist(globalvalue.chmpath)
    return filenames if ok else [ ]


class PyChmSearchView(QtGui.QWidget, Ui_TabSearch):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.setupUi(self)
        self.searchBox.setFocus()
        self.connect(self.btnGo, QtCore.SIGNAL('clicked()'), self.onReturnPressed)
        self.connect(self.searchBox.lineEdit(), QtCore.SIGNAL('returnPressed()'), self.onReturnPressed)
        self.connect(self.tree, QtCore.SIGNAL('itemDoubleClicked(QTreeWidgetItem*,int)'), self.onDoubleClicked)

    def clear(self):
        self.tree.clear()
        self.searchBox.lineEdit().clear()

    def search(self, rexp):
        filenames = filterByExt( getFilenames(), getExtensions() )
        if not filenames:
            return

        progress = QtGui.QProgressDialog(u'Searching ...', u'Abort',
               0, len(filenames), self)
        progress.forceShow()

        results = []
        for index, filename in enumerate(filenames):
            progress.setValue(index)
            if index % 5 == 0 and progress.wasCanceled() :
                    break

            file_content = globalvalue.chmFile.GetFileAsStrByUrl(filename.decode('utf-8', 'ignore'))
            if not file_content:
                continue

            match = detenc.search(file_content)
            if match:
                encoding = match.group(1)
            elif globalvalue.encoding:
                encoding = globalvalue.encoding
            else:
                encoding = 'utf-8'

            rc = re.compile(unicode(rexp).encode(encoding))
            match = rc.search(file_content)
            if match:
                results.append((filename.decode('utf-8', 'ignore'), match.group(0).decode(encoding, 'ignore')))

        self.showSearchResults(results)
        progress.setValue( len(filenames) )


    #FIXME; temporary name
    def showSearchResults(self, results):
        self.tree.clear()
        for url, name in results:
            item = QTreeWidgetItem(self.tree)
            item.url = url
            item.setText(0, name)
            item.setText(1, url)
        self.tree.update()

    def onReturnPressed(self):
        text = self.searchBox.lineEdit().text()
        text = unicode(text).strip()
        if text == u'':
            return
        if globalvalue.globalcfg.sengine_own:
            self.search(text)
            return
        if not globalvalue.chmFile.IsSearchable():
            return
        self.tree.clear()
        rt = globalvalue.chmFile.Search(text)
        for entry in rt:
            for url in entry.urls:
                item = QTreeWidgetItem(self.tree)
                item.url = url
                item.setText(0, entry.key)
                item.setText(1, url)
        self.tree.update()

    def onDoubleClicked(self, item, col):
        if item is None:
            return
        self.emit(QtCore.SIGNAL('openUrl'), item.url)

if __name__ == "__main__":
    import sys
    from pychmfile import PyChmFile
    globalvalue.chmpath = u'sb.chm'
    globalvalue.chmFile = PyChmFile()
    globalvalue.chmFile.loadFile(globalvalue.chmpath)
    app = QtGui.QApplication(sys.argv)
    sch = PyChmSearchView()
    sch.show()
    sys.exit(app.exec_())


