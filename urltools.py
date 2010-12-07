#!/usr/bin/python
# coding: utf8
#########################################################################
# Author: Xinyu.Xiang(John)
# email: zorrohunter@gmail.com
# Created Time: 2009年05月26日 星期二 03时15分00秒
# File Name: urltools.py
# Description:
#########################################################################
import os.path
import re

def isRemoteURL(url):
    '''
    check if url is a remote url
    url: unicode
    return : tuple, first is bool to tell if it's remote
             second is remote protocol(unicode)
    '''
    assert isinstance(url, unicode)

    if url.lower().startswith(u"mailto"):
        protocol = u'mailto'
        return (True, protocol)

    pattern = re.compile(u"^(\\w+):\\/\\/", re.I)
    match = pattern.search(url)

    if match:
        proto = match.group(1).lower()
	if proto in ( u"http", u"ftp", u"news", ) :
            return (True, proto)

    return (False, u'')


def isjsurl(url):
    '''
    check if url is a js url
    url: unicode
    '''
    assert isinstance(url, unicode)

    url = url.lower()
    return url.startswith(u"javascript://")

def isnewchmurl(url):
    '''
    url:unicode
    return: tuple(bool,unicode,unicode)
            first item tell if it's newchmurl,
            second item is chm file,
            third item is page.
    '''
    assert isinstance(url, unicode)

    pattern = re.compile(u'^ms-its:(.*)::(.*)$', re.I)
    match = pattern.search(url)
    if match:
        chmfile = match.group(1)
        page = match.group(2)
        return (True, chmfile, page)
    return (False, None, None)

def getaburlifneed(url):
    '''
    url:unicode
    return: unicode. if need(not romote,js,newchm url),return
            a clean absolute url;else, return url passed in.
    '''
    assert isinstance(url, unicode)

    if ( not isRemoteURL(url)[0] ) and ( not isjsurl(url) )  and ( not isnewchmurl(url)[0] ):
        url = os.path.normpath(url)
        if url[0] != u'/':
            url = u'/' + url
    return url

