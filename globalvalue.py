#!/usr/bin/python
# coding: utf8
#########################################################################
# Author: Xinyu.Xiang(John)
# email: zorrohunter@gmail.com
# Created Time: 2009年05月26日 星期二 03时01分09秒
# File Name: global.py
# Description:
#########################################################################

#from config import GlobalConfig
from options import PyChmViewerConfig as GlobalConfig
globalcfg = GlobalConfig()

chmFile        = None
chmpath        = None
encoding       = "gb18030"
mainWindow     = None
currentwebview = None
tabs           = None

