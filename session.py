#!/usr/bin/env python
# vim: set fileencoding=utf-8 :

import os
import locale

from option import PyChmViewerConfig

_, system_encoding = locale.getdefaultlocale()


class Session(object):
    def __init__(self, config_path=None):
        self.config_dir = os.path.join( os.environ["HOME"], ".pychmviewer")

        config_path = config_path or \
                      os.path.join(self.config_dir, "pychmviewer.cfg" )

        self.config = PyChmViewerConfig(config_path)

        self.system_encoding = locale.getdefaultlocale()[1]



