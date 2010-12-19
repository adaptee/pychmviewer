#!/usr/bin/env python
# vim: set fileencoding=utf-8 :

" Provides a central place for obtaining common info."

import os
import locale
import bsddb

import xdg.BaseDirectory
from PyQt4 import QtCore

from config import PyChmViewerConfig




class Session(object):
    " A central place with common info across whole app."

    organization       = u"PyChmViewer"
    application        = u"PyChmViewer"
    description        = u"A CHM reader written in PyQt"
    version            = u"0.1.2"
    license            = u"GPLv2"
    homepage           = u"http://www.github.com/adaptee/pychmviewer"

    authors = [
                (u"Xinyu.Xiang(John)", u"zorrohunter@gmail.com", "2009 - 2009"),
                (u"Jekyll Wu"        , u"adaptee@gmail.com"    , "2010 - ")    ,
              ]

    def __init__(self):

        self.config_dir      = self._getConfigDir()
        self.config          = self._getConfig()
        self.snapshot        = self._getSnapshot()
        self.system_encoding = locale.getdefaultlocale()[1]

        QtCore.QCoreApplication.setOrganizationName(self.organization)
        QtCore.QCoreApplication.setApplicationName(self.application)
        self.qsettings = QtCore.QSettings()

    def _getConfigDir(self):
        " Get the location of config dir"
        config_dir = os.path.join( xdg.BaseDirectory.xdg_config_home,
                                   self.application)

        if not os.path.exists(config_dir):
            os.mkdir(config_dir)

        return config_dir

    def _getConfig(self):
        " Get the config object."
        config_path = os.path.join(self.config_dir, "pychmviewer.cfg" )

        return PyChmViewerConfig(config_path)

    def _getSnapshot(self):
        " Get the snapshot of last session."
        snapshot_path = os.path.join( self.config_dir, "snapshot.db" )

        try:
            return bsddb.hashopen(snapshot_path)
        except bsddb.db.DBNoSuchFileError:
            # a dummy database
            return { }

