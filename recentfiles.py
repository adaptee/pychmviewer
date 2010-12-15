#!/usr/bin/env python
# vim: set fileencoding=utf-8 :


import os
from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import QString, QStringList

# only responbile for data
class RecentFiles():

    def __init__(self, maxlen=10):
        #TODO; implement the maxlen feature
        self.maxlen = maxlen
        self.recentfiles = [ ]
        self.hasChanged = False


    def addToRecentFiles(self, path):
        self._assert()
        if  path == self.recentfiles[0]:
            # if already the latest, do nothing
            self.hasChanged = False
        else:
            if path in self.recentfiles :
                self.recentfiles.remove(path)
            self.recentfiles.insert(0, path)
            self.hasChanged = True

    def delFromRecentsFiles(self, path):
        self._assert()

        if path in self.recentfiles:
            self.recentfiles.remove(path)
            self.hasChanged = True
        else:
            self.hasChanged = False

    def clearRecentFiles(self):
        self.recentfiles = [ ]
        self.hasChanged = True

    def saveRecentFiles(self):
        raise NotImplementedError("")

    def loadRecentFiles(self):
        raise NotImplementedError("")

    def _assert(self):
        # should never contain duplication!
        def duplicated(paths):
            return len(paths) != len( list(set(paths) ) )

        assert not duplicated(self.recentfiles), \
               "[Logic Error] duplication exist!"


# responsible for interactive with others
class QtRecentFiles(QtCore.QObject, RecentFiles, ):
    key = "recents/recents"

    def __init__(self, maxlen, parent=None):
        QtCore.QObject.__init__(self, parent)
        RecentFiles.__init__(self, maxlen)
        self.actions = [ ]
        self.loadRecentFiles()
        self.updateActions()

    def onFileOpened(self, path):
        #print "[onFileOpend] %s" % path
        self.addToRecentFiles(path)
        self.updateActions()

    def onFileNotOpened(self, path):
        self.delFromRecentsFiles(path)
        self.updateActions()

    def onClearRecentFiles(self):
        self.clearRecentFiles()
        self.updateActions()

    def createAction(self, pair):
        index  = pair[0]
        path   = pair[1]

        text   = QString( u"&%s. %s" % ( index + 1, os.path.basename(path) ) )
        path   = QString( path)

        action = QtGui.QAction(self)
        action.setText(text)
        action.setToolTip(path )
        action.setData(path)

        self.connect(action,
                     QtCore.SIGNAL('triggered(bool)'),
                     self.openRecentFile
                    )

        return action

    def updateActions(self):
        self._assert()

        if self.hasChanged:

            self.actions = map( self.createAction, enumerate(self.recentfiles) )

            for action in self.actions:
                self.connect(action,
                             QtCore.SIGNAL('triggered(bool)'),
                             self.openRecentFile
                            )

            self.emit(QtCore.SIGNAL('recentFilesUpdated'), True)

            self.hasChanged = False


    def openRecentFile(self):
        action = self.sender()
        if action:
            path = action.data()
            self.emit(QtCore.SIGNAL('openRecentFile'), path)


    def saveRecentFiles(self):
        self._assert()
        settings = QtCore.QSettings()

        recentfiles = QStringList()
        for path in self.recentfiles:
            recentfiles.append( QString(path) )

        settings.setValue(self.key, recentfiles)

    def loadRecentFiles(self):
        settings = QtCore.QSettings()

        paths = settings.value(self.key).toStringList()
        recentfiles = [ ]
        for path in paths:
            recentfiles.append( unicode(path) )

        self.recentfiles = recentfiles
        self.hasChanged  = True
