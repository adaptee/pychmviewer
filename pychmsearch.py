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
from utils import getchmfile, getchmpath, getmainwindow, getencoding, getcfg
from extract_chm import getfilelist
from Ui_tab_search import Ui_TabSearch



def getExtensions():
    extensions= []

    for ext, enable in getcfg().searchext.iteritems():
        if enable:
            extensions.append(a)

    return extensions

def getFilenames():

    ok, filenames = getfilelist(getchmpath())
    return filenames if ok else [ ]

def filterByExt(filenames, exts):
    if not filenames or not exts:
        return filenames

    filenames = [ filename.lower() for filename in filenames  ]
    exts      = [ ext.lower() for ext in exts  ]
    results   = [ ]

    for filename in filenames:
        for ext in exts:
            if filename.endswith(ext):
                results.append(filename)

    return results


def guessEncoding(contents):
    meta_charset = re.compile(r'<meta\b[^<]*?charset\s*?=\s*?([\w-]+)[\s\'"]', re.I)

    match = meta_charset.search(contents)
    if match:
        encoding = match.group(1)
    elif getencoding():
        encoding = getencoding()
    else:
        encoding = "utf-8"

    return encoding


class PyChmSearchView(QtGui.QWidget, Ui_TabSearch):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)

        self.setupUi(self)
        self.searchBox.setFocus()
        self.connect(self.go, QtCore.SIGNAL('clicked()'), self.search)
        self.connect(self.searchBox.lineEdit(), QtCore.SIGNAL('returnPressed()'), self.search)
        self.connect(self.tree, QtCore.SIGNAL('itemDoubleClicked(QTreeWidgetItem*,int)'), self.onDoubleClicked)

    def clear(self):
        self.tree.clear()
        self.searchBox.lineEdit().clear()

    def searchBySelf(self, rexp):
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

            chmfile = getchmfile()
            file_content = chmfile.getContentsByURL(filename.decode('utf-8', 'ignore'))
            if not file_content:
                continue

            encoding = guessEncoding(file_content)

            rc = re.compile(unicode(rexp).encode(encoding))
            match = rc.search(file_content)
            if match:
                results.append( ( filename.decode('utf-8', 'ignore'),
                                  match.group(0).decode(encoding, 'ignore'),)
                              )

        progress.setValue( len(filenames) )

        self.showSearchResults(results)


    #FIXME; temporary name
    def showSearchResults(self, results):
        self.tree.clear()
        for url, name in results:
            item = QTreeWidgetItem(self.tree)
            item.url = url
            item.setText(0, name)
            item.setText(1, url)
        self.tree.update()

    def search(self):
        text = self.searchBox.lineEdit().text()
        text = unicode(text).strip()

        if text :
            self.searchBySelf(text)


    def onDoubleClicked(self, item, _col):
        if item :
            self.emit(QtCore.SIGNAL('openUrl'), item.url)

if __name__ == "__main__":

    import sys

    from pychmfile import PyChmFile
    from session import system_encoding

    if len(sys.argv) > 1:

        globalvalue.chmpath = sys.argv[1].decode(system_encoding)
        globalvalue.chmFile = PyChmFile()
        globalvalue.chmFile.loadFile(globalvalue.chmpath)

        app = QtGui.QApplication(sys.argv)
        sch = PyChmSearchView()
        sch.show()
        sys.exit(app.exec_())


