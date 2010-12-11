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

from pychmfile import PyChmFile
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

        # FIXME; 3 lines should be put into Ui_xxxx.py, not here
        self.WebViewsWidget = PyChmTabs(mainwin=self, parent=self.widget)
        self.WebViewsWidget.setObjectName(_fromUtf8("WebViewsWidget"))
        self.horizontalLayout.addWidget(self.WebViewsWidget)

        self.tabmanager = self.WebViewsWidget

        # FIXME; dirty hack; to be moved out after refactor
        self.tabmanager.onOpenAtNewTab(u'index.html')

        self._setupFileMenu()
        self._setupViewMenu()
        self._setupPanelMenu()
        self._setupPanelDock()
        self._setupNavigation()
        self._setupSettingsMenu()
        self._setupHelpMenu()
        self._setupMiscActions()
        self.setWebFont()

        if paths:
            self._startUpWithPathsGiven(paths)
        else:
            self._startUpWithPathsNotGiven()

    def _startUpCommon(self):
        pass

    def _startUpWithPathsGiven(self, paths):
        for path in paths:
            self.openFile(path)

    def _startUpWithPathsNotGiven(self):
        if self.config.loadlasttime:
            self.tabmanager.loadFrom(self.session.snapshot)

    @property
    def currentView(self):
        return self.tabmanager.currentView

    def setWebFont(self):
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
        self.connect(self.tabmanager,
                QtCore.SIGNAL('tabSwitched'), self.onTabSwitched)

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



    def onTabSwitched(self):
        self.onCheckToolBar()
        self.setWindowTitle( u"%s - PyChmViewer" %
                             self.currentView.chmfile.title
                           )


    def onOpenFile(self):
        path = QtGui.QFileDialog.getOpenFileName(None,
                                                   u'Choose file',
                                                   self.config.lastdir,
                                                   u'CHM files (*.chm)',
                                                 )
        path = unicode(path)

        try:
            self.openFile(path)
        except StandardError:
            print ("[Error] failed to open: %s" % path)

    def openFile(self, path):

        chmfile = PyChmFile(self.session, path)
        # FIXME; dirty hack; to be deleted
        #chmfile.session = self.session

        view = self.tabmanager.onOpenAtNewTab(chmfile.home)
        view.chmfile = chmfile


    def onAbout(self):
        dialog = AboutDialog(self)
        dialog.exec_()

    def onSetting(self):
        dialog = SettingDlg(mainwin=self, parent=self)
        if dialog.exec_() == QtGui.QDialog.Accepted:
            self.config.loadlasttime = dialog.loadlasttime
            self.config.fontfamily = unicode(dialog.fontfamily)
            self.config.fontsize = dialog.fontsize
            self.config.openremote = dialog.openremote
            self.config.searchext = dialog.searchext
            self.config.save_into_file()

            self.setWebFont()
            for window in self.tabmanager.windows:
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
        self.topicsview.locateUrl(self.currentView.openedpg)

    def openInCurrentTab(self, url):
        print "[debug] openInCurrentTab(): %s" % url
        self.currentView.openPage(url)

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
        self.tabmanager.saveTo(self.session.snapshot)
        event.accept()

if __name__  ==  "__main__":
    app = QtGui.QApplication(sys.argv)
    mainwin = PyChmMainWindow()
    mainwin.show()
    sys.exit(app.exec_())

