#!/usr/bin/env python
# vim: set fileencoding=utf-8 :



from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import QString

# only responbile for data
class RecentFiles(object):
    key = "recents/recents"

    def __init__(self, max=10):
        self.max = max
        # newest one comes last
        self.recents = [ ]

    def addToRecentFiles(self, path):
        if path in self.recents:
            self.recents.remove(path)

        self.recents.append(path)

    def delFromRecentsFiles(self, path):
        try:
            self.recents.remove(path)
        except ValueError :
            pass

    def clearRecentFiles(self):
        self.recents = [ ]

    def saveRecentFiles(self):
        raise NotImplementedError("")

    def loadRecentFiles(self):
        raise NotImplementedError("")

    def _assert(self):
        # should never contain duplication!
        def hasDuplications(l):
            return len(l) != len( list(set(l) ) )

        assert not hasDuplications(self.recents), \
               "[Logic Error] duplication exist!"

# responsible for interactive with others
class QtRecentFiles(RecentFiles, QtCore.QObject):
    def __init(self, max, parent=None):
        RecentFiles.__init(self, max)
        self.actions = [ ]

    def onFileOpened(self, path):
        self.addToRecentFiles(path)
        self.updateActions()

    def onFileNotOpened(self, path):
        self.delFromRecentsFiles(path)
        self.updateActions()

    def onClearRecentFiles(self):
        self.clearRecentFiles()
        self.updateActions()

    def updateActions(self):

        def createAction(index, path):
            action = QtGui.QAction(self)

            text = QString( u"&%s.%s" % ( index + 1, os.path.basename(path) ) )
            path = QString( path)
            action.setText(text)
            action.setToolTip(path )
            action.setData(path)

            self.connect(action,
                         QtCore.SIGNAL('triggered(bool)'),
                         self.openRecentFile)

            return action

        self._assert()
        self.actions = map(createAction, enumerate(self.recents) )

    def openRecentFile():
        action = self.sender()
        if action:
            path = action.data()
            self.emit(QtCore.SIGNAL('openRecentFile(QString)'), path)


    def saveRecentFiles(self):
        self._assert()
        settings = QtCore.QSettings()
        settings.setValue(key, self.recents)

    def loadRecentFiles(self):
        self._assert()
        settings = QtCore.QSettings()
        return settings.value(key).toStringList()






