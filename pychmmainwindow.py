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
from config import PyChmConfig
from pychmfile import PyChmFile
from encodinglist import encodings
from settingdlg import SettingDlg
from htmldlg import HtmlDialog
from about import AboutDialog
from session import system_encoding
from utils import getchmfile, setchmfile, setencoding,  getcfg
from Ui_window_main import Ui_MainWindow


def setWebFont():
    config     = getcfg()
    fontfamily = config.fontfamily
    fontsize   = config.fontsize

    settings   = QtWebKit.QWebSettings.globalSettings()

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


class PyChmMainWindow(QtGui.QMainWindow, Ui_MainWindow):
    def __init__(self, session, parent=None):
        QtGui.QMainWindow.__init__(self, parent)
        self.setupUi(self)


        self._setupFileMenu()
        self._setupViewMenu()
        self._setupPanelMenu()
        self._setupPanelDock()
        self._setupNavigation()
        self._setupSettingsMenu()
        self._setupHelpMenu()
        self._setupMiscActions()

        self._setupEncodingsSubMenu()
        setWebFont()

        # FIXME ; these 2 lines are so dirty and evil
        # that it must die! ASAP!
        self.config = getcfg()

        #experimental
        self.session = session
        self.config = session.config
        self.tabmanager = self.WebViewsWidget
        #self.bookmarkview = None [done]
        #self.topicsview =  None

        self.initialize()

    @property
    def currentView(self):
        return self.tabmanager.currentView


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

        self.tabifyDockWidget(self.dockIndex, self.dockTopics)
        self.tabifyDockWidget(self.dockIndex, self.dockSearch)
        self.tabifyDockWidget(self.dockIndex, self.dockBookmark)

        #self.indexview = PyChmIndexView(self.dockIndex)
        self.indexview = PyChmIndexView(mainwin=self, parent=self.dockIndex)
        self.dockIndex.setWidget(self.indexview)

        #self.topicsview = PyChmTopicsView(self.dockTopics)
        self.topicsview = PyChmTopicsView(mainwin=self, parent=self.dockTopics)
        self.dockTopics.setWidget(self.topicsview)

        #self.searchview = PyChmSearchView(self.dockSearch)
        self.searchview = PyChmSearchView(mainwin=self, parent=self.dockSearch)
        self.dockSearch.setWidget(self.searchview)

        #self.bookmarkview = PyChmBookmarksView(self.dockBookmark)
        self.bookmarkview = PyChmBookmarksView(mainwin=self, parent=self.dockBookmark)
        self.dockBookmark.setWidget(self.bookmarkview)

        self.connect(self.indexview, QtCore.SIGNAL('openUrl'), self.openInCurrentTab)
        self.connect(self.topicsview, QtCore.SIGNAL('openUrl'), self.openInCurrentTab)
        self.connect(self.searchview, QtCore.SIGNAL('openUrl'), self.openInCurrentTab)

    def _setupFileMenu(self):
        self.connect(self.file_Open_action, QtCore.SIGNAL('triggered(bool)'), self.onOpenFile)
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
        self.connect(self.WebViewsWidget,
                QtCore.SIGNAL('checkToolBar'), self.onCheckToolBar)
        self.connect(self.bookmark_AddAction,
                QtCore.SIGNAL('triggered(bool)'), self.onAddBookmark)

    def _setupEncodingsSubMenu(self):
        encodings_menu = QMenu(self)
        self.groupOfEncodings = QtGui.QActionGroup(self)

        action = QAction(self)
        action.setText(u'Auto')
        action.encoding = None
        action.setCheckable(True)
        action.setChecked(True)

        self.groupOfEncodings.addAction(action)
        encodings_menu.addAction(action)

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

    def initialize(self):
        self.config.lastdir = os.path.dirname(getchmfile().path)
        self.config.save_into_file()
        self.conf = PyChmConfig(getchmfile().path)
        self.bookmarkview.db = self.conf.bookmarkdb
        ok = False
        self.WebViewsWidget.closeAll()
        if self.conf.lastconfdb and self.config.loadlasttime:
            ok = self.WebViewsWidget.loadFrom(self.conf.lastconfdb)
        if not ok:
            self.WebViewsWidget.onOpenAtNewTab(getchmfile().home)
        self.indexview.loadIndex(getchmfile().index)
        self.bookmarkview.loadBookmarks()
        self.topicsview.loadTopics(getchmfile().topics)
        self.setWindowTitle(getchmfile().title + u' PyChmViewer')


    def onOpenFile(self):
        choice = QtGui.QFileDialog.getOpenFileName(None,
                                                   u'choose file',
                                                   self.config.lastdir,
                                                   u'CHM files (*.chm)',
                                                 )
        chmpath = unicode(choice)
        chmfile = PyChmFile()
        ok = chmfile.loadFile(chmpath)
        if ok:
            setchmfile(chmfile)
            self.WebViewsWidget.saveTo(self.conf.lastconfdb)
            self.indexview.dataloaded = False
            self.bookmarkview.dataloaded = False
            self.topicsview.clear()
            self.searchview.clear()
            self.initialize()

    def onAbout(self):
        dialog = AboutDialog(self)
        dialog.exec_()

    def onSetting(self):
        dialog = SettingDlg(self)
        if dialog.exec_() == QtGui.QDialog.Accepted:
            self.config.loadlasttime = dialog.loadlasttime
            self.config.fontfamily = unicode(dialog.fontfamily)
            self.config.fontsize = dialog.fontsize
            self.config.openremote = dialog.openremote
            self.config.searchext = dialog.searchext
            self.config.save_into_file()
            setWebFont()
            for window in self.WebViewsWidget.windows:
                window.reload()

    def onViewSource(self):
        dialog = HtmlDialog(self)
        editor = dialog.sourceEdit
        editor.setPlainText(self.currentView.page().currentFrame().toHtml())
        editor.setWindowTitle(self.currentView.title())
        dialog.resize(800, 600)
        dialog.exec_()

    def onAddBookmark(self):
        self.bookmarkview.onAddPressed()

    def onCheckToolBar(self):
        if self.currentView is None:
            self.nav_actionBack.setEnabled(False)
            self.nav_actionForward.setEnabled(False)
            return
        if self.currentView.canGoBack():
            self.nav_actionBack.setEnabled(True)
        else:
            self.nav_actionBack.setEnabled(False)
        if self.currentView.canGoForward():
            self.nav_actionForward.setEnabled(True)
        else:
            self.nav_actionForward.setEnabled(False)


    def onEncodingChanged(self, action):

        view = self.currentView
        view.onEncodingChanged(action.encoding)
        setencoding(action.encoding)

        for window in self.WebViewsWidget.windows:
            window.reload()

    def onFilePrint(self):
        self.currentView.printPage()

    def onZoonIn(self):
        self.currentView.zoomIn()

    def onZoomOut(self):
        self.currentView.zoomOut()

    def onZoomOff(self):
        self.currentView.normsize()

    def onLocateInTopics(self):
        self.topicsview.locateUrl(self.currentView.openedpg)

    def openInCurrentTab(self, url):
        print "[debug] trying to open url: %s" % url
        self.currentView.openPage(url)

    def onGoHome(self):
        self.currentView.openPage(getchmfile().home)

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

        output_dir = unicode(output_dir).encode(system_encoding)

        chmfile = getchmfile()
        maximum = len( chmfile.getURLs() )


        progress = QtGui.QProgressDialog(u'Extract chm file',
                                         u'Abort',
                                         0,
                                         maximum,
                                         self
                                         )
        progress.forceShow()

        reports = chmfile.extractAll(output_dir)
        logs = [ ]

        counter = 1
        for report in reports:
            progress.setValue(counter)
            counter += 1
            if counter % 16 == 0 and progress.wasCanceled() :
                break
            logs.append(report)


    def closeEvent(self, event):
        self.WebViewsWidget.saveTo(self.conf.lastconfdb)
        event.accept()

if __name__  ==  "__main__":
    app = QtGui.QApplication(sys.argv)
    mainwin = PyChmMainWindow()
    mainwin.show()
    sys.exit(app.exec_())

