#!/usr/bin/python
# coding: utf8
#########################################################################
# Author: Xinyu.Xiang(John)
# email: zorrohunter@gmail.com
# Created Time: 2009年05月31日 星期日 04时26分40秒
# File Name: pychmbookmarks.py
# Description:
#########################################################################
import cPickle as Pickle

from PyQt4 import QtCore, QtGui
from PyQt4.QtGui import QListWidgetItem
from PyQt4.QtCore import QString

from Ui_tab_bookmarks import Ui_TabBookmarks
import globalvalue

def getCurrentWebView():
    return globalvalue.currentwebview


class PyChmBookmarkItem(QListWidgetItem):
    def __init__(self, parent, name=None, url=None, pos=None):
        QListWidgetItem.__init__(self, parent)
        self.name = name
        self.url = url
        self.pos = pos

    def save(self, db):
        if isinstance(self.name, QString):
            self.name = unicode(self.name)
        nm = self.name.encode('utf-8')
        v = Pickle.dumps((self.url, self.pos))
        db[nm] = v
        db.sync()

    def delfromdb(self, db):
        if isinstance(self.name, QString):
            self.name = unicode(self.name)
        name = self.name.encode('utf-8')
        try:
            del db[name]
            db.sync()
        except:
            pass

    def seturlandpos(self, dbv):
        self.url, self.pos = Pickle.loads(dbv)

class PyChmBookmarksView(QtGui.QWidget, Ui_TabBookmarks):
    def __init__(self, parent=None, db=None):
        '''
        attrs:
           db: a bsddb , the bookmarks stored in it
        '''
        QtGui.QWidget.__init__(self, parent)
        self.setupUi(self)
        self.db = db
        self.connect(self.list, QtCore.SIGNAL('itemDoubleClicked(QListWidgetItem*)'), self.onItemDoubleClicked)
        self.connect(self.btnAdd, QtCore.SIGNAL('clicked()'), self.onAddPressed)
        self.connect(self.btnDel, QtCore.SIGNAL('clicked()'), self.onDelPressed)
        self.connect(self.btnEdit, QtCore.SIGNAL('clicked()'), self.onEditPressed)
        self.dataloaded = False

    def onAddPressed(self):
        '''
        inner method
        '''

        webview = getCurrentWebView()

        url          = webview.openedpg
        title        = webview.title()
        pos          = webview.getScrollPos()

        default_name = title or u"new bookmark"

        name, ok = QtGui.QInputDialog.getText(  self,
                                                u'add bookmark',
                                                u'input the name of this bookmark',
                                                QtGui.QLineEdit.Normal,
                                                default_name,
                                              )
        if not ok or not name:
            return

        while self.db.has_key(unicode(name).encode('utf-8')):
            name, ok = QtGui.QInputDialog.getText(self, u'add bookmark', u'the name exists,input another!',
                    QtGui.QLineEdit.Normal, name)
            if not ok or len(name) == 0:
                return

        item = PyChmBookmarkItem(self.list, name, url, pos)
        item.setText(name)
        item.save(self.db)

    def onDelPressed(self):
        '''
        inner method
        '''
        item = self.list.currentItem()
        if item is not None:
            item.delfromdb(self.db)
            self.list.takeItem(self.list.row(item))

    def onEditPressed(self):
        '''
        inner method
        '''
        item = self.list.currentItem()
        if item is not None:
            name, ok = QtGui.QInputDialog.getText(self, u'edit bookmark', u'input the name of this bookmark',
                    QtGui.QLineEdit.Normal, item.name)
            if not ok or len(name) == 0:
                return

            item.name = name
            item.setText(name)

    def showEvent(self, event):
        '''
        inner method
        '''
        if self.db is None or self.dataloaded:
            return
        self.dataloaded=True
        self.loaddata()

    def clearandsetdb(self, db):
        '''
        clear the bookmark view and set a new db
        '''
        self.db = db
        self.list.clear()
        self.dataloaded = False

    def loaddata(self):
        '''
        loaddata from db
        '''
        if self.dataloaded:
            return
        self.dataloaded = True
        self.list.clear()
        for k, v in self.db.iteritems():
            item = PyChmBookmarkItem(self.list)
            item.name = k.decode('utf-8')
            item.setText(k)
            item.seturlandpos(v)

    def onItemDoubleClicked(self, item):
        '''
        inner method
        '''
        if not item :
            return

        webview = getCurrentWebView()

        if webview.openedpg != item.url:
            webview.openPage(item.url)

        webview.setScrollPos(item.pos)
