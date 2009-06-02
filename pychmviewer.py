#!/usr/bin/python
# coding: utf8
#########################################################################
# Author: Xinyu.Xiang(John)
# email: zorrohunter@gmail.com
# Created Time: 2009年06月01日 星期一 16时43分26秒
# File Name: pychmviewer.py
# Description: 
#########################################################################

import sys,os
import globalvalue 
from pychmfile import PyChmFile
from PyQt4 import QtCore, QtGui
from pychmmainwindow import PyChmMainWindow
from PyQt4.QtGui import QPixmap,QSplashScreen

ok=False
app = QtGui.QApplication(sys.argv)
if len(sys.argv)>=2:
    globalvalue.chmpath=os.path.abspath(sys.argv[1].decode(sys.getfilesystemencoding()))
    globalvalue.chmFile=PyChmFile()
    ok=globalvalue.chmFile.loadFile(globalvalue.chmpath)
if not ok:
    if globalvalue.chmpath!=None:
        print 'open chm file',globalvalue.chmpath,'failed'
    file=QtGui.QFileDialog.getOpenFileName(None, u'choose file',globalvalue.globalcfg.lastdir,
            u'CHM files (*.chm)')
    globalvalue.chmpath=os.path.abspath(unicode(file))
    globalvalue.chmFile=PyChmFile()
    ok=globalvalue.chmFile.loadFile(globalvalue.chmpath)
    if not ok:
        sys.exit(0)
pixmap=QPixmap(os.path.join(sys.path[0],'splash.png'))
splash=QSplashScreen(pixmap)
splash.show()
mw=PyChmMainWindow()
mw.show()
splash.finish(mw)
sys.exit(app.exec_())
