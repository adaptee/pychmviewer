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

from Ui_tab_bookmarks import Ui_TabBookmarks
import globalvalue

def getCurrentWebView():
    return globalvalue.currentwebview

class PyChmBookmarkItem(QListWidgetItem):
    def __init__(self, parent, name=None, url=None, pos=None):
        QListWidgetItem.__init__(self, parent)
        self.name = name
        self.url  = url
        self.pos  = pos

    def saveTo(self, db):
        name  = self.name.encode('utf-8')
        value = Pickle.dumps((self.url, self.pos))
        db[name] = value
        db.sync()

    def delFrom(self, db):
        name = self.name.encode('utf-8')
        try:
            del db[name]
            db.sync()
        except StandardError :
            pass

    def setUrlandPos(self, db_value):
        self.url, self.pos = Pickle.loads(db_value)

class PyChmBookmarksView(QtGui.QWidget, Ui_TabBookmarks):
    def __init__(self, parent=None, db=None):
        '''
        attrs:
           db: a bsddb , the bookmarks stored in it
        '''
        QtGui.QWidget.__init__(self, parent)
        self.setupUi(self)

        self.db = db
        self.dataloaded = False

        self.connect(self.list, QtCore.SIGNAL('itemDoubleClicked(QListWidgetItem*)'), self.onItemDoubleClicked)
        self.connect(self.btnAdd, QtCore.SIGNAL('clicked()'), self.onAddPressed)
        self.connect(self.btnDel, QtCore.SIGNAL('clicked()'), self.onDelPressed)
        self.connect(self.btnEdit, QtCore.SIGNAL('clicked()'), self.onEditPressed)

    def _getNameFromUser(   self,
                            title=u"add bookmar",
                            prompt=u"input the name of this bookmark",
                            default=u"new bookmark",
                        ):

        #TODO: make sure the dialog is always wide enough ,
        # to show the title completely.
        name, ok = QtGui.QInputDialog.getText( self,
                                               title,
                                               prompt,
                                               QtGui.QLineEdit.Normal,
                                               default,
                                             )
        if not ok or not name:
            return u""
        else:
            # transform QString into unicode.
            return unicode(name)


    def _getNameForBookmark(self,
                            title=u"add bookmar",
                            prompt=u"input the name of this bookmark",
                            default=u"new bookmark",
                           ):

        name = self._getNameFromUser( title=title,
                                      prompt=prompt,
                                      default=default,
                                    )
        if name :
            # name confliction is not allowed
            while self.db.has_key(name.encode('utf-8')):

                title = u"name confliction"
                prompt = u"Bookmark named as '%s' already exists, choose another name." % name
                name = self._getNameFromUser( title=title,
                                            prompt=prompt,
                                            default=name,
                                            )
                if not name:
                    break

        return name

    def onAddPressed(self):
        '''
        inner method
        '''

        webview = getCurrentWebView()

        url   = webview.openedpg
        title = webview.title()
        pos   = webview.getScrollPos()

        default_name = title or u"new bookmark"

        name = self._getNameForBookmark(default=default_name)

        if name:
            item = PyChmBookmarkItem(self.list, name, url, pos)
            item.setText(name)
            item.saveTo(self.db)

    def onDelPressed(self):
        '''
        inner method
        '''
        item = self.list.currentItem()
        if item :
            item.delFrom(self.db)
            self.list.takeItem(self.list.row(item))

    def onEditPressed(self):
        '''
        inner method
        '''
        item = self.list.currentItem()
        if item :
            name = self._getNameForBookmark( title=u"rename bookmark",
                                             prompt=u'input new name',
                                           )
            if name:
                item.name = name
                item.setText(name)

    def showEvent(self, event):
        '''
        inner method
        '''
        if not self.db or self.dataloaded:
            return

        self.loadBookmarks()

    def clearandsetdb(self, db):
        '''
        clear the bookmark view and set a new db
        '''
        self.db = db
        self.list.clear()
        self.dataloaded = False

    def loadBookmarks(self):
        '''
        load Bookmarks from db
        '''
        if self.dataloaded:
            return

        self.list.clear()

        for key, value in self.db.iteritems():
            item = PyChmBookmarkItem(self.list)
            key = key.decode('utf-8')
            item.name = key
            item.setUrlandPos(value)
            item.setText(key)

        self.dataloaded = True

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
