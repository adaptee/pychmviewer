#!/usr/bin/python
# coding: utf8
#########################################################################
# Author: Xinyu.Xiang(John)
# email: zorrohunter@gmail.com
# Created Time: 2009年05月26日 星期二 03时15分00秒
# File Name: urltools.py
# Description:
#########################################################################
import re

def parseChmURL(url):
    '''
    url:unicode
    return: tuple(bool,unicode,unicode)
            first item tell if it's a url pointing to another .CHM
            second item is chm file,
            third item is page.
    '''
    assert isinstance(url, unicode)

    # [scheme]  ms-its:[chmpath]::[pagepath]
    pattern = re.compile(u'^ms-its:(.*)::(.*)$', re.I)
    match = pattern.search(url)
    if match:
        newchmfile = match.group(1)
        page = match.group(2)
        return (True, newchmfile, page)
    return (False, None, None)
