#!/usr/bin/python
# coding: utf8
#########################################################################
# Author: Xinyu.Xiang(John)
# email: zorrohunter@gmail.com
# Created Time: 2009年06月01日 星期一 16时43分26秒
# File Name: pychmviewer.py
# Description:
#########################################################################

import os
import sys

from PyQt4 import QtGui

import globalvalue
from pychmfile import PyChmFile
from pychmmainwindow import PyChmMainWindow

if __name__ == "__main__":

    filesystem_encoding = sys.getfilesystemencoding()

    ok = False
    app = QtGui.QApplication(sys.argv)

    if len(sys.argv)>=2:
        globalvalue.chmpath = os.path.abspath(sys.argv[1].decode(filesystem_encoding))
        globalvalue.chmFile = PyChmFile()
        ok = globalvalue.chmFile.loadFile(globalvalue.chmpath)

    if not ok:
        if globalvalue.chmpath :
            print (u"Failed open chm file: %s" % globalvalue.chmpath )

        choice = QtGui.QFileDialog.getOpenFileName(
                                                None,
                                                u'choose file',
                                                globalvalue.globalcfg.lastdir,
                                                u'CHM files (*.chm *.CHM)',
                                                   )
        globalvalue.chmpath = os.path.abspath(unicode(choice))
        globalvalue.chmFile = PyChmFile()

        ok = globalvalue.chmFile.loadFile(globalvalue.chmpath)
        if not ok:
            sys.exit(1)

    mainwin = PyChmMainWindow()
    mainwin.show()
    sys.exit(app.exec_())
