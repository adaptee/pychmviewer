#!/usr/bin/python
# coding: utf8
#########################################################################
# Author: Xinyu.Xiang(John)
# email: zorrohunter@gmail.com
# Created Time: 2009年06月01日 星期一 11时03分34秒
# File Name: pychmmainwindow.py
# Description:
#########################################################################

import os
import sys

from PyQt4 import QtCore, QtGui
from PyQt4.QtGui import QAction, QMenu
from PyQt4 import QtWebKit

from pychmindex import PyChmIndexView
from pychmtopics import PyChmTopicsView
from pychmsearch import PyChmSearchView
from pychmbookmarks import PyChmBookmarksView
from pychmtabs import PyChmTabs

from encodinglist import encodings
from settingdlg import SettingDlg
from htmldlg import HtmlDialog
from about import AboutDialog
from Ui_window_main import Ui_MainWindow

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s


class PyChmMainWindow(QtGui.QMainWindow, Ui_MainWindow):
    def __init__(self, session, paths=None, parent=None):
        QtGui.QMainWindow.__init__(self, parent)
        self.setupUi(self)

        self.session = session
        self.config  = session.config

        # make using QSettings more easy
        QtCore.QCoreApplication.setOrganizationName(session.organization)
        QtCore.QCoreApplication.setApplicationName(session.application)
        # You do not want to resize the mainwindow every time
        self.restoreLayoutInfo()

        # FIXME; 3 lines should be put into Ui_xxxx.py, not here
        self.WebViewsWidget = PyChmTabs(mainwin=self, parent=self.widget)
        self.WebViewsWidget.setObjectName(_fromUtf8("WebViewsWidget"))
        self.horizontalLayout.addWidget(self.WebViewsWidget)

        self.tabmanager = self.WebViewsWidget

        self._setupFileMenu()
        self._setupViewMenu()
        self._setupPanelMenu()
        self._setupPanelDock()
        self._setupNavigation()
        self._setupSettingsMenu()
        self._setupHelpMenu()
        self._setupMiscActions()
        self._setWebFont()

        # FIXME; dirty
        # FIXME; flash still does not work
        #settings   = QtWebKit.QWebSettings.globalSettings()
        #settings.setAttribute(QtWebKit.QWebSettings.PluginsEnabled, True)

        if paths:
            self._startUpWithPaths(paths)
        else:
            self._startUpWithNoPaths()

    def _startUpWithPaths(self, paths):
        for path in paths:
            try:
                self.openFile(path)
            except IOError:
                pass

    def _startUpWithNoPaths(self):
        if self.config.sessionRestore:
            self.tabmanager.loadFrom(self.session.snapshot)

    @property
    def currentView(self):
        return self.tabmanager.currentView



    def _setWebFont(self):
        settings   = QtWebKit.QWebSettings.globalSettings()

        fontfamily = self.config.fontfamily
        fontsize   = self.config.fontsize

        if fontfamily :
            settings.setFontFamily(QtWebKit.QWebSettings.StandardFont, fontfamily)
            settings.setFontFamily(QtWebKit.QWebSettings.FixedFont, fontfamily)
            settings.setFontFamily(QtWebKit.QWebSettings.SerifFont, fontfamily)
            settings.setFontFamily(QtWebKit.QWebSettings.SansSerifFont, fontfamily)
            settings.setFontFamily(QtWebKit.QWebSettings.CursiveFont, fontfamily)
            settings.setFontFamily(QtWebKit.QWebSettings.FantasyFont, fontfamily)
        if fontsize :
            settings.setFontSize(QtWebKit.QWebSettings.DefaultFontSize, fontsize)
            settings.setFontSize(QtWebKit.QWebSettings.MinimumFontSize, fontsize)
            settings.setFontSize(QtWebKit.QWebSettings.MinimumLogicalFontSize, fontsize)
            settings.setFontSize(QtWebKit.QWebSettings.DefaultFixedFontSize, fontsize)

    def _setupPanelMenu(self):

        self.actionIndex = self.dockIndex.toggleViewAction()
        self.actionIndex.setCheckable(True)
        self.actionIndex.setChecked(True)
        self.menu_Panels.addAction(self.actionIndex)

        self.actionTopics = self.dockTopics.toggleViewAction()
        self.actionTopics.setCheckable(True)
        self.actionTopics.setChecked(True)
        self.menu_Panels.addAction(self.actionTopics)

        self.actionSearch = self.dockSearch.toggleViewAction()
        self.actionSearch.setCheckable(True)
        self.actionSearch.setChecked(True)
        self.menu_Panels.addAction(self.actionSearch)

        self.actionBookmark = self.dockBookmark.toggleViewAction()
        self.actionBookmark.setCheckable(True)
        self.actionBookmark.setChecked(True)
        self.menu_Panels.addAction(self.actionBookmark)

    def _setupPanelDock(self):

        # the order determines who is listed before another
        # In this case  Index->Topics->Search->Bookmark
        self.tabifyDockWidget(self.dockIndex, self.dockTopics)
        self.tabifyDockWidget(self.dockIndex, self.dockSearch)
        self.tabifyDockWidget(self.dockIndex, self.dockBookmark)

        self.indexview = PyChmIndexView(mainwin=self, parent=self.dockIndex)
        self.dockIndex.setWidget(self.indexview)

        self.topicsview = PyChmTopicsView(mainwin=self, parent=self.dockTopics)
        self.dockTopics.setWidget(self.topicsview)

        self.searchview = PyChmSearchView(mainwin=self, parent=self.dockSearch)
        self.dockSearch.setWidget(self.searchview)

        self.bookmarkview = PyChmBookmarksView(mainwin=self, parent=self.dockBookmark)
        self.dockBookmark.setWidget(self.bookmarkview)

        self.connect(self.indexview, QtCore.SIGNAL('openURL'), self.openInCurrentTab)
        self.connect(self.topicsview, QtCore.SIGNAL('openURL'), self.openInCurrentTab)
        self.connect(self.searchview, QtCore.SIGNAL('openURL'), self.openInCurrentTab)

        # Topics is the most useful one, so activiate it by force
        self.dockTopics.activateWindow()
        self.dockTopics.raise_()


    def _setupFileMenu(self):
        self.connect(self.file_Open_action, QtCore.SIGNAL('triggered(bool)'), self.onFileOpen)
        self.connect(self.file_Print_action, QtCore.SIGNAL('triggered(bool)'), self.onFilePrint)
        self.connect(self.file_Extract_action,
                QtCore.SIGNAL('triggered(bool)'), self.onExtractCurrentCHMFile)

    def _setupViewMenu(self):
        self.connect(self.view_Increase_font_size_action,
                QtCore.SIGNAL('triggered(bool)'), self.onZoonIn)
        self.connect(self.view_Decrease_font_size_action,
                QtCore.SIGNAL('triggered(bool)'), self.onZoomOut)
        self.connect(self.view_norm_font_size_action,
                QtCore.SIGNAL('triggered(bool)'), self.onZoomOff)
        self.connect(self.view_View_HTML_source_action,
                QtCore.SIGNAL('triggered(bool)'), self.onViewSource)
        self.connect(self.view_Locate_in_contents_action,
                QtCore.SIGNAL('triggered(bool)'), self.onLocateInTopics)

        self._setupEncodingsSubMenu()

    def _setupNavigation(self):
        self.connect(self.nav_actionHome,
                QtCore.SIGNAL('triggered(bool)'), self.onGoHome)
        self.connect(self.nav_actionBack,
                QtCore.SIGNAL('triggered(bool)'), self.onGoBack)
        self.connect(self.nav_actionForward,
                QtCore.SIGNAL('triggered(bool)'), self.onGoForward)

    def _setupSettingsMenu(self):
        self.connect(self.settings_SettingsAction,
                QtCore.SIGNAL('triggered(bool)'), self.onSetting)

    def _setupHelpMenu(self):
        self.connect(self.actionAbout,
                QtCore.SIGNAL('triggered(bool)'), self.onAbout)

    def _setupMiscActions(self):
        self.connect(self.tabmanager,
                QtCore.SIGNAL('tabSwitched'), self.onTabSwitched)

        self.connect(self.tabmanager,
                QtCore.SIGNAL('checkToolBar'), self.onCheckToolBar)

        self.connect(self.tabmanager,
                     QtCore.SIGNAL('tabSwitched'),
                     self.topicsview.onTabSwitched,
                    )

        self.connect(self.tabmanager,
                     QtCore.SIGNAL('tabSwitched'),
                     self.indexview.onTabSwitched,
                    )

        self.connect(self.tabmanager,
                     QtCore.SIGNAL('tabSwitched'),
                     self.bookmarkview.onTabSwitched,
                    )

        self.connect(self.tabmanager,
                     QtCore.SIGNAL('tabSwitched'),
                     self.searchview.onTabSwitched,
                    )

        self.connect(self.bookmark_AddAction,
                QtCore.SIGNAL('triggered(bool)'), self.onAddBookmark)

    def _setupEncodingsSubMenu(self):
        encodings_menu = QMenu(self)
        self.groupOfEncodings = QtGui.QActionGroup(self)

        for language, encoding in encodings:
            action = QAction(self)
            action.setText( u"%s ( %s )" % (language, encoding) )
            action.encoding = encoding
            action.setCheckable(True)
            self.groupOfEncodings.addAction(action)
            encodings_menu.addAction(action)

        self.view_Set_encoding_action.setMenu(encodings_menu)

        self.connect(self.groupOfEncodings,
                     QtCore.SIGNAL('triggered(QAction*)'),
                     self.onEncodingChanged,
                    )


    def keyPressEvent(self, event):
        if event.matches(QtGui.QKeySequence.Open):
            self.onFileOpen()
        else:
            QtGui.QMainWindow.keyPressEvent(self, event)

    def closeEvent(self, event):
        self.config.save_into_file()
        self.tabmanager.saveTo(self.session.snapshot)
        self.storeLayoutInfo()

        # delegate other tasks to super class
        QtGui.QMainWindow.closeEvent(self, event)

    def storeLayoutInfo(self):
        settings = QtCore.QSettings()
        settings.setValue("mainwin/maximized", self.isMaximized() )
        settings.setValue("mainwin/geometry",  self.saveGeometry() )

    def restoreLayoutInfo(self):
        settings = QtCore.QSettings()
        geometry = settings.value("mainwin/geometry").toByteArray()
        maxmized = settings.value("mainwin/maximized").toBool()

        if maxmized:
            self.showMaximized()
        else:
            self.restoreGeometry(geometry)


    def onTabSwitched(self):
        self.onCheckToolBar()
        self.updateWindowTitle()

    def updateWindowTitle(self):
        if self.currentView:
            window_title = u"%s - PyChmViewer" % \
                          self.currentView.chmfile.title
        else:
            window_title = u"PyChmViewer"

        self.setWindowTitle(window_title)

    def onFileOpen(self):
        path = QtGui.QFileDialog.getOpenFileName(None,
                                                   u'Choose file',
                                                   self.config.lastdir,
                                                   u'CHM files (*.chm)',
                                                 )
        if path:
            path = unicode(path)
            # update lastdir after each succeful dialog
            self.config.lastdir = os.path.dirname(path)

            try:
                self.openFile(path)
            except IOError:
                # FIXME ; should give GUI warning, instead
                print ("[Error] failed to open: %s" % path)

    def openFile(self, path):
        self.tabmanager.openChmFile(path)

    def onAbout(self):
        dialog = AboutDialog(self)
        dialog.exec_()

    def onSetting(self):
        dialog = SettingDlg(mainwin=self, parent=self)
        if dialog.exec_() == QtGui.QDialog.Accepted:
            self.config.sessionRestore = dialog.sessionRestore
            self.config.fontfamily = unicode(dialog.fontfamily)
            self.config.fontsize = dialog.fontsize
            self.config.openRemoteURL = dialog.openRemoteURL

            self._setWebFont()
            for webview in self.tabmanager.webviews:
                webview.reload()

    def onViewSource(self):
        dialog = HtmlDialog(self)
        editor = dialog.sourceEdit
        editor.setPlainText(self.currentView.page().currentFrame().toHtml())
        editor.setWindowTitle(self.currentView.title())
        dialog.resize(800, 600)
        dialog.exec_()

    def onAddBookmark(self):
        self.bookmarkview.addBookmark()

    def onCheckToolBar(self):
        if self.currentView :
            self.nav_actionBack.setEnabled(   self.currentView.canGoBack() )
            self.nav_actionForward.setEnabled(self.currentView.canGoForward())
        else:
            self.nav_actionBack.setEnabled(False)
            self.nav_actionForward.setEnabled(False)


    def onEncodingChanged(self, action):
        self.currentView.onEncodingChanged(action.encoding)

    def onFilePrint(self):
        self.currentView.printPage()

    def onZoonIn(self):
        self.currentView.zoomIn()

    def onZoomOut(self):
        self.currentView.zoomOut()

    def onZoomOff(self):
        self.currentView.zoomOff()

    def onLocateInTopics(self):
        self.topicsview.locateUrl(self.currentView.loadedURL)

    def openInCurrentTab(self, url):
        self.currentView.loadURL(url)

    def onGoHome(self):
        self.currentView.goHome()

    def onGoBack(self):
        self.currentView.goBack()

    def onGoForward(self):
        self.currentView.goForward()

    def onExtractCurrentCHMFile(self):
        output_dir = QtGui.QFileDialog.getExistingDirectory(self,
                'select a directory to store files',
                '',
                QtGui.QFileDialog.ShowDirsOnly|QtGui.QFileDialog.DontResolveSymlinks)
        if not output_dir:
            return

        output_dir = unicode(output_dir).encode(self.session.system_encoding)

        chmfile = self.currentView.chmfile
        maximum = len( chmfile.allURLs )


        progress = QtGui.QProgressDialog(u'Extract chm file',
                                         u'Abort',
                                         0,
                                         maximum,
                                         self
                                         )
        progress.forceShow()

        reports = chmfile.extractAll(output_dir)
        logs = [ ]

        for index, report in enumerate(reports):
            logs.append(report)
            progress.setValue(index+1)
            if (index + 1) % 16 == 0 and progress.wasCanceled() :
                break

if __name__  ==  "__main__":
    raise NotImplementedError("")
