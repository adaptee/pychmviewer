#!/usr/bin/python
# coding: utf8
#########################################################################
# Author: Xinyu.Xiang(John)
# email: zorrohunter@gmail.com
# Created Time: 2009年05月24日 星期日 21时38分10秒
# File Name: pychmfile.py
# Description:
#########################################################################

import sys
import re
import os.path
from HTMLParser import HTMLParser

from utils import remove_comment

try:
    from pychm.chm import CHMFile
    has_pychm = True
except ImportError :
    from chm.chm import CHMFile
    print ("Can't find pychm.chm.CHMFile, use CHMFile instead")
    has_pychm = False

def normalize_url(url):
    if not url:
        return url

    url = remove_comment(url)

    pattern = re.compile(u"^(\\w+):\\/\\/")
    if pattern.match(url):
        return u''

    if url[0:13].lower() == u"javascript://":
        return u''

    pattern = re.compile(u"^ms-its:(.*)::(.*)$", re.I)
    if pattern.match(url):
        return u''

    if url[0] != u'/':
        url = u'/' + url

    return os.path.normpath(url)


class TableEntry(object):
    def __init__(self):
        '''
        attrs:
        key: the key(unicode) of the entry
        urls: list of tuples, first item of tuple is the name(unicode) of the
              url, second is the url(unicode)
              except!!! when return by search function, it's a list of unicode
        indent: the indent of the entry
        '''
        self.key    = None
        self.urls   = []
        self.indent = 0

class PyChmFile(object):
    def __init__(self):
        self.__chm        = None
        self.__title      = u''
        self.__homeurl    = u''
        self.__content_table = None
        self.__index_table   = None

    def loadFile(self, filename):
        '''
        filename must be unicode
        if success,return True,
        else,return False
        '''
        assert isinstance(filename, unicode)

        if self.__chm:
            self.__chm.CloseCHM()
        else:
            self.__chm = CHMFile()

        if not self.__chm.LoadCHM(filename.encode(sys.getfilesystemencoding())):
            print ("load file failed")
            return False

        self.__title = u''
        self.__content_table = None
        self.__index_table = None
        self.__chm.GetWindowsInfo()
        self.__code = self.__chm.GetLCID()[0]
        self.__homeurl = self.__chm.home.decode(self.__code)
        self.__homeurl = normalize_url(self.__homeurl)

        if self.__code is None or self.__code == '':
            self.__code = "utf-8"

        self.__homeurl = self.__chm.home.decode(self.__code)
        self.__title = self.__chm.title.decode(self.__code)

        return True

    def __getChmEncoding(self):
        return self.__code
    chmencoding = property(__getChmEncoding, None, None, 'encoding from LCID')

    def __getIndexTable(self):
        if self.__index_table :
            return self.__index_table
        #parse indextree
        if self.__chm.index is None:
            self.__index_table = []
            return []
        idxurl = self.__chm.index.decode(self.__code)
        idxctt = self.GetFileAsStrByUrl(idxurl)
        if not idxctt:
            idxctt = self.__chm.GetIndex()
        if idxctt:
            print (self.__code)
            self.__parseIndexTable(idxctt.decode(self.__code, 'ignore'))
        return self.__index_table
    index = property(__getIndexTable, None, None, "parsed indextree, list of TableEntry")

    def __getContentTable(self):
        if self.__content_table :
            return self.__content_table
        # parse topictree
        if self.__chm.topics is None:
            self.__content_table = []
            return []
        tpurl = self.__chm.topics.decode(self.__code)
        tpctt = self.GetFileAsStrByUrl(tpurl)
        if not tpctt:
            tpctt = self.__chm.GetTopicsTree()
        if tpctt:
            self.__parseContentTable(tpctt.decode(self.__code) )
        return self.__content_table
    topic = property(__getContentTable, None, None, "parsed topictree, list of TableEntry")


    def __gettitle(self):
        return self.__title
    Title = property(__gettitle, None, None, "the title of the chm file")

    def __gethomeurl(self):
        return self.__homeurl
    HomeUrl = property(__gethomeurl, None, None, "home url of the chm file")

    def __hascontenttable(self):
        self.__getContentTable()
        return self.__content_table is not None and len(self.__content_table) != 0
    HasTopic = property(__hascontenttable)

    def __hasindextable(self):
        self.__getIndexTable()
        return self.__index_table is not None and len(self.__index_table) != 0
    HasIndex = property(__hasindextable)

    def IsSearchable(self):
        return self.__chm.IsSearchable()

    def Search(self, text, wholewords=0, titleonly=0):
        '''
        Performs full-text search on the archive.
        text:unicode
        The first parameter is the word to look for, the second
        indicates if the search should be for whole words only, and
        the third parameter indicates if the search should be
        restricted to page titles.
        This method will return list of TableEntry,
        item.urls being list of unicode
        '''
        if has_pychm:
            if not self.IsSearchable():
                return None
            assert isinstance(text, unicode)
            text = text.encode('utf-8') ##not sure##############################
            rt = self.__chm.Search(text, wholewords, titleonly)
            srt = []
            for k, vl in rt.iteritems():
                entry = TableEntry()
                entry.key = k.decode(self.__code)
                entry.urls = [v.decode(self.__code) for v in vl]
                srt.append(entry)
            return srt
        else:
            if not self.IsSearchable():
                return None
            assert isinstance(text, unicode)
            text = text.encode('utf-8') ##not sure##############################
            rt = self.__chm.Search(text, wholewords, titleonly)
            srt = []
            for k, v in rt[1].items():
                entry = TableEntry()
                entry.key = k.decode(self.__code)
                entry.urls = [v.decode(self.__code),]
                srt.append(entry)
            return srt

    def CheckUrl(self, url):
        '''
        url: unicode
        check if the url if aviable
        return bool
        '''
        assert isinstance(url, unicode)

        url = normalize_url(url)
        if url == u'':
            return False

        fail, _ = self.__chm.ResolveObject( url.encode('utf-8') )

        return not bool(fail)


    def GetFileAsStrByUrl(self, url):
        '''
        url must be unicode
        return the file content @ url as raw data (not encoded)
        if failed, return None
        '''
        assert isinstance(url, unicode)

        url = normalize_url(url)
        if url == u'':
            return None

        fail, unit_info = self.__chm.ResolveObject( url.encode('utf-8') )
        if fail:
            return None

        length, data = self.__chm.RetrieveObject(unit_info)

        return data[0:length] if length else None

    def __parseContentTable(self, ctt):
        assert isinstance(ctt, unicode)

        parser = TableParser()
        parser.feed(ctt)
        self.__content_table = parser.EntryList

    def __parseIndexTable(self, idx):

        assert isinstance(idx, unicode)

        parser  =  TableParser()
        parser.feed(idx)
        self.__index_table = parser.EntryList

        self.__index_table.sort(key=lambda x:x.key)

class TableParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.entrylist = []
        self.crtentry = None
        self.indent = 0
        self.names = []
        self.locals = []
        self.key = None
        self.root_indent_offset_set = False
        self.root_indent_offset = 0

    def handle_starttag(self, tag, attrs):
        tag = tag.lower().encode('utf-8')
        if hasattr(self, 'start_' + tag):
            getattr(self, 'start_' + tag)(attrs)

    def handle_startendtag(self, tag, attrs):
        tag = tag.lower().encode('utf-8')
        if hasattr(self, 'start_' + tag):
            getattr(self, 'start_' + tag)(attrs)

    def handle_endtag(self, tag):
        tag = tag.lower().encode('utf-8')
        if hasattr(self, 'end_' + tag):
            getattr(self, 'end_' + tag)()


    def __getEntryList(self):
#        self.close()
        return self.entrylist
    EntryList = property(__getEntryList)

    def start_object(self, attrs):
        for k, v in attrs:
            if v.lower() == u'text/sitemap':
                self.crtentry = TableEntry()
                return

    def end_object(self):
        if self.crtentry is None:
            return
        if self.key is not None:
            if not self.root_indent_offset_set:
                self.root_indent_offset_set = True
                self.root_indent_offset = self.indent
            self.crtentry.key = self.key
            if len(self.names) > 0:
                self.crtentry.urls = zip(self.names, self.locals)
            else:
                self.crtentry.urls = zip((self.key,), self.locals)
        elif len(self.names)>0:
            if not self.root_indent_offset_set:
                self.root_indent_offset_set = True
                self.root_indent_offset = self.indent
            self.crtentry.key = self.names[0]
            self.crtentry.urls = zip(self.names, self.locals)
        else:
            #print ("parse error")
            self.crtentry = None
            self.names = []
            self.locals = []
            self.key = None
            return
        self.crtentry.indent = self.indent-self.root_indent_offset
        self.entrylist.append(self.crtentry)
        self.crtentry = None
        self.names = []
        self.locals = []
        self.key = None

    def start_param(self, attrs):
        if self.crtentry is not None:
            isname    = False
            islocal   = False
            iskeyword = False
            for k, v in attrs:
                v = v.lower()
                if v == u'keyword':
                    iskeyword = True
                elif v == u'name':
                    isname = True
                elif v == u'local':
                    islocal = True
            if isname:
                for k, v in attrs:
                    if k.lower() == u'value':
                        self.names.append(v)
            elif islocal:
                for k, v in attrs:
                    if k.lower() == u'value':
                        self.locals.append(v)
            elif iskeyword:
                for k, v in attrs:
                    if k.lower() == u'value':
                        self.key = v

    def start_ul(self, attrs):
        self.indent += 1
        if self.indent > 256:
            print ("something maybe wrong! indent reaches the maxes num")

    def end_ul(self):
        self.indent -= 1
        if self.indent < self.root_indent_offset:
            self.indent = self.root_indent_offset
