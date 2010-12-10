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
from chm import chmlib

import soup
from utils import remove_comment, getencoding, getcfg
from session import system_encoding

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

def getExtensions():
    extensions= []

    for ext, enable in getcfg().searchext.iteritems():
        if enable:
            extensions.append(ext)

    return extensions

def filterByExt(filenames, exts):
    if not filenames or not exts:
        return filenames

    filenames = [ filename.lower() for filename in filenames  ]
    exts      = [ ext.lower() for ext in exts  ]
    results   = [ ]

    for filename in filenames:
        for ext in exts:
            if filename.endswith(ext):
                results.append(filename)

    return results


def guessEncoding(contents):
    meta_charset = re.compile(r'<meta\b[^<]*?charset\s*?=\s*?([\w-]+)[\s\'"]', re.I)

    match = meta_charset.search(contents)
    if match:
        encoding = match.group(1)
    elif getencoding():
        encoding = getencoding()
    else:
        encoding = "utf-8"

    return encoding



class PyChmFile(object):
    #self._chm.filename

    #self._chm.GetTopicsTree()  (data)
    #self._chm.GetIndex()       (data)
    #self._chm.index   (url only)
    #self._chm.topics  (url only)
    def __init__(self):
        self.initialize()

    def initialize(self):
        self._chm           = CHMFile()
        self._title         = u""
        self._homeurl       = u""
        self._encoding      = u""
        self._content_table = [ ]
        self._index_table   = [ ]
        self._fullpath      = ""

    def reset(self):
        self._chm.CloseCHM()
        self.initialize()

    def loadFile(self, filename):
        '''
        filename must be unicode
        if success,return True,
        else,return False
        '''

        assert isinstance(filename, unicode)
        self.reset()

        if not self._chm.LoadCHM(filename.encode(system_encoding)):
            print ("load file failed")
            return False

        chm = self._chm

        codepage, _country, _language = chm.GetLCID()
        encoding = codepage2encoding(codepage)
        self._encoding = encoding or 'utf-8'

        self._homeurl = normalize_url( chm.home.decode(encoding) )
        self._title   = chm.title.decode(encoding)

        def getFullPath(filename):
            filename = filename.encode(system_encoding)
            fullpath = os.path.realpath(filename)
            return fullpath.decode(system_encoding)

        self._fullpath = getFullPath(filename)

        return True



    def search(self, pattern):
        urls = self.getSearchableURLs()

        for url in urls:

            file_content = self.getContentsByURL(url.decode('utf-8', 'ignore'))
            if file_content:
                encoding = guessEncoding(file_content)

                rc = re.compile(unicode(pattern).encode(self.encoding))
                match = rc.search(file_content)
                if match:
                    yield( ( url.decode('utf-8', 'ignore'),
                            match.group(0).decode(encoding, 'ignore'),
                        )
                        )
                else:
                    yield None
            else:
                yield None

    def getSearchableURLs(self):
        return filterByExt( self._getfilelist(), getExtensions() )


    def _getfilelist(self):
        '''
        get filelist of the given path chm file
        return (bool,fileurllist)
        '''

        def callback(cf, ui, paths):
            '''
            innermethod
            '''
            paths.append(ui.path)
            return chmlib.CHM_ENUMERATOR_CONTINUE


        chmfile = chmlib.chm_open( self._fullpath.encode(system_encoding) )

        paths = []
        ok = chmlib.chm_enumerate(chmfile, chmlib.CHM_ENUMERATE_ALL, callback, paths)
        chmlib.chm_close(chmfile)

        if ok:
            return paths
        else:
            return []


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
            _, tree = soup.parse(index_data.decode(self._encoding))
            self._index_table = tree

            return tree




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

        if topics_data :
            _, tree = soup.parse(topics_data.decode(self._encoding))
            self._content_table = tree

            return tree

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


