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
from utils import getchmfile, setchmfile, getchmpath, setchmpath, getcfg
from pychmfile import PyChmFile
from pychmmainwindow import PyChmMainWindow
from session import system_encoding

if __name__ == "__main__":

    ok = False
    app = QtGui.QApplication(sys.argv)

    if len(sys.argv)>=2:
        setchmpath( os.path.abspath(sys.argv[1].decode(system_encoding)) )
        setchmfile( PyChmFile() )
        ok = getchmfile().loadFile(getchmpath())

    if not ok:
        chmpath = getchmpath()
        if chmpath :
            print (u"Failed open chm file: %s" % chmpath )

        choice = QtGui.QFileDialog.getOpenFileName(
                                                None,
                                                u'choose file',
                                                getcfg().lastdir,
                                                u'CHM files (*.chm *.CHM)',
                                                   )
        setchmpath( os.path.abspath(unicode(choice)) )
        setchmfile( PyChmFile() )

        ok = getchmfile().loadFile(getchmpath())
        if not ok:
            sys.exit(1)

    mainwin = PyChmMainWindow()
    mainwin.show()
    sys.exit(app.exec_())
