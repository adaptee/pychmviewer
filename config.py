#!/usr/bin/python
# coding: utf8
#########################################################################
# Author: Xinyu.Xiang(John)
# email: zorrohunter@gmail.com
# Created Time: 2009年05月31日 星期日 03时15分44秒
# File Name: config.py
# Description: 
#########################################################################
from md5sum import md5sum
import sys
import os
import exceptions
import bsddb
from ConfigParser import ConfigParser
home=os.environ['HOME']
cfghome=os.path.join(home,'.pychmviewer')
globalcfgfile=os.path.join(cfghome,'config.cfg')
encoding=sys.getfilesystemencoding()
class GlobalConfig(object):
    def __getlastdir(self):
        return self.__lastdir.decode(encoding)
    def __setlastdir(self,v):
        assert isinstance(v,unicode)
        self.__lastdir=v.encode(encoding)
    lastdir=property(__getlastdir,__setlastdir)

    def __init__(self):
        cfg=ConfigParser()
        try:
            cfg.read(globalcfgfile)
        except:
            pass
        if not cfg.has_section('userconfig'):
            self.loadlasttime=True
            self.openremote=True
            self.fontfamily=None
            self.fontsize=None
            self.__lastdir=home

        try:
            self.loadlasttime=cfg.getboolean('userconfig','loadlasttime')
        except:
            self.lastlasttime=True
        try:
            self.openremote=cfg.getboolean('userconfig','openremote')
        except:
            self.openremote=True
        try:
            self.fontfamily=cfg.get('userconfig','fontfamily').decode('utf-8')
            if self.fontfamily=='default':
                self.fontfamily=None
        except:
            self.fontfamily=None
        try:
            self.fontsize=cfg.getint('userconfig','fontsize')
        except:
            self.fontsize=None
        try:
            self.__lastdir=cfg.get('userconfig','lastdir')
        except:
            self.__lastdir=home

    def savecfg(self):
        cfg=ConfigParser()
        cfg.add_section('userconfig')
        cfg.set('userconfig','loadlasttime',str(self.loadlasttime))
        cfg.set('userconfig','openremote',str(self.openremote))
        if self.fontfamily:
            cfg.set('userconfig','fontfamily',self.fontfamily.encode('utf-8'))
        if self.fontsize:
            cfg.set('userconfig','fontsize',str(self.fontsize))
        cfg.set('userconfig','lastdir',self.__lastdir)
        try:
            os.mkdir(cfghome,0700)
        except exceptions.OSError:
            pass
        f=open(globalcfgfile,'wb')
        cfg.write(f)
        f.flush()
        f.close()
        

class PyChmConfig(object):
    def __init__(self,chmpath):
        assert isinstance(chmpath,unicode)
        self.md5=md5sum(chmpath)
        self.cfghome=os.path.join(home,'.pychmviewer')
        try:
            os.mkdir(self.cfghome,0700)
        except exceptions.OSError:
            pass
        self.cfghome=os.path.join(self.cfghome,self.md5)
        try:
            os.mkdir(self.cfghome,0700)
        except exceptions.OSError:
            pass
        bookmarkpath=os.path.join(self.cfghome,'bookmark.db')
        lastconfpath=os.path.join(self.cfghome,'last.db')
        self.bookmarkdb=bsddb.hashopen(bookmarkpath)
        self.lastconfdb=bsddb.hashopen(lastconfpath)
