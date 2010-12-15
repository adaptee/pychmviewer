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
from argparse import ArgumentParser

from PyQt4 import QtGui

from session import Session
from pychmmainwindow import PyChmMainWindow


if __name__ == "__main__":
    session = Session()

    argparser = ArgumentParser(
                                description= "A CHM reader written in PyQt."
                              )

    argparser.add_argument( "paths",
                             metavar="PATH",
                             nargs='*',
                             help="CHM File to open."
                          )

    args = argparser.parse_args()
    paths = [ unicode( os.path.realpath(path), session.system_encoding )
              for path in args.paths
            ]

    app = QtGui.QApplication(sys.argv)
    mainwindow = PyChmMainWindow(session, paths)
    mainwindow.show()
    sys.exit(app.exec_())
