#!/usr/bin/python
# coding: utf8
#########################################################################
# Author: Xinyu.Xiang(John)
# email: zorrohunter@gmail.com
# Created Time: 2009年05月26日 星期二 01时17分03秒
# File Name: pychmwebview.py
# Description:
#########################################################################

import os.path
import urllib
import cStringIO as StringIO

from PyQt4 import QtCore, QtGui
from PyQt4.QtNetwork import QNetworkReply, QNetworkRequest, QNetworkAccessManager
from PyQt4.QtWebKit import QWebView, QWebPage
from PyQt4.QtCore import QTimer, QLatin1String, QUrl, QVariant
from PyQt4.QtCore import QIODevice, Qt

import urltools
from utils import getchmfile, setchmfile, getencoding, gettabs, remove_comment
from content_type import content_types


class PyChmNetReply(QNetworkReply):
    def __init__(self, request, url, parent=None, qwebview=None):
        QNetworkReply.__init__(self, parent)
        self.qwebview = qwebview
        self.setRequest(request)
        self.setOpenMode(QIODevice.ReadOnly)
        self.m_data = self.loadResource(url)
        if self.m_data:
            self.m_length = len(self.m_data)
            self.m_data = StringIO.StringIO(self.m_data)
        else:
            self.m_length = 0
            self.m_data = StringIO.StringIO('')
        self.left = self.m_length
        self.setHeader(QNetworkRequest.ContentLengthHeader, QVariant(QtCore.QByteArray.number(self.m_length)))
#        QTimer.singleShot(0, self, QtCore.SIGNAL('metaDataChanged()'))
        QTimer.singleShot(0, self, QtCore.SIGNAL('readyRead()'))

    def bytesAvailable(self):
        return self.left + QNetworkReply.bytesAvailable(self)

    def abort(self):
        pass

    def readData(self, maxlen):
        data = self.m_data.read(maxlen)
        self.left = self.m_length-self.m_data.tell()
        if self.left == 0:
            QTimer.singleShot(0, self, QtCore.SIGNAL('finished()'))
        return data

    def loadResource(self, url):
        chm = getchmfile()
        if not chm:
            return ''

        path = unicode(url.path())
        path = remove_comment(path)
        path = urllib.unquote_plus(path)

        data = chm.getContentsByURL(path)
        if not data:
            self.setError(404,'')
            return None
        self.setContentTypeHeader(path)

        return data

    def setContentTypeHeader(self, path):
        ext = os.path.splitext(path)[1].lower()
        if ext :
            ext = ext[1:]
        ctt_type = content_types.get(ext, 'binary/octet')
        if ctt_type.lower().startswith('text') and getencoding() :
            ctt_type += '; charset=' + getencoding()
        self.setHeader(QNetworkRequest.ContentTypeHeader, QVariant(ctt_type))


class PyChmNetworkAccessManager(QNetworkAccessManager):
    def __init__(self, parent):
        QNetworkAccessManager.__init__(self, parent)
        self.qwebview = parent

    def createRequest(self, op, request, outgoingdata):
        scheme = request.url().scheme()
        if scheme == QLatin1String('ms-its'):
            return PyChmNetReply(request, request.url(), self.qwebview, self.qwebview)
        return QNetworkAccessManager.createRequest(self, op, request, outgoingdata)

class PyChmWebView(QWebView):
    def __init__(self, parent=None):
        '''
        zoom: zoom out times
        openedpg: current openedpage
        signal 'openUrl' will be emited(with param url:unicode)
        signal 'openatnewtab' will be emited(with param url:unicode)
        signal 'openremoteatnewtab' will be emited(with param url:unicode)
        signal 'openRemoteUrl' will be emited(with param url:unicode)
        '''
        QWebView.__init__(self, parent)
        self.page().setNetworkAccessManager(PyChmNetworkAccessManager(self))
        self.page().setLinkDelegationPolicy(QWebPage.DelegateAllLinks)
        self.connect(self, QtCore.SIGNAL('linkClicked(const QUrl&)'), self.onLinkClicked)
        self.connect(self, QtCore.SIGNAL('loadFinished(bool)'), self.onLoadFinished)
        self.zoomOff()
        self.reload()
        self.openedpg = None
        self.currentPos = 0

        #FIXME ; dirty hack
        self.tabsmanager = gettabs()
        #self.tabmanager = None
        self.chmfile = None
        self.encoding = "gb18030"

    def zoomOut(self):
        '''
        zoom out fontsize
        '''
        self.zoom /= 1.2
        self.setTextSizeMultiplier(self.zoom)

    def zoomIn(self):
        '''
        zoom in the fontsize
        '''
        self.zoom *= 1.2
        self.setTextSizeMultiplier(self.zoom)

    def zoomOff(self):
        '''
        to make the font size normal
        '''
        self.zoom = 1.0
        self.setTextSizeMultiplier(self.zoom)

    def find(self, text, backward=False, casesens=False):
        '''
        text: the search text
        backward:bool
        '''
        flags = QWebPage.FindWrapsAroundDocument
        if backward:
            flags |= QWebPage.FindBackward
        if casesens:
            flags |= QWebPage.FindCaseSensitively
        self.findText(text, flags)

    def onLoadFinished(self, ok):
        '''
        inner method
        '''
        if ok:
            self.page().currentFrame().setScrollBarValue(Qt.Vertical, self.currentPos)
            self.currentPos = 0
            self.tabsmanager.setTabName(self)
        else:
            print 'file not found'

    def printPage(self):
        printer = QtGui.QPrinter(QtGui.QPrinter.HighResolution)
        dialog = QtGui.QPrintDialog(printer, self)
        if dialog.exec_() != QtGui.QDialog.Accepted:
            return
        self.print_(printer)

    def goBack(self):
        self.history().back()

    def goForward(self):
        self.history().forward()

    def contextMenuEvent(self, event):
        '''
        inner method
        '''
        menu = QtGui.QMenu(self)
        link = self.anchorAt(event.pos())
        if link :
            self.keepnewtaburl = link
            menu.addAction(u'在新标签页打开', self.openAtNewPage)
            menu.exec_(event.globalPos())
        if not self.selectedText().isEmpty():
            menu.addAction(u'复制', self.copyToClipboard)
            menu.exec_(event.globalPos())

    def copyToClipboard(self):
        QtGui.QApplication.clipboard().setText(self.selectedText())

    def mousePressEvent(self, event):
        '''
        inner method
        '''
        if event.button() != QtCore.Qt.MidButton:
            QWebView.mousePressEvent(self, event)
            return

        self.keepnewtaburl = self.anchorAt(event.pos())
        if self.keepnewtaburl :
            if self.keepnewtaburl[0:4] == 'http':
                self.emit(QtCore.SIGNAL('openremoteatnewtab'), self.keepnewtaburl)
            else:
                self.emit(QtCore.SIGNAL('openatnewtab'), self.keepnewtaburl)


    def anchorAt(self, pos):
        '''
        inner method
        '''

        chmfile = getchmfile()
        chmpath = chmfile.path

        res = self.page().currentFrame().hitTestContent(pos)
        if not res.linkUrl().isValid():
            return None
        qurl = res.linkUrl()
        if qurl.scheme() == 'http' or qurl.scheme()== 'https' :
            return unicode(qurl.toString())
        if qurl.scheme() != 'ms-its':
            return None
        url = unicode(qurl.path())
        if url == u'/':
            url = chmfile.home
        isnew, ochm, pg = urltools.isNewChmURL(unicode(qurl.toString()))
        if isnew:
            ochm = os.path.join(os.path.dirname(chmpath), ochm)
            if ochm != chmpath:
                url = pg
            else:
                return None

        url = os.path.normpath(url)
        return url

    def openAtNewPage(self):
        '''
        inner method
        '''
        if self.keepnewtaburl :
            if self.keepnewtaburl[0:4] == 'http':
                self.emit(QtCore.SIGNAL('openremoteatnewtab'), self.keepnewtaburl)
                return
            self.emit(QtCore.SIGNAL('openatnewtab'), self.keepnewtaburl)

    def onLinkClicked(self, qurl):
        '''
        inner method
        '''

        chmfile = getchmfile()
        chmpath = chmfile.path


        if qurl.scheme() == 'http' or qurl.scheme() == 'https':
            self.emit(QtCore.SIGNAL('openRemoteUrl'), unicode(qurl.toString()))
            return
        if qurl.scheme() != 'ms-its':
            return
        url = unicode(qurl.path())
        if url == u'/':
            url = chmfile.home
        isnew, ochm, pg = urltools.isNewChmURL(unicode(qurl.toString()))
        if isnew:
            ochm = os.path.join(os.path.dirname(chmpath), ochm)
            if ochm != chmpath:
                url = pg
            else:
                return
        url = os.path.normpath(url)
        self.emit(QtCore.SIGNAL('openUrl'), url)

    def openPage(self, url):
        '''
        url: unicode or Qstring. must be absolute url(ignore the first '/' is ok) in current chmfile
        '''
        assert isinstance(url, QtCore.QString) or isinstance(url, unicode)
        if isinstance(url, QtCore.QString):
            url = unicode(url)
        if url[0:4] == 'http':
            self.load(QtCore.QUrl(url))
            self.tabsmanager.setTabName(self)

            self.openedpg = url
            return
        if url == u'/':
            url = getchmfile().home
        try:
            pos = url.index(u'://')
            if url[0:pos] != u'ms-its': #just for url in chmfile
                return
            url = url[0:pos]+os.path.normpath(url[pos+3:])
        except:
            url = os.path.normpath(url)
            if url[0] != u'/':
                url = u'/' + url
            url = os.path.normpath(url)

        if not url.lower().startswith(u'ms-its://'):
            url = u'ms-its://' + url
        print ("[debug] [webview.openPage] loading url: %s" % url)
        self.load(QtCore.QUrl(url))
        self.tabsmanager.setTabName(self)
        self.openedpg = url[9:]
        return True

    def getScrollPos(self):
        '''
        get current pos of the frame
        '''
        return self.page().currentFrame().scrollBarValue(Qt.Vertical)

    def setScrollPos(self, pos):
        '''
        set current pos of the frame
        '''
        self.currentPos = pos
        self.page().currentFrame().setScrollBarValue(Qt.Vertical, pos)

    def canGoBack(self):
        return self.history().canGoBack()

    def canGoForward(self):
        return self.history().canGoForward()

if __name__ == '__main__':

    import sys

    from pychmfile import PyChmFile
    from session import system_encoding

    if len(sys.argv) > 1:

        path = sys.argv[1].decode(system_encoding)
        chmfile = PyChmFile(path)
        setchmfile(chmfile)

        app = QtGui.QApplication(sys.argv)
        Form = PyChmWebView()
        Form.openPage(chmfile.home)
        Form.show()
        sys.exit(app.exec_())
