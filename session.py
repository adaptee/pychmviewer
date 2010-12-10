#!/usr/bin/env python
# vim: set fileencoding=utf-8 :

import os
import locale

from option import PyChmViewerConfig

_, system_encoding = locale.getdefaultlocale()


def Session(object):
    def __init__(self):
        self.config_dir = os.path.join( os.environ["HOME"], ".pychmviewer")
        self.config_filename = os.path.join(self.config_dir, "pychmviewer.cfg")
        self.config = PyChmviewerConfig(self.config_filename)
        self.system_encoding = locale.getdefaultlocale()[1]



