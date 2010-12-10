#!/usr/bin/env python
# vim: set fileencoding=utf-8 :

import locale

_, system_encoding = locale.getdefaultlocale()


def Session(object):
    def __init__(self, config):
        self.config = config
