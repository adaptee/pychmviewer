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
from Ui_mainwindow import Ui_MainWindow

from recentfiles import QtRecentFiles

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s


#TODO
# fullscreen mode:
# void QWidget::showFullScreen ()
# void QWidget::showNormal ()
# bool  isFullScreen () const
# Qt::WindowStates QWidget::windowState ()



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
        self._setupEditMenu()
        self._setupViewMenu()
        self._setupPanelMenu()
        self._setupPanelDock()
        self._setupBookmarkMenu()
        self._setupTabsMenu()
        self._setupSettingsMenu()
        self._setupHelpMenu()
        self._setupNavigation()
        self._setupMiscActions()
        self._setWebFont()

        settings = QtWebKit.QWebSettings.globalSettings()
        settings.setAttribute(QtWebKit.QWebSettings.JavascriptEnabled, True)
        #settings.setAttribute(QtWebKit.QWebSettings.PluginsEnabled, True)

        self._setupRecentFiles()

        if paths:
            self._startUpWithPaths(paths)
        else:
            self._startUpWithNoPaths()

    def _setupRecentFiles(self):
        self.recentfiles = QtRecentFiles(10, self)
        self.connect(self.recentfiles,
                    QtCore.SIGNAL('recentFilesUpdated'),
                    self.onRecentFilesUpdated ,
                    )

        self.onRecentFilesUpdated()

        self.connect(self.tabmanager,
                    QtCore.SIGNAL('fileOpened'),
                    self.onFileOpened2 ,
                    )

        self.connect(self.tabmanager,
                    QtCore.SIGNAL('fileNotOpened'),
                    self.onFileNotOpened2 ,
                    )

        self.connect(self.tabmanager,
                    QtCore.SIGNAL('fileOpened'),
                    self.onFileOpened ,
                    )

        self.connect(self.tabmanager,
                    QtCore.SIGNAL('fileNotOpened'),
                    self.onFileNotOpened ,
                    )

    def onRecentFilesUpdated(self):

        actions = self.recentfiles.actions

        if actions:
            menu = QMenu(self)

            for action in self.recentfiles.actions:
                menu.addAction(action)

            menu.addSeparator()

            actionClearRecentFiles = QAction(self)
            actionClearRecentFiles.setText(u"Clear list")

            self.connect(actionClearRecentFiles,
                         QtCore.SIGNAL("triggered(bool)"),
                         self.onClearRecentFiles2
                        )

            menu.addAction(actionClearRecentFiles)

            self.actionOpenRecents.setMenu(menu)
            self.actionOpenRecents.setEnabled(True)
        else:
            self.actionOpenRecents.setEnabled(False)


    def onFileOpened2(self, path):
        self.recentfiles.onFileOpened(path)

    def onFileNotOpened2(self, path):
        self.recentfiles.onFileNotOpened(path)

    def onClearRecentFiles2(self):
        self.recentfiles.onClearRecentFiles()

    def onFileOpened(self, path) :
        pass

    def onFileNotOpened(self, path) :
        QtGui.QMessageBox.warning( self,
                                   u"Failed to open file",
                                   u"%s does not exist" % path,
                                  )


    def _startUpWithPaths(self, paths):
        for path in paths:
            try:
                self.openFile(path)
            except IOError:
                pass

    def _startUpWithNoPaths(self):
        if self.config.sessionRestore:
            try:
                self.tabmanager.loadFrom(self.session.snapshot)
            except StandardError:
                # ignore failures cause by non-existing-anymore files
                pass


    def _setupFileMenu(self):
        self.connect(self.actionOpenFile,
                     QtCore.SIGNAL('triggered(bool)'),
                     self.onOpenFile)
        self.connect(self.actionPrintPage,
                     QtCore.SIGNAL('triggered(bool)'),
                     self.onPrintPage)
        self.connect(self.actionExtractFile,
                     QtCore.SIGNAL('triggered(bool)'),
                     self.onExtractFile)
        self.connect(self.actionQuitApp,
                     QtCore.SIGNAL('triggered(bool)'),
                     self.onQuitApp)

    def onOpenFile(self):
        path = QtGui.QFileDialog.getOpenFileName(None,
                                                 u'Choose file',
                                                 self.config.lastdir,
                                                 u'CHM files (*.chm)',
                                                 )
        if path:
            path = unicode(path)
            # update lastdir after each succeful dialog
            self.config.lastdir = os.path.dirname(path)

            self.openFile(path)

    def onPrintPage(self):
        self.currentView.printPage()

    def onExtractFile(self):
        output_dir = QtGui.QFileDialog.getExistingDirectory(self,
                "select a directory to store files",
                "",
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

    def onQuitApp(self):
        self.close()


    def _setupEditMenu(self):
        self.connect(self.actionCopy,
                     QtCore.SIGNAL('triggered(bool)'),
                     self.onCopy)

        self.connect(self.actionSelectAll,
                     QtCore.SIGNAL('triggered(bool)'),
                     self.onSelectAll)

        self.connect(self.actionFind,
                     QtCore.SIGNAL('triggered(bool)'),
                     self.onFind)

        self.connect(self.actionFindNext,
                     QtCore.SIGNAL('triggered(bool)'),
                     self.onFindNext)

        self.connect(self.actionFindPrevious,
                     QtCore.SIGNAL('triggered(bool)'),
                     self.onFindPrevious)

    def onCopy(self):
        self.currentView.onCopy()

    def onSelectAll(self):
        self.currentView.onSelectAll()

    def onFind(self):
        self.tabmanager.onFind()

    def onFindNext(self):
        self.tabmanager.onFindNext()

    def onFindPrevious(self):
        self.tabmanager.onFindPrevious()


    def _setupViewMenu(self):
        self.connect(self.actionZoomIn,
                     QtCore.SIGNAL('triggered(bool)'),
                     self.onZoonIn)
        self.connect(self.actionZoomOut,
                     QtCore.SIGNAL('triggered(bool)'),
                     self.onZoomOut)
        self.connect(self.actionZoomOff,
                     QtCore.SIGNAL('triggered(bool)'),
                     self.onZoomOff)
        self.connect(self.actionViewHtmlSource,
                     QtCore.SIGNAL('triggered(bool)'),
                     self.onViewHtmlSource)
        self.connect(self.actionLocate,
                     QtCore.SIGNAL('triggered(bool)'),
                     self.onLocateInTopics)

        self._setupEncodingsSubMenu()




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

        self.actionChangeEncoding.setMenu(encodings_menu)

        self.connect(self.groupOfEncodings,
                     QtCore.SIGNAL('triggered(QAction*)'),
                     self.onEncodingChanged,
                    )

    def onZoonIn(self):
        self.currentView.zoomIn()

    def onZoomOut(self):
        self.currentView.zoomOut()

    def onZoomOff(self):
        self.currentView.zoomOff()

    def onEncodingChanged(self, action):
        self.currentView.onEncodingChanged(action.encoding)

    def onViewHtmlSource(self):
        dialog = HtmlDialog(self)
        editor = dialog.sourceEdit
        editor.setPlainText(self.currentView.page().currentFrame().toHtml())
        editor.setWindowTitle(self.currentView.title())
        dialog.resize(800, 600)
        dialog.exec_()

    def onLocateInTopics(self):
        self.topicsview.locateUrl(self.currentView.loadedURL)



    def _setupBookmarkMenu(self):

        self.connect(self.actionAddBookmark,
                     QtCore.SIGNAL('triggered(bool)'),
                     self.onAddBookmark)

    def onAddBookmark(self):
        self.bookmarkview.onAddBookmark()


    def _setupTabsMenu(self):

        self.connect(self.actionOpenNewTab,
                     QtCore.SIGNAL('triggered(bool)'),
                     self.onOpenNewTab)

        self.connect(self.actionCloseCurrentTab,
                     QtCore.SIGNAL('triggered(bool)'),
                     self.onCloseCurrentTab)

    def onOpenNewTab(self):
        self.tabmanager.onOpenNewTab()

    def onCloseCurrentTab(self):
        self.tabmanager.onCloseCurrentTab()


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

        self.connect(self.actionTogglePanels,
                     QtCore.SIGNAL('triggered(bool)'),
                     self.onTogglePanels)

        self.actionIndex = self.dockIndex.toggleViewAction()
        self.actionIndex.setCheckable(True)
        self.actionIndex.setChecked(True)
        self.menuPanels.addAction(self.actionIndex)

        self.actionTopics = self.dockTopics.toggleViewAction()
        self.actionTopics.setCheckable(True)
        self.actionTopics.setChecked(True)
        self.menuPanels.addAction(self.actionTopics)

        self.actionSearch = self.dockSearch.toggleViewAction()
        self.actionSearch.setCheckable(True)
        self.actionSearch.setChecked(True)
        self.menuPanels.addAction(self.actionSearch)

        self.actionBookmark = self.dockBookmark.toggleViewAction()
        self.actionBookmark.setCheckable(True)
        self.actionBookmark.setChecked(True)
        self.menuPanels.addAction(self.actionBookmark)

    def onTogglePanels(self):
        pass

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

        self.connect(self.indexview,
                     QtCore.SIGNAL('openURL'),
                     self.openInCurrentTab)
        self.connect(self.topicsview,
                     QtCore.SIGNAL('openURL'),
                     self.openInCurrentTab)
        self.connect(self.searchview,
                     QtCore.SIGNAL('openURL'),
                     self.openInCurrentTab)

        # Topics is the most useful one, so activiate it by force
        self.dockTopics.activateWindow()
        self.dockTopics.raise_()

    def _setupSettingsMenu(self):
        self.connect(self.actionOpenSettings,
                     QtCore.SIGNAL('triggered(bool)'),
                     self.onOpenSettings)

    def onOpenSettings(self):
        dialog = SettingDlg(mainwin=self, parent=self)
        if dialog.exec_() == QtGui.QDialog.Accepted:
            self.config.sessionRestore = dialog.sessionRestore
            self.config.fontfamily = unicode(dialog.fontfamily)
            self.config.fontsize = dialog.fontsize
            self.config.openRemoteURL = dialog.openRemoteURL

            self._setWebFont()
            for webview in self.tabmanager.webviews:
                webview.reload()

    def _setupHelpMenu(self):
        self.connect(self.actionAboutApp,
                     QtCore.SIGNAL('triggered(bool)'),
                     self.onAboutApp)
        self.connect(self.actionAboutQt,
                     QtCore.SIGNAL('triggered(bool)'),
                     self.onAboutQt)

    def onAboutApp(self):
        dialog = AboutDialog(self)
        dialog.exec_()

    def onAboutQt(self):
        QtGui.QMessageBox.aboutQt(self,
                            title=QtCore.QCoreApplication.applicationName() )

    def _setupNavigation(self):
        self.connect(self.actionGoHome,
                     QtCore.SIGNAL('triggered(bool)'),
                     self.onGoHome)
        self.connect(self.actionGoBack,
                     QtCore.SIGNAL('triggered(bool)'),
                     self.onGoBack)
        self.connect(self.actionGoForward,
                     QtCore.SIGNAL('triggered(bool)'),
                     self.onGoForward)

    def onGoHome(self):
        self.currentView.goHome()

    def onGoBack(self):
        self.currentView.goBack()

    def onGoForward(self):
        self.currentView.goForward()


    def _setupMiscActions(self):
        self.connect(self.tabmanager,
                     QtCore.SIGNAL('tabSwitched'),
                     self.onTabSwitched)


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

        self.connect(self.tabmanager,
                     QtCore.SIGNAL('checkToolBar'),
                     self.onCheckToolBar)

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

    def onCheckToolBar(self):
        if self.currentView :
            self.actionGoBack.setEnabled(   self.currentView.canGoBack() )
            self.actionGoForward.setEnabled(self.currentView.canGoForward())
        else:
            self.actionGoBack.setEnabled(False)
            self.actionGoForward.setEnabled(False)


    def openFile(self, path):
        self.tabmanager.openChmFile(path)

    def openInCurrentTab(self, url):
        self.currentView.loadURL(url)

    @property
    def currentView(self):
        return self.tabmanager.currentView

    def closeEvent(self, event):
        self.config.save_into_file()
        self.tabmanager.saveTo(self.session.snapshot)
        self.storeLayoutInfo()
        self.recentfiles.saveRecentFiles()

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

