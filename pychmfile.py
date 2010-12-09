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
from chm.chm import CHMFile
from HTMLParser import HTMLParser

from utils import remove_comment

# TODO: provide real implementation
def codepage2encoding(codepage):
    return codepage

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
        indent: the indent of the entry
        '''
        self.key    = None
        self.urls   = []
        self.indent = 0

class PyChmFile(object):
    def __init__(self):
        self.initialize()

    def initialize(self):
        self._chm           = CHMFile()
        self._title         = u""
        self._homeurl       = u""
        self._encoding      = u""
        self._content_table = [ ]
        self._index_table   = [ ]

    def reset(self):
        self._chm.CloseCHM()
        self.initialize()

    def loadFile(self, filename):
        '''
        filename must be unicode
        if success,return True,
        else,return False
        '''
        #self._chm.GetTopicsTree()
        #self._chm.GetIndex()
        #self._chm.filename

        #self._chm.GetEncoding()  (not working)
        #self._chm.lcid    (magic number)

        #self._chm.index   (url only)
        #self._chm.topics  (url only)

        assert isinstance(filename, unicode)
        self.reset()

        if not self._chm.LoadCHM(filename.encode(sys.getfilesystemencoding())):
            print ("load file failed")
            return False

        chm = self._chm

        codepage, country, language = chm.GetLCID()
        encoding = codepage2encoding(codepage)
        self._encoding = encoding or 'utf-8'

        self._homeurl = normalize_url( chm.home.decode(encoding) )
        self._title   = chm.title.decode(encoding)

        return True

    @property
    def title(self):
        "Title of this CHM file"
        return self._title

    @property
    def home(self):
        "Home of this file"
        return self._homeurl

    @property
    def encoding(self):
        "Encoding of this chm file"
        return self._encoding

    @property
    def index(self):
        "Index of this chm file"
        if self._index_table :
            return self._index_table

        if not self._chm.index :
            self._index_table = []
            return []

        index_url = self._chm.index.decode(self._encoding)
        index_data = self.getContentsByURL(index_url)
        if not index_data:
            index_data = self._chm.GetIndex()
        if index_data:
            self._parseIndexTable(index_data.decode(self._encoding, 'ignore'))

        return self._index_table

    @property
    def topics(self):
        if self._content_table :
            return self._content_table

        if not self._chm.topics :
            self._content_table = []
            return []

        topics_url = self._chm.topics.decode(self._encoding)
        topics_data = self.getContentsByURL(topics_url)

        if not topics_data:
            topics_data = self._chm.GetTopicsTree()
        if topics_data:
            self._parseContentTable(topics_data.decode(self._encoding) )

        return self._content_table

    def checkURL(self, url):
        '''
        url: unicode
        check if the url is available
        return bool
        '''
        assert isinstance(url, unicode)

        url = normalize_url(url)
        if not url :
            return False

        fail, _ = self._chm.ResolveObject( url.encode('utf-8') )

        return not bool(fail)


    def getContentsByURL(self, url):
        '''
        url must be unicode
        return the file content @ url as raw data (not encoded)
        if failed, return None
        '''
        assert isinstance(url, unicode)

        url = normalize_url(url)
        if not url :
            return None

        fail, unit_info = self._chm.ResolveObject( url.encode('utf-8') )
        if fail:
            return None

        length, data = self._chm.RetrieveObject(unit_info)

        return data[0:length] if length else None

    def _parseTable(self, data):
        parser = TableParser()
        parser.feed(data)
        return parser.EntryList

    def _parseContentTable(self, content):
        assert isinstance(content, unicode)

        self._content_table = self._parseTable(content)

    def _parseIndexTable(self, index):
        assert isinstance(index, unicode)

        self._index_table = self._parseTable(index)
        self._index_table.sort(key=lambda x:x.key)


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


    def _getEntryList(self):
#        self.close()
        return self.entrylist
    EntryList = property(_getEntryList)

    def start_object(self, attrs):
        for k, v in attrs:
            if v.lower() == u'text/sitemap':
                self.crtentry = TableEntry()
                return

    def end_object(self):
        if not self.crtentry :
            return
        if self.key :
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
        if self.crtentry :
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
