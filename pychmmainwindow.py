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

import globalvalue
from Ui_window_main import Ui_MainWindow
from pychmindex import PyChmIdxView
from pychmtopics import PyChmTopicsView
from pychmsearch import PyChmSearchView
from pychmbookmarks import PyChmBookmarksView
from config import PyChmConfig
from pychmfile import PyChmFile
from htmldlg import HtmlDlg
from encodinglist import encodings
from settingdlg import SettingDlg
from about import aboutdlg
from extract_chm import getfilelist

class PyChmMainWindow(QtGui.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self, parent)
        self.setupUi(self)

        self.actionIndex = self.dockIndex.toggleViewAction()
        self.actionIndex.setCheckable(True)
        self.actionIndex.setChecked(True)
        self.menu_Windows.addAction(self.actionIndex)

        self.actionTopics = self.dockTopics.toggleViewAction()
        self.actionTopics.setCheckable(True)
        self.actionTopics.setChecked(True)
        self.menu_Windows.addAction(self.actionTopics)

        self.actionSearch = self.dockSearch.toggleViewAction()
        self.actionSearch.setCheckable(True)
        self.actionSearch.setChecked(True)
        self.menu_Windows.addAction(self.actionSearch)

        self.actionBookmark = self.dockBookmark.toggleViewAction()
        self.actionBookmark.setCheckable(True)
        self.actionBookmark.setChecked(True)
        self.menu_Windows.addAction(self.actionBookmark)

        globalvalue.tabs = self.WebViewsWidget
        globalvalue.mainWindow = self

        self.tabifyDockWidget(self.dockIndex, self.dockTopics)
        self.tabifyDockWidget(self.dockIndex, self.dockSearch)
        self.tabifyDockWidget(self.dockIndex, self.dockBookmark)

        self.indexview = PyChmIdxView(self.dockIndex)
        self.dockIndex.setWidget(self.indexview)

        self.topicsview = PyChmTopicsView(self.dockTopics)
        self.dockTopics.setWidget(self.topicsview)

        self.searchview = PyChmSearchView(self.dockSearch)
        self.dockSearch.setWidget(self.searchview)

        self.bookmarkview = PyChmBookmarksView(self.dockBookmark)
        self.dockBookmark.setWidget(self.bookmarkview)

        self.connect(self.indexview, QtCore.SIGNAL('openUrl'), self.openincurrenttab)
        self.connect(self.topicsview, QtCore.SIGNAL('openUrl'), self.openincurrenttab)
        self.connect(self.searchview, QtCore.SIGNAL('openUrl'), self.openincurrenttab)
        self.connect(self.file_Open_action, QtCore.SIGNAL('triggered(bool)'), self.openFile)
        self.connect(self.file_Print_action, QtCore.SIGNAL('triggered(bool)'), self.onFilePrint)
        self.connect(self.view_Increase_font_size_action,
                QtCore.SIGNAL('triggered(bool)'), self.zoominview)
        self.connect(self.view_Decrease_font_size_action,
                QtCore.SIGNAL('triggered(bool)'), self.zoomoutview)
        self.connect(self.view_norm_font_size_action,
                QtCore.SIGNAL('triggered(bool)'), self.normview)
        self.connect(self.view_Locate_in_contents_action,
                QtCore.SIGNAL('triggered(bool)'), self.locateInTopics)
        self.connect(self.nav_actionHome,
                QtCore.SIGNAL('triggered(bool)'), self.viewHome)
        self.connect(self.nav_actionBack,
                QtCore.SIGNAL('triggered(bool)'), self.viewBack)
        self.connect(self.nav_actionForward,
                QtCore.SIGNAL('triggered(bool)'), self.viewForward)
        self.connect(self.WebViewsWidget,
                QtCore.SIGNAL('checkToolBar'), self.onCheckToolBar)
        self.connect(self.bookmark_AddAction,
                QtCore.SIGNAL('triggered(bool)'), self.onAddBookmark)
        self.connect(self.view_View_HTML_source_action,
                QtCore.SIGNAL('triggered(bool)'), self.onViewSource)
        self.connect(self.settings_SettingsAction,
                QtCore.SIGNAL('triggered(bool)'), self.onSetting)
        self.connect(self.actionAbout,
                QtCore.SIGNAL('triggered(bool)'), self.onAbout)
        self.connect(self.actionextract,
                QtCore.SIGNAL('triggered(bool)'), self.onExtractChm)

        self.addEncoding()
        self.inital()
        self.setWebFont()

    def onAbout(self):
        dlg = aboutdlg(self)
        dlg.exec_()

    def onSetting(self):
        dlg = SettingDlg(self)
        if dlg.exec_() == QtGui.QDialog.Accepted:
            globalvalue.globalcfg.loadlasttime = dlg.loadlasttime
            globalvalue.globalcfg.fontfamily = unicode(dlg.fontfamily)
            globalvalue.globalcfg.fontsize = dlg.fontsize
            globalvalue.globalcfg.openremote = dlg.openremote
            globalvalue.globalcfg.searchext = dlg.searchext
            globalvalue.globalcfg.savecfg()
            self.setWebFont()
            for v in self.WebViewsWidget.windows:
                v.reload()


    def setWebFont(self):
        st = QtWebKit.QWebSettings.globalSettings()
        if globalvalue.globalcfg.fontfamily is not None:
            st.setFontFamily(QtWebKit.QWebSettings.StandardFont, globalvalue.globalcfg.fontfamily)
            st.setFontFamily(QtWebKit.QWebSettings.FixedFont, globalvalue.globalcfg.fontfamily)
            st.setFontFamily(QtWebKit.QWebSettings.SerifFont, globalvalue.globalcfg.fontfamily)
            st.setFontFamily(QtWebKit.QWebSettings.SansSerifFont, globalvalue.globalcfg.fontfamily)
            st.setFontFamily(QtWebKit.QWebSettings.CursiveFont, globalvalue.globalcfg.fontfamily)
            st.setFontFamily(QtWebKit.QWebSettings.FantasyFont, globalvalue.globalcfg.fontfamily)
        if globalvalue.globalcfg.fontsize is not None:
            st.setFontSize(QtWebKit.QWebSettings.DefaultFontSize, globalvalue.globalcfg.fontsize)
            st.setFontSize(QtWebKit.QWebSettings.MinimumFontSize, globalvalue.globalcfg.fontsize)
            st.setFontSize(QtWebKit.QWebSettings.MinimumLogicalFontSize, globalvalue.globalcfg.fontsize)
            st.setFontSize(QtWebKit.QWebSettings.DefaultFixedFontSize, globalvalue.globalcfg.fontsize)
#            for v in self.WebViewsWidget.windows:
#                v.reload()


    def onViewSource(self):
        dlg = HtmlDlg(self)
        editor = dlg.sourceEdit
        editor.setPlainText(globalvalue.currentwebview.page().currentFrame().toHtml())
        editor.setWindowTitle(globalvalue.currentwebview.title())
        dlg.resize(800, 600)
        dlg.exec_()

    def onAddBookmark(self):
        self.bookmarkview.onAddPressed()

    def onCheckToolBar(self):
        if globalvalue.currentwebview == None:
            self.nav_actionBack.setEnabled(False)
            self.nav_actionForward.setEnabled(False)
            return
        if globalvalue.currentwebview.canback():
            self.nav_actionBack.setEnabled(True)
        else:
            self.nav_actionBack.setEnabled(False)
        if globalvalue.currentwebview.canforward():
            self.nav_actionForward.setEnabled(True)
        else:
            self.nav_actionForward.setEnabled(False)

    def addEncoding(self):
        encmenu = QMenu(self)
        self.genc = QtGui.QActionGroup(self)

        action = QAction(self)
        action.setText(u'auto')
        action.encoding = None
        action.setCheckable(True)
        action.setChecked(True)

        self.genc.addAction(action)
        encmenu.addAction(action)

        for language, encoding in encodings:
            action = QAction(self)
            action.setText(language + '-*- ' + encoding)
            action.encoding = encoding
            action.setCheckable(True)
            self.genc.addAction(action)
            encmenu.addAction(action)

        self.view_Set_encoding_action.setMenu(encmenu)
        self.connect(self.genc,QtCore.SIGNAL('triggered(QAction*)'),
                self.onEncodingChg)

    def onEncodingChg(self, action):
        globalvalue.encoding = action.encoding
        for window in self.WebViewsWidget.windows:
            window.reload()

    def inital(self):
        globalvalue.globalcfg.lastdir = os.path.dirname(globalvalue.chmpath)
        globalvalue.globalcfg.savecfg()
        self.conf = PyChmConfig(globalvalue.chmpath)
        self.bookmarkview.db = self.conf.bookmarkdb
        ok = False
        self.WebViewsWidget.closeAll()
        if len(self.conf.lastconfdb) != 0 and globalvalue.globalcfg.loadlasttime:
            ok = self.WebViewsWidget.loadfromdb(self.conf.lastconfdb)
        if not ok:
            self.WebViewsWidget.onOpenatNewTab(globalvalue.chmFile.HomeUrl)
        self.indexview.loaddata(globalvalue.chmFile.index)
        self.topicsview.loaddata(globalvalue.chmFile.topic)
        self.bookmarkview.loaddata()
        self.setWindowTitle(globalvalue.chmFile.Title+u' PyChmViewer')

    def openFile(self):
        file = QtGui.QFileDialog.getOpenFileName(None, u'choose file', globalvalue.globalcfg.lastdir,
                u'CHM files (*.chm)')
        chmpath = unicode(file)
        chmFile = PyChmFile()
        ok = chmFile.loadFile(chmpath)
        if not ok:
            mb = QtGui.QMessageBox(self)
            mb.setText(u'not open')
            mb.exec_()
            return
        else:
            globalvalue.chmpath = chmpath
            globalvalue.chmFile = chmFile
            self.WebViewsWidget.savealltab(self.conf.lastconfdb)
            self.indexview.dataloaded = False
            self.topicsview.dataloaded = False
            self.bookmarkview.dataloaded = False
            self.searchview.clear()
            self.inital()

    def onFilePrint(self):
        globalvalue.currentwebview.printPage()

    def zoominview(self):
        globalvalue.currentwebview.zoomin()

    def zoomoutview(self):
        globalvalue.currentwebview.zoomout()

    def normview(self):
        globalvalue.currentwebview.normsize()

    def locateInTopics(self):
        self.topicsview.locateUrl(globalvalue.currentwebview.openedpg)

    def openincurrenttab(self, url):
        globalvalue.currentwebview.openPage(url)

    def viewHome(self):
        globalvalue.currentwebview.openPage(globalvalue.chmFile.HomeUrl)

    def viewBack(self):
        globalvalue.currentwebview.back()

    def viewForward(self):
        globalvalue.currentwebview.forward()

    def closeEvent(self, e):
        self.WebViewsWidget.savealltab(self.conf.lastconfdb)
        e.accept()

    def onExtractChm(self):
        od = QtGui.QFileDialog.getExistingDirectory(self,
                'select a directory to store files',
                '',
                QtGui.QFileDialog.ShowDirsOnly|QtGui.QFileDialog.DontResolveSymlinks)
        if len(od) == 0:
            return
        ok, filelist = getfilelist(globalvalue.chmpath)
        if not ok:
            return
        prgrs = QtGui.QProgressDialog(u'Extract chm file', u'Abort',
               0, len(filelist),self)
        prgrs.forceShow()
        od = unicode(od).encode(sys.getfilesystemencoding())
        for i, opath in enumerate(filelist):
            prgrs.setValue(i)
            if i % 5 == 0:
                if prgrs.wasCanceled():
                    break
            fpath = opath.decode('utf-8').encode(sys.getfilesystemencoding())
            if fpath[0] != '/':
                fpath = '/' + fpath
            fpath = os.path.normpath(fpath)
            fpath = fpath[1:]
            fpath = os.path.join(od, fpath)
            fdir, file = os.path.split(fpath)
            try:
                os.makedirs(fdir)
            except StandardError:
                pass
            s = globalvalue.chmFile.GetFileAsStrByUrl(opath.decode('utf-8'))
            if s is None:
                #print 'extract',opath,'failed'
                continue
            try:
                file = open(fpath,'wb')
                file.write(s)
                file.flush()
                file.close()
                print ("extract: %s" % opath.decode('utf-8') )
            except StandardError:
                print ("cannot open %s" % fpath)
        prgrs.setValue(len(filelist))

if __name__  ==  "__main__":
    app = QtGui.QApplication(sys.argv)
    mainwin = PyChmMainWindow()
    mainwin.show()
    sys.exit(app.exec_())

