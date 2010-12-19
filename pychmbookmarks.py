#!/usr/bin/python
# vim: set fileencoding=utf-8 :

" Provides the bookmark panel. "

import cPickle as Pickle

from PyQt4 import QtCore, QtGui
from PyQt4.QtGui import QListWidgetItem

from Ui_panelbookmarks import Ui_PanelBookmarks

class PyChmBookmarkItem(QListWidgetItem):
    " Represent one item of bookmark"
    def __init__(self, parent, name=None, url=None, pos=None):
        QListWidgetItem.__init__(self, parent)
        self.name = name
        self.url  = url
        self.pos  = pos

    def saveTo(self, db):
        " Save this item into external db."
        name  = self.name.encode('utf-8')
        value = Pickle.dumps((self.url, self.pos))
        db[name] = value
        db.sync()

    def delFrom(self, db):
        " Delete this item from external db."
        name = self.name.encode('utf-8')
        try:
            del db[name]
            db.sync()
        except StandardError :
            pass

    def setValue(self, db_value):
        " Update the value "
        self.url, self.pos = Pickle.loads(db_value)

class PyChmBookmarksView(QtGui.QWidget, Ui_PanelBookmarks):
    " Implements the bookmark panel. "
    def __init__(self, mainwin=None, parent=None, ):
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
                            title=u"add bookmark",
                            prompt=u"input the name of this bookmark",
                            default=u"new bookmark",
                        ):

        " Prompt user to input name. "
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
        " Prompt user to specify name for bookmark item. "

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
        " update the contents to fit with current file."
        self.clear()

        if self.mainwin.currentView:
            chmfile = self._getCurrentChmFile()
            self.db = chmfile.bookmarkdb
            self.loadBookmarks()

    def loadBookmarks(self):
        " Load bookmarks from external db. "
        self.clear()

        for key, value in self.db.iteritems():
            item = PyChmBookmarkItem(self.list)
            key = key.decode('utf-8')
            item.name = key
            item.setValue(value)
            item.setText(key)

        self.list.update()

    def clear(self):
        " Clear current display. "
        self.list.clear()

    def _getCurrentView(self):
        "Convenient method for getting current view. "
        return self.mainwin.currentView

    def _getCurrentChmFile(self):
        "Convenient method for getting current file. "
        return self._getCurrentView().chmfile

    def onAddBookmark(self):
        "Add new bookmark item. "
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
        " Edit selected bookmark item. "
        item = self.list.currentItem()
        if item :
            name = self._getNameForBookmark( title=u"rename bookmark",
                                             prompt=u'input new name',
                                           )
            if name:
                item.name = name
                item.setText(name)

    def onDelBookmark(self):
        " Delete selectd bookmark item. "
        item = self.list.currentItem()
        if item :
            item.delFrom(self.db)
            self.list.takeItem(self.list.row(item))

    def onOpenBookmark(self, item):
        " Open selected bookmark item. "
        if item :
            webview = self._getCurrentView()

            webview.loadURL(item.url)
            webview.suggestedPos = item.pos
