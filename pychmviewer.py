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

from session import Session

from utils import getchmfile, setchmfile, getcfg
from pychmfile import PyChmFile
from pychmmainwindow import PyChmMainWindow
from session import system_encoding

if __name__ == "__main__":

    app = QtGui.QApplication(sys.argv)

    chmfile = PyChmFile()
    path = ""
    ok = False

    if len(sys.argv) >= 2:
        path = os.path.realpath(sys.argv[1].decode(system_encoding))
        ok = chmfile.loadFile(path)
        setchmfile(chmfile)

    if not ok:
        if path :
            print (u"Failed open chm file: %s" % path )

        path = QtGui.QFileDialog.getOpenFileName(
                                                None,
                                                u'choose file',
                                                getcfg().lastdir,
                                                u'CHM files (*.chm *.CHM)',
                                                   )

        ok = chmfile.loadFile(unicode(path))
        if not ok:
            sys.exit(1)

        setchmfile( chmfile )

    # experimental
    session = Session()

    mainwin = PyChmMainWindow(session)
    mainwin.show()

    sys.exit(app.exec_())
