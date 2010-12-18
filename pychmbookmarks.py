#!/usr/bin/python
# vim: set fileencoding=utf-8 :

import cPickle as Pickle

from PyQt4 import QtCore, QtGui
from PyQt4.QtGui import QListWidgetItem

from Ui_panelbookmarks import Ui_PanelBookmarks

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

    def setValue(self, db_value):
        self.url, self.pos = Pickle.loads(db_value)

class PyChmBookmarksView(QtGui.QWidget, Ui_PanelBookmarks):

    def __init__(self, mainwin=None, parent=None, ):
        '''
        attrs:
           db: a small database storing bookmarks
        '''
        QtGui.QWidget.__init__(self, parent)
        self.setupUi(self)

        self.mainwin = mainwin
        # { } used as dummy database, to prevent NoneType Error
        self.db      = { }

        self.connect(self.buttonAddBookmark,
                     QtCore.SIGNAL('clicked()'),
                     self.onAddBookmark)
        self.connect(self.buttonEditBookmark,
                     QtCore.SIGNAL('clicked()'),
                     self.onEditBookmark)
        self.connect(self.buttonDelBookmark,
                     QtCore.SIGNAL('clicked()'),
                     self.onDelBookmark)

        self.connect(self.list,
                     QtCore.SIGNAL('itemDoubleClicked(QListWidgetItem*)'),
                     self.onOpenBookmark
                    )

    def _getNameFromUser(   self,
                            title=u"add bookmar",
                            prompt=u"input the name of this bookmark",
                            default=u"new bookmark",
                        ):

        #FIXME ; the dialog maybe not wide enough to show title completely.
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

                title  = u"Name confliction"
                prompt = u"Bookmark '%s' already exists, choose another name."\
                         % name
                name = self._getNameFromUser( title=title,
                                            prompt=prompt,
                                            default=name,
                                            )
                if not name:
                    break

        return name

    def onTabSwitched(self):
        self.clear()

        if self.mainwin.currentView:
            chmfile = self._getCurrentChmFile()
            self.db = chmfile.bookmarkdb
            self.loadBookmarks()

    def loadBookmarks(self):
        '''
        load Bookmarks from db
        '''
        self.clear()

        for key, value in self.db.iteritems():
            item = PyChmBookmarkItem(self.list)
            key = key.decode('utf-8')
            item.name = key
            item.setValue(value)
            item.setText(key)

        self.list.update()

    def clear(self):
        '''
        clear the bookmark view
        '''
        self.list.clear()


    def _getCurrentView(self):
        return self.mainwin.currentView

    def _getCurrentChmFile(self):
        return self._getCurrentView().chmfile

    def onAddBookmark(self):
        webview = self._getCurrentView()

        url   = unicode( webview.loadedURL.path() )
        title = webview.title()
        pos   = webview.currentPos()

        default_name = title or u"new bookmark"

        name = self._getNameForBookmark(default=default_name)

        if name:
            item = PyChmBookmarkItem(self.list, name, url, pos)
            item.setText(name)
            item.saveTo(self.db)

    def onEditBookmark(self):
        item = self.list.currentItem()
        if item :
            name = self._getNameForBookmark( title=u"rename bookmark",
                                             prompt=u'input new name',
                                           )
            if name:
                item.name = name
                item.setText(name)

    def onDelBookmark(self):
        item = self.list.currentItem()
        if item :
            item.delFrom(self.db)
            self.list.takeItem(self.list.row(item))

    def onOpenBookmark(self, item):
        if item :
            webview = self._getCurrentView()

            webview.loadURL(item.url)
            webview.suggestedPos = item.pos
