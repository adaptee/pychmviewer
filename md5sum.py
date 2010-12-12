#!/usr/bin/python
# coding: utf8
#########################################################################
# Author: Xinyu.Xiang(John)
# email: zorrohunter@gmail.com
# Created Time: 2009年05月31日 星期日 02时49分00秒
# File Name: md5sum.py
# Description:
#########################################################################
import io
import sys
import hashlib
from session import system_encoding

def md5sum(filename):
    assert isinstance(filename, unicode)
    filename = filename.encode(system_encoding)
    md5 = hashlib.md5()
    fileobj = io.FileIO(filename,'rb')
    binaries = fileobj.read(51200)
    while binaries != '':
        md5.update(binaries)
        binaries = fileobj.read(8096)
    fileobj.close()
    return md5.hexdigest()

