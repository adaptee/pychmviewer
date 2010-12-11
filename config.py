#!/usr/bin/python
# coding: utf8
#########################################################################
# Author: Xinyu.Xiang(John)
# email: zorrohunter@gmail.com
# Created Time: 2009年05月31日 星期日 03时15分44秒
# File Name: config.py
# Description:
#########################################################################
import os
#FIXME; this module is deprecated and marked to be removal in future
import bsddb

from md5sum import md5sum

home          = os.environ['HOME']
cfghome       = os.path.join(home, '.pychmviewer')


class PyChmConfig(object):
    def __init__(self, chmpath):
        assert isinstance(chmpath, unicode)

        self.md5 = md5sum(chmpath)
        self.cfghome = cfghome

        if not os.path.exists(cfghome):
            try:
                os.mkdir(self.cfghome, 0755)
            except OSError:
                pass

        self.cfghome = os.path.join(self.cfghome, self.md5)

        try:
            os.mkdir(self.cfghome, 0755)
        except OSError:
            pass

        lastconfpath = os.path.join(self.cfghome, 'last.db')
        self.lastconfdb = bsddb.hashopen(lastconfpath)
