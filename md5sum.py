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
import string

def md5sum(filename):
    assert isinstance(filename,unicode)
    filename=filename.encode(sys.getfilesystemencoding())
    m=hashlib.md5()
    file=io.FileIO(filename,'rb')
    bytes=file.read(51200)
    while bytes!='':
        m.update(bytes)
        bytes=file.read(8096)
    file.close()
    return m.hexdigest()

if __name__=='__main__':
    print md5sum(sys.argv[1].decode(sys.getfilesystemencoding()))
