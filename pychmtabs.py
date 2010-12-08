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

import globalvalue
from Ui_window_browser import Ui_TabbedBrowser
from pychmwebview import PyChmWebView

class PyChmTabs(QtGui.QWidget, Ui_TabbedBrowser):
    def __init__(self, parent=None):
        '''
        attrs:
            windows: list of PyChmWebView
            signal 'newtabadded' with parameter view(PyChmWebView) will be emited
            signal 'checkToolBar' will emit when sth in view changed(use it to check the
                      toolbar's forward and backward
        '''
        QtGui.QWidget.__init__(self, parent)
        self.setupUi(self)

        if self.tabWidget.count() > 0:
            self.tabWidget.removeTab(0)
        self.connect(self.tabWidget,
                QtCore.SIGNAL('currentChanged(int)'), self.onTabChanged)

        self.closeButton = QtGui.QToolButton(self)
        self.closeButton.setCursor(QtCore.Qt.ArrowCursor)
        self.closeButton.setAutoRaise(True)
        icon  =  QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/images/closetab.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.closeButton.setIcon(icon)
        self.closeButton.setToolTip(u'close current page')
        self.closeButton.setEnabled(False)
        self.connect(self.closeButton, QtCore.SIGNAL('clicked()'), self.onCloseCurrentTab)
        self.tabWidget.setCornerWidget(self.closeButton, QtCore.Qt.TopRightCorner)

        self.newButton = QtGui.QToolButton(self)
        self.newButton.setCursor(QtCore.Qt.ArrowCursor)
        self.newButton.setAutoRaise(True)
        icon  =  QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/images/addtab.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.newButton.setIcon(icon)
        self.newButton.setToolTip(u'add page')
        self.connect(self.newButton, QtCore.SIGNAL('clicked()'), self.onOpenNewTab)
        self.tabWidget.setCornerWidget(self.newButton, QtCore.Qt.TopLeftCorner)

        self.frameFind.setVisible(False)

        self.connect(self.editFind, QtCore.SIGNAL('textEdited(const QString&)'),
                self.onTextEdited)
        self.connect(self.editFind, QtCore.SIGNAL('returnPressed()'),
                self.onFindReturnPressed)
        self.connect(self.toolClose, QtCore.SIGNAL('clicked()'), self.frameFind.hide)
        self.connect(self.toolPrevious, QtCore.SIGNAL('clicked()'), self.onFindPrevious)
        self.connect(self.toolNext, QtCore.SIGNAL('clicked()'), self.onFindNext)

        self.windows = []

    def keyPressEvent(self, event):
        if event.matches(QtGui.QKeySequence.Find):
            self.frameFind.show()
            self.editFind.setFocus()
            self.editFind.setSelection(0, len(self.editFind.text()))
        if event.matches(QtGui.QKeySequence.Copy):
            selectedText = self.tabWidget.currentWidget().selectedText()
            if not selectedText.isEmpty():
                QtGui.QApplication.clipboard().setText(selectedText)


    def onFindReturnPressed(self):
        self.find()

    def addNewTab(self, active):
        ''''''
        view = PyChmWebView(self.tabWidget)
        self.editFind.installEventFilter(self)
        self.windows.append(view)
        self.tabWidget.addTab(view, '')

        if active or len(self.windows) == 1:
            self.tabWidget.setCurrentWidget(view)
            globalvalue.currentwebview = view #set the current web view, so other part will know
            # FIXME
            self.parent().currentwebview = view
        self.connect(view, QtCore.SIGNAL('openUrl'), globalvalue.currentwebview.openPage)
        self.connect(view, QtCore.SIGNAL('openatnewtab'), self.onOpenatNewTab)
        if globalvalue.globalcfg.openremote:
            self.connect(view, QtCore.SIGNAL('openRemoteUrl'), globalvalue.currentwebview.openPage)
            self.connect(view, QtCore.SIGNAL('openremoteatnewtab'), self.onOpenatNewTab)
        self.connect(view.page(), QtCore.SIGNAL('loadFinished(bool)'), self.emitCheckToolBar)
        self.emit(QtCore.SIGNAL('newtabadded'), view)
        self.updateCloseButton()
        return view


    def emitCheckToolBar(self):
        self.emit(QtCore.SIGNAL('checkToolBar'))

    def closeTab(self, view):
        pos = -1
        for i, v in enumerate(self.windows):
            if v == view:
                pos = i
        if pos != -1:
            del self.windows[pos]
        else:
            print ('err: unknow webview to close')
            return
        self.tabWidget.removeTab(self.tabWidget.indexOf(view))
        self.updateCloseButton()

    def find(self):
        self.tabWidget.currentWidget().find(self.editFind.text(),
                                            False, self.checkCase.isChecked())
        if not self.frameFind.isVisible():
            self.frameFind.show()

    def updateCloseButton(self):
        enable = len(self.windows) > 1
        self.closeButton.setEnabled(enable)

    def onOpenatNewTab(self, url):
        view = self.addNewTab(True)
        view.openPage(url)
        return view

    def onTabChanged(self, tabnum):
        if tabnum == -1:
            return
        globalvalue.currentwebview = self.tabWidget.widget(tabnum)
        globalvalue.currentwebview.setFocus()
        self.emit(QtCore.SIGNAL('checkToolBar'))

    def closeAll(self):
        for window in self.windows:
            self.closeTab(window)

    def onCloseCurrentTab(self):
        if len(self.windows) == 1:
            return
        self.closeTab(self.tabWidget.currentWidget())
        globalvalue.currentwebview = self.tabWidget.currentWidget()

    def onOpenNewTab(self):
        url = self.tabWidget.currentWidget().openedpg
        self.onOpenatNewTab(url)

    def onTextEdited(self, _):
        self.find()

    def onFindPrevious(self):
        self.tabWidget.currentWidget().find(self.editFind.text(),
                                            True, self.checkCase.isChecked())
    def onFindNext(self):
        self.tabWidget.currentWidget().find(self.editFind.text(),
                                          False  , self.checkCase.isChecked())

    def setTabName(self, view):
        i = self.tabWidget.indexOf(view)
        if i == -1:
            return
        title = view.title()
        if not title :
            title = globalvalue.chmFile.Title
        if not title :
            title = u'no title'
        if len(title) > 15:
            title = title[0:12] + u'...'
        self.tabWidget.setTabText(i, title)

    def savealltab(self, db):
        db.clear()
        for i, v in enumerate(self.windows):
            if not globalvalue.globalcfg.openremote:
                try:
                    v.openedpg.index(u'://')
                    b = True
                except:
                    b = False
                if b:
                    continue
            key = str(i)
            v = Pickle.dumps((v.openedpg, v.getScrollPos()))
            db[key] = v
        db.sync()

    def loadfromdb(self, db):
        try:
            for k, v in db.iteritems():
                url, pos = Pickle.loads(v)
                view = self.onOpenatNewTab(url)
                view.setScrollPos(pos)
            return True
        except:
            self.closeAll()
            return False


if __name__ == '__main__':
    import sys
    app = QtGui.QApplication(sys.argv)
    from pychmfile import PyChmFile
    globalvalue.chmFile = PyChmFile()
    globalvalue.chmpath = u'python261.chm'
    globalvalue.chmFile.loadFile(globalvalue.chmpath)
    Form  = PyChmTabs()
    globalvalue.tabs = Form
    Form.onOpenatNewTab(globalvalue.chmFile.HomeUrl)
    Form.show()
    sys.exit(app.exec_())

