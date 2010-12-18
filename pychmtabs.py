#!/usr/bin/python
# coding: utf8
#########################################################################
# Author: Xinyu.Xiang(John)
# email: zorrohunter@gmail.com
# Created Time: 2009年06月01日 星期一 04时05分01秒
# File Name: pychmtabs.py
# Description:
#########################################################################

import cPickle as Pickle

from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import QUrl

from pychmfile import PyChmFile
from pychmwebview import PyChmWebView
from Ui_window_browser import Ui_TabbedBrowser

class PyChmTabs(QtGui.QWidget, Ui_TabbedBrowser):
    def __init__(self, mainwin=None, parent=None):
        '''
        webviews: list of PyChmWebView
        '''
        QtGui.QWidget.__init__(self, parent)
        self.setupUi(self)

        self.mainwin     = mainwin
        self.config      = mainwin.config
        self.session     = mainwin.session
        self.webviews    = []
        self.currentView = None

        self._setupButtonClose()
        self._setupButtonNew()
        self.frameFind.setVisible(False)

        self.connect(self.tabWidget,
                     QtCore.SIGNAL('currentChanged(int)'),
                     self.onTabSwitched
                    )

        self.connect(self.editFind,
                     QtCore.SIGNAL('textEdited(const QString&)'),
                     self.onTextEdited)
        self.connect(self.editFind,
                     QtCore.SIGNAL('returnPressed()'),
                     self.onFindReturnPressed)
        self.connect(self.toolClose,
                     QtCore.SIGNAL('clicked()'),
                     self.frameFind.hide)
        self.connect(self.toolPrevious,
                     QtCore.SIGNAL('clicked()'),
                     self.onFindPrevious)
        self.connect(self.toolNext,
                     QtCore.SIGNAL('clicked()'),
                     self.onFindNext)



    def _setupButtonClose(self):

        buttonClose = self._createButton(pixmap=":/images/closetab.png",
                                         tooltip=u"close current page",
                                         )
        buttonClose.setEnabled(False)
        self.tabWidget.setCornerWidget(buttonClose, QtCore.Qt.TopRightCorner)
        self.connect(buttonClose,
                     QtCore.SIGNAL('clicked()'),
                     self.onCloseCurrentTab)

        self.buttonClose = buttonClose

    def _setupButtonNew(self):
        buttonNew = self._createButton(pixmap=":/images/addtab.png",
                                       tooltip=u"open new page",
                                      )
        self.tabWidget.setCornerWidget(buttonNew, QtCore.Qt.TopLeftCorner)
        self.connect(buttonNew,
                     QtCore.SIGNAL('clicked()'),
                     self.onOpenNewTab)

        self.buttonNew = buttonNew

    def _createButton(self, pixmap, tooltip=u""):

        def createIcon(pixmap_path):
            icon = QtGui.QIcon()
            icon.addPixmap(QtGui.QPixmap(pixmap_path), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            return icon

        button = QtGui.QToolButton(self)

        button.setCursor(QtCore.Qt.ArrowCursor)
        button.setAutoRaise(True)
        button.setIcon(createIcon(pixmap))
        button.setToolTip(tooltip)

        return button

    def keyPressEvent(self, keyevent):
        if keyevent.key() == QtCore.Qt.Key_Escape:
            # Vim user will love this behaviour !
            # cancel find, return focus back
            self.frameFind.hide()
            self.currentView.setFocus()
        else:
            self.tabWidget.keyPressEvent(keyevent)


    def openChmFile(self, path):
        try:
            chmfile = PyChmFile(self.session, path)

            view = PyChmWebView(tabmanager=self,
                                chmfile=chmfile,
                                parent=self.tabWidget
                            )

            self.addNewTab(view)

            # FIXME; dirty hack, but we sitll need it now.
            view.goHome()

            self.emit(QtCore.SIGNAL('fileOpened'), path)

            return view

        except StandardError :
            self.emit(QtCore.SIGNAL('fileNotOpened'), path)
            return None


    def onOpenNewTab(self):
        "duplicate a new view showing same url as this one"
        url = self.tabWidget.currentWidget().loadedURL
        self.onOpenURLatNewTab(url)

    def onOpenURLatNewTab(self, url):
        "open specified url in a newly created view"
        if not self.currentView:
            raise ValueError("[Terrible]! Shame of the coder!")

        view = self.currentView.clone()
        self.addNewTab(view)
        view.loadURL(url)

        return view

    def addNewTab(self, view, active=True):
        "only responsible for putting view into widgetmanager"

        self.webviews.append(view)
        self.tabWidget.addTab(view, '')

        if active or len(self.webviews) == 1:
            self.tabWidget.setCurrentWidget(view)
            self.currentView = view

        self.editFind.installEventFilter(self)

        self.connect(view,
                     QtCore.SIGNAL('openURL'),
                     view.loadURL)
        self.connect(view,
                     QtCore.SIGNAL('openURLatNewTab'),
                     self.onOpenURLatNewTab)
        self.connect(view.page(),
                     QtCore.SIGNAL('loadFinished(bool)'),
                     self.onLoadFinished)

        self.emit(QtCore.SIGNAL('newTabAdded'), view)
        self.updateButtonClose()

        return view

    def closeAll(self):
        for webview in self.webviews:
            self.closeTab(webview)

    def closeTab(self, view):
        pos = -1
        for index, webview in enumerate(self.webviews):
            if webview == view:
                pos = index
        if pos != -1:
            del self.webviews[pos]
        else:
            raise ValueError("[Terrible] asked to close non-managed view! ")

        self.tabWidget.removeTab(self.tabWidget.indexOf(view))
        self.updateButtonClose()


    def updateButtonClose(self):
        enable = len(self.webviews) > 0
        self.buttonClose.setEnabled(enable)

    def onCloseCurrentTab(self):
        self.closeTab(self.tabWidget.currentWidget())
        self.currentView = self.tabWidget.currentWidget()

    def onTabSwitched(self, tabnum):
        self.currentView = self.tabWidget.widget(tabnum)
        # Maybe no views exists now
        if self.currentView:
            self.currentView.setFocus()

        self.emit(QtCore.SIGNAL('tabSwitched'))

    def onLoadFinished(self):
        self.emit(QtCore.SIGNAL('checkToolBar'))

    def setTabName(self, view, title):
        def shortenTitle(title):
            return title[0:12] + u"..." if len(title) > 15 else title

        index = self.tabWidget.indexOf(view)
        if index != -1 :
            title = shortenTitle(title)
            self.tabWidget.setTabText(index, title)

    def onFind(self):
        self.frameFind.show()
        self.editFind.setFocus()
        self.editFind.setSelection(0, len(self.editFind.text()))

    def onFindReturnPressed(self):
        self.find()

    def onTextEdited(self, _text):
        self.find()

    def find(self):
        self.tabWidget.currentWidget().find(self.editFind.text(),
                                            False, self.checkCase.isChecked())
        if not self.frameFind.isVisible():
            self.frameFind.show()

    def onFindPrevious(self):
        self.tabWidget.currentWidget().find(self.editFind.text(),
                                            True, self.checkCase.isChecked())
    def onFindNext(self):
        self.tabWidget.currentWidget().find(self.editFind.text(),
                                          False  , self.checkCase.isChecked())


    def saveTo(self, db):
        "save snapshot of opened views "
        # we only remember now, not past...
        db.clear()

        def isRemoteURL(url):
            return url.scheme() in ["http", "https"]

        for index, view in enumerate(self.webviews):
            if isRemoteURL(view.loadedURL) and not self.config.openRemoteURL:
                continue

            key   = str(index + 1)  # avoid 0
            value = Pickle.dumps((view.chmfile.path,
                                  unicode(view.loadedURL.toString()),
                                  view.currentPos(),
                                  )
                                )
            db[key] = value

        db.sync()

    def loadFrom(self, db):
        "restore previously open views from snapshot"

        for value in db.values():
            path, url, pos = Pickle.loads(value)
            view = self.openChmFile(path)
            if view :
                view.suggestedPos = pos
                view.loadURL(QUrl(url) )


if __name__ == '__main__':
    raise NotImplementedError()
