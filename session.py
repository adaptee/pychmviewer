#!/usr/bin/env python
# vim: set fileencoding=utf-8 :

import os
import locale
import bsddb

from option import PyChmViewerConfig

organization       = u"PyChmViewer"
application        = u"PyChmViewer"
description        = u"A CHM reader written in PyQt"
version            = u"0.1.1"
license            = u"GPLv2"
homepage           = u"http://www.github.com/adaptee/pychmviewer"

authors = [
             (u"Xiuyu"    , u"someone@gmail.com", "2009 - 2009"),
             (u"Jekyll Wu", u"Adaptee@gmail.com", "2010 - "),
          ]


class Session(object):
    def __init__(self):
        self.config_dir      = self._getConfigDir()
        self.config          = self._getConfig()
        self.snapshot        = self._getSnapshot()
        self.system_encoding = locale.getdefaultlocale()[1]

        self.organization    = organization
        self.application     = application
        self.description     = description
        self.version         = version
        self.license         = license
        self.authors         = authors
        self.homepage        = homepage

    def _getConfigDir(self):
        config_dir = os.path.join( os.environ["HOME"], ".pychmviewer")

        if not os.path.exists(config_dir):
            os.mkdir(config_dir)

        return config_dir

    def _getConfig(self):
        config_path = os.path.join(self.config_dir, "pychmviewer.cfg" )

        return PyChmViewerConfig(config_path)

    def _getSnapshot(self):
        snapshot_path = os.path.join( self.config_dir, "snapshot.db" )

        try:
            return bsddb.hashopen(snapshot_path)
        except bsddb.db.DBNoSuchFileError:
            # a dummy database
            return { }

