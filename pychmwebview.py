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
from utils import remove_comment
from content_type import content_types


class PyChmNetReply(QNetworkReply):
    def __init__(self, request, url, parent=None, qwebview=None):
        QNetworkReply.__init__(self, parent)
        self.qwebview = qwebview

        self.setRequest(request)
        self.setOpenMode(QIODevice.ReadOnly)

        self.m_data   = self.loadResource(url)
        self.m_length = len(self.m_data)
        self.m_data   = StringIO.StringIO(self.m_data)

        self.left     = self.m_length

        self.setHeader(QNetworkRequest.ContentLengthHeader, QVariant(QtCore.QByteArray.number(self.m_length)))

        QTimer.singleShot(0, self, QtCore.SIGNAL('readyRead()'))

    def loadResource(self, url):
        chmfile = self.qwebview.chmfile
        if not chmfile:
            return ""

        path = unicode(url.path())
        path = remove_comment(path)
        path = urllib.unquote_plus(path)

        data = chmfile.getContentsByURL(path)
        #print ("[loadResource] data length:%s" % len(data))

        if data:
            self.setContentTypeHeader(path)
            return data
        else:
            self.setError(404, "")
            return ""

    def setContentTypeHeader(self, path):
        "provide necessary charset info, so that webkit can show it nicely"
        ext = os.path.splitext(path)[1].lower()
        if ext :
            ext = ext[1:]

        content_type = content_types.get(ext, 'binary/octet').lower()
        if content_type.startswith('text') and self.qwebview.encoding :
            content_type += ("; charset=%s" % self.qwebview.encoding)

        self.setHeader(QNetworkRequest.ContentTypeHeader, QVariant(content_type))


    def bytesAvailable(self):
        return self.left + QNetworkReply.bytesAvailable(self)

    def readData(self, maxlen):
        data = self.m_data.read(maxlen)
        self.left = self.m_length - self.m_data.tell()
        if self.left == 0:
            QTimer.singleShot(0, self, QtCore.SIGNAL('finished()'))
        return data

    def abort(self):
        pass


class PyChmNetworkAccessManager(QNetworkAccessManager):
    def __init__(self, parent):
        QNetworkAccessManager.__init__(self, parent)
        self.qwebview = parent

    def createRequest(self, op, request, outgoingdata):
        scheme = request.url().scheme()

        # special case for links related with .CHM
        if scheme == QLatin1String("ms-its"):
            return PyChmNetReply(request, request.url(), self.qwebview, self.qwebview)
        else:
            return QNetworkAccessManager.createRequest(self, op, request, outgoingdata)

class PyChmWebView(QWebView):
    def __init__(self, tabmanager, chmfile, parent):
        '''
        zoom: zoom out times
        openedpg: current openedpage
        signal 'openURL' will be emited(with param url:unicode)
        signal 'openURLatNewTab' will be emited(with param url:unicode)
        signal 'openRemoteURLatNewTab' will be emited(with param url:unicode)
        signal 'openRemoteURL' will be emited(with param url:unicode)
        '''
        QWebView.__init__(self, parent)
        self.page().setNetworkAccessManager(PyChmNetworkAccessManager(self))
        self.page().setLinkDelegationPolicy(QWebPage.DelegateAllLinks)

        self.zoom = 1.0
        self.tabmanager = tabmanager
        self.session    = tabmanager.session
        self.chmfile    = chmfile
        self.encoding   = "gb18030"
        self.url        = None
        self.openedpg   = None
        self.suggestedPos = 0

        self.connect(self, QtCore.SIGNAL('linkClicked(const QUrl&)'), self.onLinkClicked)
        self.connect(self, QtCore.SIGNAL('loadFinished(bool)'), self.onLoadFinished)

    # FIXME; maybe not needed?
    def clone(self):
        view = PyChmWebView(tabmanager=self.tabmanager,
                            chmfile=self.chmfile,
                            parent=self.parent() )

        view.enocding     = self.encoding
        view.suggestedPos = self.currentPos()
        view.url          = self.url
        view.openedpg     = self.openedpg

        return view

    def keyPressEvent(self, event):
        if event.matches(QtGui.QKeySequence.Copy):
            self.copyToClipboard()
        elif event.matches(QtGui.QKeySequence.SelectAll):
            self.selectAll()
        elif event.matches(QtGui.QKeySequence.Refresh):
            self.reload()
        elif event.matches(QtGui.QKeySequence.Back):
            self.goBack()
        elif event.matches(QtGui.QKeySequence.Forward):
            self.goForward()
        #elif event.matches(QtGui.QKeySequence.ZoomIn):
            #self.zoomIn()
        #elif event.matches(QtGui.QKeySequence.ZoomOut) :
            #self.zoomOut()
        else:
            QWebView.keyPressEvent(self,event)


    def contextMenuEvent(self, event):
        menu = QtGui.QMenu(self)
        link = self.anchorAt(event.pos())
        if link :
            self.keepnewtaburl = link
            menu.addAction(u"在新标签页打开", self.openAtNewPage)
            menu.exec_(event.globalPos())
        if not self.selectedText().isEmpty():
            menu.addAction(u"复制", self.copyToClipboard)
            menu.exec_(event.globalPos())

    def mousePressEvent(self, event):
        # special support for middle button
        if event.button() == QtCore.Qt.MidButton:
            # FIXME; is this really worthwhile?
            self.keepnewtaburl = self.anchorAt(event.pos())
            if self.keepnewtaburl :
                if self.keepnewtaburl[0:4] == "http":
                    self.emit(QtCore.SIGNAL('openRemoteURLatNewTab'), self.keepnewtaburl)
                else:
                    self.emit(QtCore.SIGNAL('openAtNewTab'), self.keepnewtaburl)
        else:
            QWebView.mousePressEvent(self, event)

    def onLinkClicked(self, qurl):
        # toString() provides full info,
        # path() only provide the
        print "[linkClicked] url: %s" % unicode(qurl.toString()).encode('utf-8')

        if qurl.scheme() in [ "http", "https"] :
            self.emit(QtCore.SIGNAL('openRemoteURL'), unicode(qurl.toString()))
            return

        elif qurl.scheme() == 'ms-its':
            url = unicode(qurl.path())
            print "[finalurl] url: %s" % url.encode('utf-8')

            chmfile = self.chmfile

            if url == u'/':
                url = chmfile.home

            url = os.path.normpath(url)
            self.emit(QtCore.SIGNAL('openURL'), url)

        else:
            raise NotImplementedError("")

    # this method is only reponsible for loading url in current view
    # whether creating new tab is not with its concern
    # FIXME; currently only support 3 scheme:
    # http,
    # https,
    # path(with out ms-its scheme prefix  within .chm)

    def openPage(self, url):
        '''
        url: unicode or Qstring. must be absolute url(ignore the first '/' is ok) in current chmfile
        '''
        assert isinstance(url, QtCore.QString) or isinstance(url, unicode)
        url = unicode(url)
        print ("[webview.openPage] original url: %s" % url)

        finalurl = ""

        if url == '/':
            finalurl = self.chmfile.home
        elif url.lower().startswith("http://") or \
            url.lower().startswith("ms-its://") :
            finalurl = url
        else:
            url = os.path.normpath(url)
            if url[0] != u'/':
                url = u'/' + url

            finalurl =  u"ms-its://" + url

        print ("[webview.openPage] final url:  %s" % finalurl )

        self.load(QtCore.QUrl(finalurl))
        self.show()
        self.tabmanager.setTabName(self, self.title() )

        self.openedpg = finalurl

    def anchorAt(self, pos):

        # Performs a hit test on the frame contents at the given position
        result = self.page().currentFrame().hitTestContent(pos)
        qurl   = result.linkUrl()

        if not qurl.isValid():
            return None
        else:
            if qurl.scheme() in [ "http", "https"] :
                return unicode(qurl.toString())
            elif qurl.scheme() == "ms-its":
                url = unicode(qurl.path())

                if url == u'/':
                    url = self.chmfile.home

                return  os.path.normpath(url)

            else:
                return None

    def openAtNewPage(self):
        if self.keepnewtaburl :
            if self.keepnewtaburl[0:4] == 'http':
                self.emit(QtCore.SIGNAL('openRemoteURLatNewTab'), self.keepnewtaburl)
            else:
                self.emit(QtCore.SIGNAL('openURLatNewTab'), self.keepnewtaburl)

    def copyToClipboard(self):
        QtGui.QApplication.clipboard().setText(self.selectedText())
        #self.triggerPageAction(QWebPage.Copy)

    def selectAll(self):
        #FIXME; it does not work
        self.triggerPageAction(QWebPage.MoveToStartOfDocument)
        self.triggerPageAction(QWebPage.SelectEndOfDocument)

    def zoomIn(self):
        self.zoom *= 1.2
        self.setTextSizeMultiplier(self.zoom)

    def zoomOut(self):
        self.zoom /= 1.2
        self.setTextSizeMultiplier(self.zoom)

    def zoomOff(self):
        " to make the font size normal "
        self.zoom = 1.0
        self.setTextSizeMultiplier(self.zoom)

    def printPage(self):
        printer = QtGui.QPrinter(QtGui.QPrinter.HighResolution)
        dialog = QtGui.QPrintDialog(printer, self)
        if dialog.exec_() == QtGui.QDialog.Accepted:
            self.print_(printer)

    def goHome(self):
        self.openPage(self.chmfile.home)

    def goBack(self):
        self.history().back()

    def goForward(self):
        self.history().forward()

    def canGoBack(self):
        return self.history().canGoBack()

    def canGoForward(self):
        return self.history().canGoForward()


    def onEncodingChanged(self, encoding):
        self.encoding = encoding
        self.chmfile.loadFile(self.chmfile.path, encoding)

        self.reload()

    def onLoadFinished(self, ok):
        if ok:
            self.setCurrentPos(self.suggestedPos)
            self.suggestedPos = 0

            self.tabmanager.setTabName(self, self.title() )
        else:
            print ("[loadFinished] page not found")

    def title(self):
        "override the QWebView.title() "

        page_title = QWebView.title(self)
        chm_title  = self.chmfile.title

        return page_title or chm_title or u"No Title"

    def currentPos(self):
        return self.page().currentFrame().scrollBarValue(QtCore.Qt.Vertical)

    def setCurrentPos(self, pos):
        self.page().currentFrame().setScrollBarValue(QtCore.Qt.Vertical, pos)

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


if __name__ == '__main__':
    raise NotImplementedError()
