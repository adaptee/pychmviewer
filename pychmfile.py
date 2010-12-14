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
import bsddb

from chm.chm import CHMFile
from chm import chmlib

import soup
from md5sum import md5sum
from utils import remove_comment, CachedProperty
from session import system_encoding

# TODO: provide serious implementation
def codepage2encoding(codepage):
    return 'gb18030' if codepage == 'cp936' else codepage

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


class PyChmFile(object):
    def __init__(self, session, path, force_encoding=None):
        self.initialize()
        self.session = session
        self.loadFile(path, force_encoding)

    def initialize(self):
        self._chm            = CHMFile()
        self._title          = u""
        self._home           = u""
        self._encoding       = u""
        self._force_encoding = u""
        self._fullpath       = u""
        self._md5sum         = None
        self._bookmarkdb     = None
        self._topics_table  = [ ]
        self._index_table    = [ ]

    def reset(self):
        self._chm.CloseCHM()
        self.initialize()

    def loadFile(self, filename, force_encoding=None):
        assert isinstance(filename, unicode)

        if force_encoding:
            self._force_encoding = force_encoding

        if not self._chm.LoadCHM(filename.encode(system_encoding)):
            raise IOError("Failed to load: %s" % filename)

        chm = self._chm

        codepage, _country, _language = chm.GetLCID()
        encoding = codepage2encoding(codepage)
        self._encoding = encoding or 'utf-8'

        self._home = normalize_url( chm.home.decode(encoding) )
        self._title   = chm.title.decode(encoding)

        def getFullPath(filename):
            filename = filename.encode(system_encoding)
            fullpath = os.path.realpath(filename)
            return fullpath.decode(system_encoding)

        def getBookmarkdb(md5sum):
            dbname = "bookmarks.db"
            config_dir = self.session.config_dir
            private_dir = os.path.join(config_dir, md5sum)

            if not os.path.exists(private_dir):
                os.mkdir(private_dir, 0755)

            return bsddb.hashopen( os.path.join(private_dir, dbname) )

        self._fullpath = getFullPath(filename)

        self._md5sum = md5sum(self.path)

        self._bookmarkdb = getBookmarkdb(self.md5sum)


    def search(self, pattern):
        def guessEncoding(contents):
            meta_charset = re.compile(r'<meta\b[^<]*?charset\s*?=\s*?([\w-]+)[\s\'"]', re.I)

            match = meta_charset.search(contents)
            if match:
                encoding = match.group(1)
            else :
                encoding = self.encoding
            return encoding

        urls = self.getSearchableURLs()

        for url in urls:
            contents = self.getContentsByURL(url.decode('utf-8', 'ignore'))
            if contents:
                encoding = guessEncoding(contents)
                contents = unicode(contents, encoding)
                match = re.search(pattern, contents, re.U)
                if match:
                    yield( url.decode('utf-8', 'ignore'),
                           match.group(0),
                         )
                else:
                    yield None
            else:
                yield None

    def getSearchableURLs(self):
        searchable_extensions = [ ".htm", ".html", ".txt"   ]

        def filterByExtension(urls, exts):
            urls   = [ url.lower() for url in urls ]

            results = [ ]
            for url in urls:
                for ext in exts:
                    if url.endswith(ext):
                        results.append(url)

            return results

        return filterByExtension( self.allURLs, searchable_extensions )

    @CachedProperty
    def allURLs(self):
        '''
        get all the URLs in  this chm file
        [note], return raw url, not unicode
        '''

        def collector(cf, ui, paths):
            paths.append(ui.path)
            return chmlib.CHM_ENUMERATOR_CONTINUE

        chmfile = chmlib.chm_open( self.path.encode(system_encoding) )

        paths = []
        ok = chmlib.chm_enumerate(chmfile,
                                  chmlib.CHM_ENUMERATE_ALL,
                                  collector,
                                  paths
                                 )

        chmlib.chm_close(chmfile)

        return paths if ok else [ ]

    def extractAll(self, output_dir):
        def normalize_path(path):
            if path[0] != '/':
                path = '/' + path
            path = os.path.normpath(path)
            path = path[1:]
            return path

        def prepare_for_extracting_to(fullpath):
            dirname = os.path.dirname(fullpath)
            if not os.path.exists(dirname):
                os.mkdir(dirname)


        urls = self.allURLs
        for url in urls:
            # FIXME; always decode using 'utf-8'?
            url = url.decode('utf-8')

            path = url.encode(system_encoding)
            path = normalize_path(path)

            fullpath = os.path.join(output_dir, path)
            try:
                prepare_for_extracting_to(fullpath)
            except OSError:
                yield ( False, u"[failure] %s" % url )
            else:
                contents = self.getContentsByURL(url)

                if contents:
                    try :
                        with open(fullpath, 'w') as writer:
                            writer.write(contents)
                        yield ( True,  u"[success] %s" % url )
                    except IOError :
                        yield ( False, u"[failure] %s" % url )
                else:
                    yield( True, "[skip] %s (empty)" % url )

    @property
    def title(self):
        "Title of this CHM file"
        return self._title

    @property
    def home(self):
        "Home of this file"
        return self._home

    @property
    def encoding(self):
        "Encoding of this chm file"
        return self._force_encoding  or self._encoding

    @property
    def path(self):
        "Encoding of this chm file"
        return self._fullpath

    @property
    def md5sum(self):
        "md5sum of this file"
        return self._md5sum

    @property
    def bookmarkdb(self):
        "small database for storing bookmarks of this chm file"
        return self._bookmarkdb

    @CachedProperty
    def index(self):
        "Index of this chm file"
        if not self._chm.index :
            return [ ]

        index_url  = self._chm.index.decode(self.encoding)
        index_data = self.getContentsByURL(index_url)

        if index_data:
            #_, tree = soup.parse(index_data.decode(self.encoding))
            _, _, tree = soup.parse(index_data.decode(self.encoding))
            return tree

    @CachedProperty
    def topics(self):
        if not self._chm.topics :
            return []

        topics_url  = self._chm.topics.decode(self.encoding)
        topics_data = self.getContentsByURL(topics_url)

        if topics_data :
            #_, tree = soup.parse(topics_data.decode(self.encoding))
            _, _, tree = soup.parse(topics_data.decode(self.encoding))
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
            return ""

        fail, unit_info = self._chm.ResolveObject( url.encode('utf-8') )
        if fail:
            return ""

        length, data = self._chm.RetrieveObject(unit_info)

        return data[0:length] if length else ""

