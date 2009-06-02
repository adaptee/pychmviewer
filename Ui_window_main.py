# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/john/git/pychmviewer/window_main.ui'
#
# Created: Tue Jun  2 22:39:36 2009
#      by: PyQt4 UI code generator 4.4.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(873, 591)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/images/pychmviewer.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        MainWindow.setDockOptions(QtGui.QMainWindow.AllowTabbedDocks|QtGui.QMainWindow.AnimatedDocks)
        self.widget = QtGui.QWidget(MainWindow)
        self.widget.setObjectName("widget")
        self.horizontalLayout = QtGui.QHBoxLayout(self.widget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.WebViewsWidget = PyChmTabs(self.widget)
        self.WebViewsWidget.setObjectName("WebViewsWidget")
        self.horizontalLayout.addWidget(self.WebViewsWidget)
        MainWindow.setCentralWidget(self.widget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 873, 24))
        self.menubar.setObjectName("menubar")
        self.menu_Settings = QtGui.QMenu(self.menubar)
        self.menu_Settings.setObjectName("menu_Settings")
        self.menu_File = QtGui.QMenu(self.menubar)
        self.menu_File.setObjectName("menu_File")
        self.menu_View = QtGui.QMenu(self.menubar)
        self.menu_View.setObjectName("menu_View")
        self.menu_Windows = QtGui.QMenu(self.menubar)
        self.menu_Windows.setObjectName("menu_Windows")
        self.menuHelp = QtGui.QMenu(self.menubar)
        self.menuHelp.setObjectName("menuHelp")
        MainWindow.setMenuBar(self.menubar)
        self.mainToolbar = QtGui.QToolBar(MainWindow)
        self.mainToolbar.setOrientation(QtCore.Qt.Horizontal)
        self.mainToolbar.setObjectName("mainToolbar")
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.mainToolbar)
        self.navToolbar = QtGui.QToolBar(MainWindow)
        self.navToolbar.setOrientation(QtCore.Qt.Horizontal)
        self.navToolbar.setObjectName("navToolbar")
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.navToolbar)
        self.viewToolbar = QtGui.QToolBar(MainWindow)
        self.viewToolbar.setOrientation(QtCore.Qt.Horizontal)
        self.viewToolbar.setObjectName("viewToolbar")
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.viewToolbar)
        self.mainStatusBar = QtGui.QStatusBar(MainWindow)
        self.mainStatusBar.setObjectName("mainStatusBar")
        MainWindow.setStatusBar(self.mainStatusBar)
        self.dockTopics = QtGui.QDockWidget(MainWindow)
        self.dockTopics.setAcceptDrops(False)
        self.dockTopics.setObjectName("dockTopics")
        self.dockWidgetContents = QtGui.QWidget()
        self.dockWidgetContents.setObjectName("dockWidgetContents")
        self.dockTopics.setWidget(self.dockWidgetContents)
        MainWindow.addDockWidget(QtCore.Qt.DockWidgetArea(1), self.dockTopics)
        self.dockIndex = QtGui.QDockWidget(MainWindow)
        self.dockIndex.setObjectName("dockIndex")
        self.dockWidgetContents_2 = QtGui.QWidget()
        self.dockWidgetContents_2.setObjectName("dockWidgetContents_2")
        self.dockIndex.setWidget(self.dockWidgetContents_2)
        MainWindow.addDockWidget(QtCore.Qt.DockWidgetArea(1), self.dockIndex)
        self.dockSearch = QtGui.QDockWidget(MainWindow)
        self.dockSearch.setObjectName("dockSearch")
        self.dockWidgetContents_3 = QtGui.QWidget()
        self.dockWidgetContents_3.setObjectName("dockWidgetContents_3")
        self.dockSearch.setWidget(self.dockWidgetContents_3)
        MainWindow.addDockWidget(QtCore.Qt.DockWidgetArea(1), self.dockSearch)
        self.dockBookmark = QtGui.QDockWidget(MainWindow)
        self.dockBookmark.setObjectName("dockBookmark")
        self.dockWidgetContents_4 = QtGui.QWidget()
        self.dockWidgetContents_4.setObjectName("dockWidgetContents_4")
        self.dockBookmark.setWidget(self.dockWidgetContents_4)
        MainWindow.addDockWidget(QtCore.Qt.DockWidgetArea(1), self.dockBookmark)
        self.file_Print_action = QtGui.QAction(MainWindow)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/images/icon_print.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.file_Print_action.setIcon(icon1)
        self.file_Print_action.setObjectName("file_Print_action")
        self.file_exit_action = QtGui.QAction(MainWindow)
        self.file_exit_action.setObjectName("file_exit_action")
        self.edit_Copy_action = QtGui.QAction(MainWindow)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/images/icon_copy.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.edit_Copy_action.setIcon(icon2)
        self.edit_Copy_action.setObjectName("edit_Copy_action")
        self.edit_SelectAll_action = QtGui.QAction(MainWindow)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap("../../.designer/backup/image8"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.edit_SelectAll_action.setIcon(icon3)
        self.edit_SelectAll_action.setObjectName("edit_SelectAll_action")
        self.edit_FindAction = QtGui.QAction(MainWindow)
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(":/images/icon_find.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.edit_FindAction.setIcon(icon4)
        self.edit_FindAction.setObjectName("edit_FindAction")
        self.file_ExtractCHMAction = QtGui.QAction(MainWindow)
        self.file_ExtractCHMAction.setObjectName("file_ExtractCHMAction")
        self.settings_SettingsAction = QtGui.QAction(MainWindow)
        self.settings_SettingsAction.setObjectName("settings_SettingsAction")
        self.bookmark_AddAction = QtGui.QAction(MainWindow)
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap(":/images/icon_add_bookmark.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.bookmark_AddAction.setIcon(icon5)
        self.bookmark_AddAction.setObjectName("bookmark_AddAction")
        self.view_Increase_font_size_action = QtGui.QAction(MainWindow)
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap(":/images/icon_font_increase.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.view_Increase_font_size_action.setIcon(icon6)
        self.view_Increase_font_size_action.setObjectName("view_Increase_font_size_action")
        self.view_Decrease_font_size_action = QtGui.QAction(MainWindow)
        icon7 = QtGui.QIcon()
        icon7.addPixmap(QtGui.QPixmap(":/images/icon_font_decrease.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.view_Decrease_font_size_action.setIcon(icon7)
        self.view_Decrease_font_size_action.setObjectName("view_Decrease_font_size_action")
        self.view_norm_font_size_action = QtGui.QAction(MainWindow)
        icon8 = QtGui.QIcon()
        icon8.addPixmap(QtGui.QPixmap(":/images/icon_font_norm.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.view_norm_font_size_action.setIcon(icon8)
        self.view_norm_font_size_action.setObjectName("view_norm_font_size_action")
        self.view_View_HTML_source_action = QtGui.QAction(MainWindow)
        icon9 = QtGui.QIcon()
        icon9.addPixmap(QtGui.QPixmap(":/images/icon_view_source.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.view_View_HTML_source_action.setIcon(icon9)
        self.view_View_HTML_source_action.setObjectName("view_View_HTML_source_action")
        self.view_Toggle_fullscreen_action = QtGui.QAction(MainWindow)
        self.view_Toggle_fullscreen_action.setCheckable(True)
        self.view_Toggle_fullscreen_action.setAutoRepeat(False)
        self.view_Toggle_fullscreen_action.setObjectName("view_Toggle_fullscreen_action")
        self.view_Toggle_contents_action = QtGui.QAction(MainWindow)
        self.view_Toggle_contents_action.setCheckable(True)
        self.view_Toggle_contents_action.setChecked(True)
        self.view_Toggle_contents_action.setAutoRepeat(False)
        self.view_Toggle_contents_action.setObjectName("view_Toggle_contents_action")
        self.view_Locate_in_contents_action = QtGui.QAction(MainWindow)
        icon10 = QtGui.QIcon()
        icon10.addPixmap(QtGui.QPixmap(":/images/icon_locate_in_content.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.view_Locate_in_contents_action.setIcon(icon10)
        self.view_Locate_in_contents_action.setObjectName("view_Locate_in_contents_action")
        self.view_Set_encoding_action = QtGui.QAction(MainWindow)
        self.view_Set_encoding_action.setObjectName("view_Set_encoding_action")
        self.file_Open_action = QtGui.QAction(MainWindow)
        icon11 = QtGui.QIcon()
        icon11.addPixmap(QtGui.QPixmap(":/images/icon_open_file.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.file_Open_action.setIcon(icon11)
        self.file_Open_action.setObjectName("file_Open_action")
        self.nav_actionBack = QtGui.QAction(MainWindow)
        icon12 = QtGui.QIcon()
        icon12.addPixmap(QtGui.QPixmap(":/images/icon_back.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.nav_actionBack.setIcon(icon12)
        self.nav_actionBack.setObjectName("nav_actionBack")
        self.nav_actionForward = QtGui.QAction(MainWindow)
        icon13 = QtGui.QIcon()
        icon13.addPixmap(QtGui.QPixmap(":/images/icon_forward.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.nav_actionForward.setIcon(icon13)
        self.nav_actionForward.setObjectName("nav_actionForward")
        self.nav_actionHome = QtGui.QAction(MainWindow)
        icon14 = QtGui.QIcon()
        icon14.addPixmap(QtGui.QPixmap(":/images/icon_home.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.nav_actionHome.setIcon(icon14)
        self.nav_actionHome.setObjectName("nav_actionHome")
        self.actionAbout = QtGui.QAction(MainWindow)
        self.actionAbout.setObjectName("actionAbout")
        self.menu_Settings.addAction(self.settings_SettingsAction)
        self.menu_File.addAction(self.file_Open_action)
        self.menu_File.addAction(self.file_Print_action)
        self.menu_View.addAction(self.view_Increase_font_size_action)
        self.menu_View.addAction(self.view_Decrease_font_size_action)
        self.menu_View.addAction(self.view_norm_font_size_action)
        self.menu_View.addAction(self.view_View_HTML_source_action)
        self.menu_View.addSeparator()
        self.menu_View.addAction(self.view_Locate_in_contents_action)
        self.menu_View.addSeparator()
        self.menu_View.addAction(self.view_Set_encoding_action)
        self.menuHelp.addAction(self.actionAbout)
        self.menubar.addAction(self.menu_File.menuAction())
        self.menubar.addAction(self.menu_View.menuAction())
        self.menubar.addAction(self.menu_Windows.menuAction())
        self.menubar.addAction(self.menu_Settings.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())
        self.mainToolbar.addAction(self.file_Open_action)
        self.mainToolbar.addAction(self.file_Print_action)
        self.navToolbar.addAction(self.nav_actionHome)
        self.navToolbar.addAction(self.nav_actionBack)
        self.navToolbar.addAction(self.nav_actionForward)
        self.viewToolbar.addAction(self.view_Locate_in_contents_action)
        self.viewToolbar.addAction(self.view_Increase_font_size_action)
        self.viewToolbar.addAction(self.view_Decrease_font_size_action)
        self.viewToolbar.addAction(self.view_norm_font_size_action)
        self.viewToolbar.addAction(self.view_View_HTML_source_action)
        self.viewToolbar.addAction(self.bookmark_AddAction)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "pychmviewer", None, QtGui.QApplication.UnicodeUTF8))
        self.menu_Settings.setTitle(QtGui.QApplication.translate("MainWindow", "&Settings", None, QtGui.QApplication.UnicodeUTF8))
        self.menu_File.setTitle(QtGui.QApplication.translate("MainWindow", "&File", None, QtGui.QApplication.UnicodeUTF8))
        self.menu_View.setTitle(QtGui.QApplication.translate("MainWindow", "&View", None, QtGui.QApplication.UnicodeUTF8))
        self.menu_Windows.setTitle(QtGui.QApplication.translate("MainWindow", "&Windows", None, QtGui.QApplication.UnicodeUTF8))
        self.menuHelp.setTitle(QtGui.QApplication.translate("MainWindow", "Help", None, QtGui.QApplication.UnicodeUTF8))
        self.mainToolbar.setWindowTitle(QtGui.QApplication.translate("MainWindow", "general toolbar", None, QtGui.QApplication.UnicodeUTF8))
        self.navToolbar.setWindowTitle(QtGui.QApplication.translate("MainWindow", "navigation toolbar", None, QtGui.QApplication.UnicodeUTF8))
        self.viewToolbar.setWindowTitle(QtGui.QApplication.translate("MainWindow", "action toolbar", None, QtGui.QApplication.UnicodeUTF8))
        self.dockTopics.setStatusTip(QtGui.QApplication.translate("MainWindow", "Topics", None, QtGui.QApplication.UnicodeUTF8))
        self.dockTopics.setWindowTitle(QtGui.QApplication.translate("MainWindow", "Topics", None, QtGui.QApplication.UnicodeUTF8))
        self.dockIndex.setStatusTip(QtGui.QApplication.translate("MainWindow", "Index", None, QtGui.QApplication.UnicodeUTF8))
        self.dockIndex.setWindowTitle(QtGui.QApplication.translate("MainWindow", "Index", None, QtGui.QApplication.UnicodeUTF8))
        self.dockSearch.setStatusTip(QtGui.QApplication.translate("MainWindow", "Search", None, QtGui.QApplication.UnicodeUTF8))
        self.dockSearch.setWindowTitle(QtGui.QApplication.translate("MainWindow", "Search", None, QtGui.QApplication.UnicodeUTF8))
        self.dockBookmark.setStatusTip(QtGui.QApplication.translate("MainWindow", "Bookmark", None, QtGui.QApplication.UnicodeUTF8))
        self.dockBookmark.setWindowTitle(QtGui.QApplication.translate("MainWindow", "Bookmark", None, QtGui.QApplication.UnicodeUTF8))
        self.file_Print_action.setText(QtGui.QApplication.translate("MainWindow", "&Print...", None, QtGui.QApplication.UnicodeUTF8))
        self.file_Print_action.setIconText(QtGui.QApplication.translate("MainWindow", "Print", None, QtGui.QApplication.UnicodeUTF8))
        self.file_Print_action.setToolTip(QtGui.QApplication.translate("MainWindow", "Print current page", None, QtGui.QApplication.UnicodeUTF8))
        self.file_Print_action.setWhatsThis(QtGui.QApplication.translate("MainWindow", "Prints currently opened page.", None, QtGui.QApplication.UnicodeUTF8))
        self.file_Print_action.setShortcut(QtGui.QApplication.translate("MainWindow", "Ctrl+P", None, QtGui.QApplication.UnicodeUTF8))
        self.file_exit_action.setText(QtGui.QApplication.translate("MainWindow", "&Quit", None, QtGui.QApplication.UnicodeUTF8))
        self.file_exit_action.setIconText(QtGui.QApplication.translate("MainWindow", "Exit", None, QtGui.QApplication.UnicodeUTF8))
        self.file_exit_action.setWhatsThis(QtGui.QApplication.translate("MainWindow", "Exits the application", None, QtGui.QApplication.UnicodeUTF8))
        self.file_exit_action.setShortcut(QtGui.QApplication.translate("MainWindow", "Ctrl+Q", None, QtGui.QApplication.UnicodeUTF8))
        self.edit_Copy_action.setText(QtGui.QApplication.translate("MainWindow", "C&opy", None, QtGui.QApplication.UnicodeUTF8))
        self.edit_Copy_action.setIconText(QtGui.QApplication.translate("MainWindow", "Copy", None, QtGui.QApplication.UnicodeUTF8))
        self.edit_Copy_action.setWhatsThis(QtGui.QApplication.translate("MainWindow", "Copies selected content to clipboard", None, QtGui.QApplication.UnicodeUTF8))
        self.edit_Copy_action.setShortcut(QtGui.QApplication.translate("MainWindow", "Ctrl+C", None, QtGui.QApplication.UnicodeUTF8))
        self.edit_SelectAll_action.setText(QtGui.QApplication.translate("MainWindow", "&Select All", None, QtGui.QApplication.UnicodeUTF8))
        self.edit_SelectAll_action.setIconText(QtGui.QApplication.translate("MainWindow", "Paste", None, QtGui.QApplication.UnicodeUTF8))
        self.edit_SelectAll_action.setWhatsThis(QtGui.QApplication.translate("MainWindow", "Selects everything in the document", None, QtGui.QApplication.UnicodeUTF8))
        self.edit_SelectAll_action.setShortcut(QtGui.QApplication.translate("MainWindow", "Ctrl+V", None, QtGui.QApplication.UnicodeUTF8))
        self.edit_FindAction.setText(QtGui.QApplication.translate("MainWindow", "&Find...", None, QtGui.QApplication.UnicodeUTF8))
        self.edit_FindAction.setIconText(QtGui.QApplication.translate("MainWindow", "Find", None, QtGui.QApplication.UnicodeUTF8))
        self.edit_FindAction.setToolTip(QtGui.QApplication.translate("MainWindow", "Find text in currently opened page", None, QtGui.QApplication.UnicodeUTF8))
        self.edit_FindAction.setWhatsThis(QtGui.QApplication.translate("MainWindow", "Enters the Find in page mode", None, QtGui.QApplication.UnicodeUTF8))
        self.edit_FindAction.setShortcut(QtGui.QApplication.translate("MainWindow", "Ctrl+F", None, QtGui.QApplication.UnicodeUTF8))
        self.file_ExtractCHMAction.setText(QtGui.QApplication.translate("MainWindow", "E&xtract CHM content...", None, QtGui.QApplication.UnicodeUTF8))
        self.file_ExtractCHMAction.setToolTip(QtGui.QApplication.translate("MainWindow", "Extract the CHM content to the directory", None, QtGui.QApplication.UnicodeUTF8))
        self.file_ExtractCHMAction.setWhatsThis(QtGui.QApplication.translate("MainWindow", "Exctracts the CHM archive content to the specified directory. All the files are extracted.", None, QtGui.QApplication.UnicodeUTF8))
        self.settings_SettingsAction.setText(QtGui.QApplication.translate("MainWindow", "&Application settings...", None, QtGui.QApplication.UnicodeUTF8))
        self.settings_SettingsAction.setToolTip(QtGui.QApplication.translate("MainWindow", "Change the application settings", None, QtGui.QApplication.UnicodeUTF8))
        self.settings_SettingsAction.setWhatsThis(QtGui.QApplication.translate("MainWindow", "Change the application settings", None, QtGui.QApplication.UnicodeUTF8))
        self.bookmark_AddAction.setText(QtGui.QApplication.translate("MainWindow", "&Add bookmark", None, QtGui.QApplication.UnicodeUTF8))
        self.bookmark_AddAction.setToolTip(QtGui.QApplication.translate("MainWindow", "Adds a bookmark for currently opened page", None, QtGui.QApplication.UnicodeUTF8))
        self.bookmark_AddAction.setWhatsThis(QtGui.QApplication.translate("MainWindow", "Adds a bookmark for currently opened page. Remembers the opened page, and scroll position. Bookmarks are accessible through Bookmarks menu or tab.", None, QtGui.QApplication.UnicodeUTF8))
        self.bookmark_AddAction.setShortcut(QtGui.QApplication.translate("MainWindow", "Ctrl+B", None, QtGui.QApplication.UnicodeUTF8))
        self.view_Increase_font_size_action.setText(QtGui.QApplication.translate("MainWindow", "&Increase font size", None, QtGui.QApplication.UnicodeUTF8))
        self.view_Increase_font_size_action.setToolTip(QtGui.QApplication.translate("MainWindow", "Increase the font size", None, QtGui.QApplication.UnicodeUTF8))
        self.view_Increase_font_size_action.setWhatsThis(QtGui.QApplication.translate("MainWindow", "Increases the document font size.", None, QtGui.QApplication.UnicodeUTF8))
        self.view_Increase_font_size_action.setShortcut(QtGui.QApplication.translate("MainWindow", "Ctrl++", None, QtGui.QApplication.UnicodeUTF8))
        self.view_Decrease_font_size_action.setText(QtGui.QApplication.translate("MainWindow", "&Decrease font size", None, QtGui.QApplication.UnicodeUTF8))
        self.view_Decrease_font_size_action.setToolTip(QtGui.QApplication.translate("MainWindow", "Decrease the font size", None, QtGui.QApplication.UnicodeUTF8))
        self.view_Decrease_font_size_action.setWhatsThis(QtGui.QApplication.translate("MainWindow", "Decreases the document font size.", None, QtGui.QApplication.UnicodeUTF8))
        self.view_Decrease_font_size_action.setShortcut(QtGui.QApplication.translate("MainWindow", "Ctrl+-", None, QtGui.QApplication.UnicodeUTF8))
        self.view_norm_font_size_action.setText(QtGui.QApplication.translate("MainWindow", "&normal size font", None, QtGui.QApplication.UnicodeUTF8))
        self.view_norm_font_size_action.setToolTip(QtGui.QApplication.translate("MainWindow", "set the font size normal", None, QtGui.QApplication.UnicodeUTF8))
        self.view_norm_font_size_action.setWhatsThis(QtGui.QApplication.translate("MainWindow", "set the document font size normal.", None, QtGui.QApplication.UnicodeUTF8))
        self.view_norm_font_size_action.setShortcut(QtGui.QApplication.translate("MainWindow", "Ctrl+O", None, QtGui.QApplication.UnicodeUTF8))
        self.view_View_HTML_source_action.setText(QtGui.QApplication.translate("MainWindow", "&View HTML source", None, QtGui.QApplication.UnicodeUTF8))
        self.view_View_HTML_source_action.setToolTip(QtGui.QApplication.translate("MainWindow", "View HTML source of current page", None, QtGui.QApplication.UnicodeUTF8))
        self.view_View_HTML_source_action.setWhatsThis(QtGui.QApplication.translate("MainWindow", "Shows the HTML source of currently opened page", None, QtGui.QApplication.UnicodeUTF8))
        self.view_View_HTML_source_action.setShortcut(QtGui.QApplication.translate("MainWindow", "Ctrl+U", None, QtGui.QApplication.UnicodeUTF8))
        self.view_Toggle_fullscreen_action.setText(QtGui.QApplication.translate("MainWindow", "Enable &full screen mode", None, QtGui.QApplication.UnicodeUTF8))
        self.view_Toggle_fullscreen_action.setWhatsThis(QtGui.QApplication.translate("MainWindow", "Enters or leaves the fullscreen mode", None, QtGui.QApplication.UnicodeUTF8))
        self.view_Toggle_fullscreen_action.setShortcut(QtGui.QApplication.translate("MainWindow", "F11", None, QtGui.QApplication.UnicodeUTF8))
        self.view_Toggle_contents_action.setText(QtGui.QApplication.translate("MainWindow", "Enable &side window", None, QtGui.QApplication.UnicodeUTF8))
        self.view_Toggle_contents_action.setWhatsThis(QtGui.QApplication.translate("MainWindow", "Shows or hides the size window (with Content, Index, Search and Bookmark tabs)", None, QtGui.QApplication.UnicodeUTF8))
        self.view_Toggle_contents_action.setShortcut(QtGui.QApplication.translate("MainWindow", "F9", None, QtGui.QApplication.UnicodeUTF8))
        self.view_Locate_in_contents_action.setText(QtGui.QApplication.translate("MainWindow", "&Locate in contents window", None, QtGui.QApplication.UnicodeUTF8))
        self.view_Locate_in_contents_action.setToolTip(QtGui.QApplication.translate("MainWindow", "Locate the current page in contents window", None, QtGui.QApplication.UnicodeUTF8))
        self.view_Locate_in_contents_action.setWhatsThis(QtGui.QApplication.translate("MainWindow", "If the current page is present in the Table of Contents, locate it there. ", None, QtGui.QApplication.UnicodeUTF8))
        self.view_Locate_in_contents_action.setShortcut(QtGui.QApplication.translate("MainWindow", "Ctrl+", None, QtGui.QApplication.UnicodeUTF8))
        self.view_Set_encoding_action.setText(QtGui.QApplication.translate("MainWindow", "Set &encoding", None, QtGui.QApplication.UnicodeUTF8))
        self.view_Set_encoding_action.setWhatsThis(QtGui.QApplication.translate("MainWindow", "Changes the current document encoding. ", None, QtGui.QApplication.UnicodeUTF8))
        self.file_Open_action.setText(QtGui.QApplication.translate("MainWindow", "&Open...", None, QtGui.QApplication.UnicodeUTF8))
        self.file_Open_action.setToolTip(QtGui.QApplication.translate("MainWindow", "Open a CHM file", None, QtGui.QApplication.UnicodeUTF8))
        self.file_Open_action.setWhatsThis(QtGui.QApplication.translate("MainWindow", "Opens a new CHM file", None, QtGui.QApplication.UnicodeUTF8))
        self.nav_actionBack.setText(QtGui.QApplication.translate("MainWindow", "Back", None, QtGui.QApplication.UnicodeUTF8))
        self.nav_actionBack.setToolTip(QtGui.QApplication.translate("MainWindow", "Navigate back", None, QtGui.QApplication.UnicodeUTF8))
        self.nav_actionBack.setWhatsThis(QtGui.QApplication.translate("MainWindow", "Navigate back in navigation history", None, QtGui.QApplication.UnicodeUTF8))
        self.nav_actionForward.setText(QtGui.QApplication.translate("MainWindow", "Forward", None, QtGui.QApplication.UnicodeUTF8))
        self.nav_actionForward.setToolTip(QtGui.QApplication.translate("MainWindow", "Navigate forward", None, QtGui.QApplication.UnicodeUTF8))
        self.nav_actionForward.setWhatsThis(QtGui.QApplication.translate("MainWindow", "Navigate forward in navigation history", None, QtGui.QApplication.UnicodeUTF8))
        self.nav_actionHome.setText(QtGui.QApplication.translate("MainWindow", "Home", None, QtGui.QApplication.UnicodeUTF8))
        self.nav_actionHome.setToolTip(QtGui.QApplication.translate("MainWindow", "Navigate home", None, QtGui.QApplication.UnicodeUTF8))
        self.nav_actionHome.setWhatsThis(QtGui.QApplication.translate("MainWindow", "Navigate to the document Home page, as specified in the document.", None, QtGui.QApplication.UnicodeUTF8))
        self.actionAbout.setText(QtGui.QApplication.translate("MainWindow", "about", None, QtGui.QApplication.UnicodeUTF8))

from pychmtabs import PyChmTabs
import images_rc

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    MainWindow = QtGui.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

