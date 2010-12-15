#!/usr/bin/env python
# vim: set fileencoding=utf-8 :


import os
from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import QString, QStringList

class RecentFiles():

    def __init__(self, maxsize=10):
        self.maxsize = maxsize
        self.recentfiles = [ ]

    def addToRecentFiles(self, path):
        self._assert()
        # remove outdated entry
        if path in self.recentfiles :
            self.recentfiles.remove(path)

        self.recentfiles.insert(0, path)
        # simple and clear way to respect 'maxsize'
        self.recentfiles = self.recentfiles[0:self.maxsize]

    def delFromRecentsFiles(self, path):
        self._assert()
        if path in self.recentfiles:
            self.recentfiles.remove(path)


    def clearRecentFiles(self):
        self.recentfiles = [ ]

    def saveRecentFiles(self):
        raise NotImplementedError("")

    def loadRecentFiles(self):
        raise NotImplementedError("")

    def _assert(self):
        # should never contain duplication!
        def duplicated(iterable):
            return len(iterable) != len( list(set(iterable) ) )

        assert not duplicated(self.recentfiles), \
               "[Logic Error] duplication exist!"

class QtRecentFiles(QtCore.QObject, RecentFiles, ):
    key = "recents/recents"

    def __init__(self, maxsize, parent=None):
        QtCore.QObject.__init__(self, parent)
        RecentFiles.__init__(self, maxsize)
        self.actions = [ ]
        self.loadRecentFiles()
        self.updateActions()

    def onFileOpened(self, path):
        self.addToRecentFiles(path)
        self.updateActions()

    def onFileNotOpened(self, path):
        self.delFromRecentsFiles(path)
        self.updateActions()

    def onClearRecentFiles(self):
        self.clearRecentFiles()
        self.updateActions()

    def _createAction(self, pair):
        index, path = pair

        text   = u"&%s. %s" % ( index + 1, os.path.basename(path) )

        action = QtGui.QAction(self)
        action.setText(text)
        #action.setData(path)
        action.path = path

        self.connect(action,
                     QtCore.SIGNAL('triggered(bool)'),
                     self.openRecentFile
                    )

        return action

    def openRecentFile(self):
        action = self.sender()
        if action:
            path = action.path
            self.emit(QtCore.SIGNAL('openRecentFile'), path)

    def updateActions(self):
        self._assert()

        self.actions = map( self._createAction, enumerate(self.recentfiles) )
        self.emit(QtCore.SIGNAL('recentFilesUpdated'), True)

    def saveRecentFiles(self):
        self._assert()

        recentfiles = QStringList()
        for path in self.recentfiles:
            recentfiles.append( QString(path) )

        settings = QtCore.QSettings()
        settings.setValue(self.key, recentfiles)

    def loadRecentFiles(self):
        settings = QtCore.QSettings()
        paths = settings.value(self.key).toStringList()

        self.recentfiles = [ ]
        for path in paths:
            self.recentfiles.append( unicode(path) )
