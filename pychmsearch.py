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

    def mySearch(self, rexp):
        ok, filelist = getfilelist(globalvalue.chmpath)
        if not ok:
            return

        extlist = []
        for a, b in globalvalue.globalcfg.searchext.iteritems():
            if b:
                extlist.append(a)

        sflist = self.__filt(filelist, extlist)
        prgrs = QtGui.QProgressDialog(u'Searching ...', u'Abort',
               0, len(sflist), self)
        prgrs.forceShow()
        rt = []
        for i, f in enumerate(sflist):
            prgrs.setValue(i)
            if i % 5 == 0:
                if prgrs.wasCanceled():
                    break
            fctt = globalvalue.chmFile.GetFileAsStrByUrl(f.decode('utf-8', 'ignore'))
            if not fctt:
                continue
            rrt = detenc.search(fctt)
            if rrt:
                enc = rrt.group(1)
            elif globalvalue.encoding:
                enc = globalvalue.encoding
            else:
                enc = 'utf-8'
            rc = re.compile(unicode(rexp).encode(enc))
            ttt = rc.search(fctt)
            if ttt:
                rt.append((f.decode('utf-8', 'ignore'), ttt.group(0).decode(enc, 'ignore')))
        self.tree.clear()
        for url, name in rt:
            item = QTreeWidgetItem(self.tree)
            item.url = url
            item.setText(0, name)
            item.setText(1, url)
        self.tree.update()
        prgrs.setValue(len(sflist))



    def __filt(self, filelist, extlist):
        rt = []
        for fp in filelist:
            ok = False
            for ext in extlist:
                if fp.lower().endswith(ext.lower()):
                    ok = True
            rt.append(fp)
        return rt

    def onReturnPressed(self):
        text = self.searchBox.lineEdit().text()
        text = unicode(text).strip()
        if text == u'':
            return
        if globalvalue.globalcfg.sengine_own:
            self.mySearch(text)
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


