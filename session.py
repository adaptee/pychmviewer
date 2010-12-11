#!/usr/bin/env python
# vim: set fileencoding=utf-8 :

import os
import locale
import bsddb

from option import PyChmViewerConfig

_, system_encoding = locale.getdefaultlocale()


class Session(object):
    def __init__(self, config_path=None):
        self.config_dir      = os.path.join( os.environ["HOME"], ".pychmviewer")
        self.config          = self._getConfig(config_path)
        self.snapshot        = self._getSnapshot()
        self.system_encoding = locale.getdefaultlocale()[1]

    def _getConfig(self, config_path=None):
        config_path = config_path or \
                      os.path.join(self.config_dir, "pychmviewer.cfg" )
        return PyChmViewerConfig(config_path)

    def _getSnapshot(self):
        path = os.path.join(  self.config_dir, "snapshot.db" )
        return bsddb.hashopen(path)




