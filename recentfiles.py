#!/usr/bin/env python
# vim: set fileencoding=utf-8 :

" Provides the facility of 'Recent Files'. "

import os

from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import QString, QStringList

class RecentFiles():
    " Implement the logic of adding/removing entry. "
    def __init__(self, maxsize=10):
        self.maxsize = maxsize
        self.recentfiles = [ ]

    def addToRecentFiles(self, path):
        " Add entry. "
        self._assert()
        # remove outdated entry
        if path in self.recentfiles :
            self.recentfiles.remove(path)

        self.recentfiles.insert(0, path)

        # respect 'maxsize'
        self.recentfiles = self.recentfiles[0:self.maxsize]

    def delFromRecentsFiles(self, path):
        " remove entry. "
        self._assert()
        if path in self.recentfiles:
            self.recentfiles.remove(path)

    def clearRecentFiles(self):
        " clear entry. "
        self.recentfiles = [ ]

    def saveRecentFiles(self):
        " searilize the list  into external storage."
        raise NotImplementedError("")

    def loadRecentFiles(self):
        " restore the list from external storage. "
        raise NotImplementedError("")

    def _assert(self):
        " Make sure the logic is right. "
        # should never contain duplication!
        def unique(iterable):
            return len(iterable) == len( set(iterable) )

        assert unique(self.recentfiles), "[Logic Error] duplication exist!"

class QRecentFiles(QtCore.QObject, RecentFiles ):
    " Implements the facility of 'Reent Files' as an reusable QObject"

    key = "recents/recents"

    def __init__(self, maxsize, qsettings, parent=None):
        QtCore.QObject.__init__(self, parent)
        RecentFiles.__init__(self, maxsize)

        self.actions = [ ]
        self.qsettings = qsettings

        self.loadRecentFiles()
        self.updateActions()

    def onFileOpened(self, path):
        " Add file into the list. "
        self.addToRecentFiles(path)
        self.updateActions()

    def onFileNotOpened(self, path):
        " Remove file from the list( if contained). "
        self.delFromRecentsFiles(path)
        self.updateActions()

    def onClearRecentFiles(self):
        " Clear the list ."
        self.clearRecentFiles()
        self.updateActions()

    def _createAction(self, pair):
        " Helper function to create QAction."
        index, path = pair

        text   = u"&%s. %s" % ( index + 1, os.path.basename(path) )

        action = QtGui.QAction(self)
        action.setText(text)
        action.path = path

        self.connect(action,
                     QtCore.SIGNAL('triggered(bool)'),
                     self.openRecentFile
                    )

        return action

    def openRecentFile(self):
        " Slot for opening one item in the list of 'Recent Files' "
        action = self.sender()
        if action:
            path = action.path
            self.emit(QtCore.SIGNAL('openRecentFile'), path)

    def updateActions(self):
        " Update the actions corrsponding recent files. "
        self._assert()

        self.actions = map (self._createAction, enumerate(self.recentfiles) )
        self.emit(QtCore.SIGNAL('recentFilesUpdated'), True)

    def saveRecentFiles(self):
        self._assert()

        recentfiles = QStringList()
        for path in self.recentfiles:
            recentfiles.append( QString(path) )

        self.qsettings.setValue(self.key, recentfiles)

    def loadRecentFiles(self):
        paths = self.qsettings.value(self.key).toStringList()

        self.recentfiles = [ ]
        for path in paths:
            self.recentfiles.append( unicode(path) )

        self._assert()
