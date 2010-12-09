#!/usr/bin/python
# coding: utf8
#########################################################################
# Author: Xinyu.Xiang(John)
# email: zorrohunter@gmail.com
# Created Time: 2009年06月03日 星期三 02时44分43秒
# File Name: extract_chm.py
# Description:
#########################################################################

from chm import chmlib

from session import system_encoding

def callback(cf, ui, paths):
    '''
    innermethod
    '''
    paths.append(ui.path)
    return chmlib.CHM_ENUMERATOR_CONTINUE

def getfilelist(chmpath):
    '''
    get filelist of the given path chm file
    return (bool,fileurllist)
    '''
    assert isinstance(chmpath, unicode)

    chmfile = chmlib.chm_open( chmpath.encode(system_encoding) )

    paths = []
    ok = chmlib.chm_enumerate(chmfile, chmlib.CHM_ENUMERATE_ALL, callback, paths)
    chmlib.chm_close(chmfile)

    return (ok, paths)
