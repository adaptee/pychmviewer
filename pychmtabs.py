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
from PyQt4.QtWebKit import QWebPage

from pychmwebview import PyChmWebView
from Ui_window_browser import Ui_TabbedBrowser

class PyChmTabs(QtGui.QWidget, Ui_TabbedBrowser):
    def __init__(self, mainwin=None, parent=None):
        '''
        attrs:
            webviews: list of PyChmWebView
            #signal 'newTabAdded' with parameter view(PyChmWebView) will be emited
            signal 'checkToolBar' will emit when sth in view changed(use it to check the
                      toolbar's forward and backward
        '''
        QtGui.QWidget.__init__(self, parent)
        self.setupUi(self)

        self.mainwin     = mainwin
        self.config      = mainwin.config
        self.session     = mainwin.session
        self.webviews    = []
        self.currentView = None

        print "[tabmanager] %d tabs exists right after __init__()" % self.tabWidget.count()
        ## FIXME; without this strange line
        ## we will have a extra and weird 'Untitled' tab
        if self.tabWidget.count() > 0:
            self.tabWidget.removeTab(0)

        self._setupCloseButton()
        self._setupNewButton()
        self.frameFind.setVisible(False)

        self.connect(self.tabWidget,
                     QtCore.SIGNAL('currentChanged(int)'),
                     self.onTabSwitched
                    )

        self.connect(self.editFind, QtCore.SIGNAL('textEdited(const QString&)'),
                self.onTextEdited)
        self.connect(self.editFind, QtCore.SIGNAL('returnPressed()'),
                self.onFindReturnPressed)
        self.connect(self.toolClose, QtCore.SIGNAL('clicked()'), self.frameFind.hide)
        self.connect(self.toolPrevious, QtCore.SIGNAL('clicked()'), self.onFindPrevious)
        self.connect(self.toolNext, QtCore.SIGNAL('clicked()'), self.onFindNext)



    def _setupCloseButton(self):

        self.closeButton = self._createButton(pixmap=":/images/closetab.png",
                                              tooltip=u"close current page",
                                             )
        self.closeButton.setEnabled(False)
        self.connect(self.closeButton, QtCore.SIGNAL('clicked()'), self.onCloseCurrentTab)
        self.tabWidget.setCornerWidget(self.closeButton, QtCore.Qt.TopRightCorner)

    def _setupNewButton(self):
        self.newButton = self._createButton(pixmap=":/images/addtab.png",
                                            tooltip=u"open new page",
                                           )
        self.connect(self.newButton, QtCore.SIGNAL('clicked()'), self.onOpenNewTab)
        self.tabWidget.setCornerWidget(self.newButton, QtCore.Qt.TopLeftCorner)

    def _createButton(self, pixmap, tooltip=u""):

        def createIcon(pixmap_path):
            icon = QtGui.QIcon()
            icon.addPixmap(QtGui.QPixmap(pixmap_path), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            return icon

        icon   = createIcon(pixmap)
        button = QtGui.QToolButton(self)

        button.setCursor(QtCore.Qt.ArrowCursor)
        button.setAutoRaise(True)
        button.setIcon(icon)
        button.setToolTip(tooltip)
        return button

    def keyPressEvent(self, event):
        if event.matches(QtGui.QKeySequence.Find):
            self.frameFind.show()
            self.editFind.setFocus()
            self.editFind.setSelection(0, len(self.editFind.text()))
        # FIXME; should this be moved into webview class?
        elif event.matches(QtGui.QKeySequence.Copy):
            self.currentView.triggerPageAction(QWebPage.Copy)
        elif event.matches(QtGui.QKeySequence.SelectAll):
            #FIXME; it does not work
            print "[keyPressEvent] Ctrl-A"
            self.currentView.triggerPageAction(QWebPage.MoveToStartOfDocument)
            self.currentView.triggerPageAction(QWebPage.SelectEndOfDocument)

    def openChmFile(self, chmfile):
        view = self.onOpenAtNewTab(chmfile.home)
        view.chmfile = chmfile
        # FIXME; dirty hack
        view.goHome()

    def onOpenNewTab(self):
        url = self.tabWidget.currentWidget().openedpg
        self.onOpenAtNewTab(url)

    def onOpenAtNewTab(self, url):
        # FIXME; should add a new param representing True/False
        # 'True' means forcc opening new tab at foregound.
        view = self.addNewTab(True)
        view.openPage(url)
        return view

    def addNewTab(self, active):
        ''''''

        if self.currentView:
            view = self.currentView.clone()
        else:
            view = PyChmWebView(tabmanager=self, parent=self.tabWidget)

        self.webviews.append(view)
        self.tabWidget.addTab(view, '')

        if active or len(self.webviews) == 1:
            self.tabWidget.setCurrentWidget(view)
            self.currentView = view

        self.editFind.installEventFilter(self)

        self.connect(view, QtCore.SIGNAL('openURL'), view.openPage)
        self.connect(view, QtCore.SIGNAL('openAtNewTab'), self.onOpenAtNewTab)
        self.connect(view.page(), QtCore.SIGNAL('loadFinished(bool)'), self.onLoadFinished)

        if self.config.openremote:
            self.connect(view, QtCore.SIGNAL('openRemoteURL'), view.openPage)
            self.connect(view, QtCore.SIGNAL('openremoteatnewtab'), self.onOpenAtNewTab)

        self.emit(QtCore.SIGNAL('newTabAdded'), view)
        self.updateCloseButton()

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
            print ('[Error] unknow webview to close')
            return

        self.tabWidget.removeTab(self.tabWidget.indexOf(view))
        self.updateCloseButton()


    def updateCloseButton(self):
        #enable = len(self.webviews) > 1
        enable = len(self.webviews) > 0
        self.closeButton.setEnabled(enable)

    def onCloseCurrentTab(self):
        # FIXME; prevent closing the only tab
        #if len(self.webviews) == 1:
            #return

        self.closeTab(self.tabWidget.currentWidget())
        self.currentView = self.tabWidget.currentWidget()
        #print "[currentView] %s" % self.currentView


    def onTabSwitched(self, tabnum):
        print "[TabSwitched] tabnum: %d" % tabnum
        self.currentView = self.tabWidget.widget(tabnum)
        # Maybe all views are closed
        if self.currentView:
            self.currentView.setFocus()

        self.emit(QtCore.SIGNAL('tabSwitched'))

    def onLoadFinished(self):
        self.emit(QtCore.SIGNAL('checkToolBar'))

    def setTabName(self, view):
        index = self.tabWidget.indexOf(view)
        if index == -1:
            return

        title = view.title() or view.chmfile.title or u"no title"
        if len(title) > 15:
            title = title[0:12] + u'...'
        self.tabWidget.setTabText(index, title)



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
        db.clear()

        for index, view in enumerate(self.webviews):
            if not self.config.openremote:
                try:
                    viewv.openedpg.index(u'://')
                    b = True
                except:
                    b = False
                if b:
                    continue
            key = str(index)
            value = Pickle.dumps((view.openedpg, view.getScrollPos()))
            db[key] = value

        db.sync()

    def loadFrom(self, db):
        try:
            for key, value in db.iteritems():
                url, pos = Pickle.loads(value)
                view = self.onOpenAtNewTab(url)
                view.setScrollPos(pos)
            return True
        except:
            self.closeAll()
            return False


if __name__ == '__main__':
    raise NotImplementedError()
