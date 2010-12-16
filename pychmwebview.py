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
from PyQt4.QtWebKit import QWebView, QWebPage
from PyQt4.QtCore import QTimer, QString, QUrl, QVariant, QIODevice
from PyQt4.QtNetwork import (QNetworkReply,
                             QNetworkRequest,
                             QNetworkAccessManager)

from content_type import content_types

def path2ChmURL(path, default):
    if path == '/':
        path = default
    if path[0] != '/':
        path = '/' + path

    if not path.startswith("ms-its://"):
        return QUrl( "ms-its://" + path )
    else:
        return QUrl(path)


class PyChmNetReply(QNetworkReply):
    def __init__(self, parent, request,  qwebview ):
        QNetworkReply.__init__(self, parent)
        self.qwebview = qwebview

        self.setRequest(request)
        self.setOpenMode(QIODevice.ReadOnly)

        rawdata      = self._loadResource( request.url() )

        if rawdata :
            self._data   = StringIO.StringIO(rawdata)
            self._length = len(rawdata)
        else:
            self._data   = StringIO.StringIO("")
            self._length = 0

        self._left   = self._length

        self.setHeader(QNetworkRequest.ContentLengthHeader,
                       QVariant(QtCore.QByteArray.number(self._length)),
                      )

        # [Notes for using QTimer]
        # We need to queue the signal rather than emit it directly,
        # because when this reply is being created, the browser does not
        # know about it yet
        QTimer.singleShot(0, self, QtCore.SIGNAL('metaDataChanged()'))
        QTimer.singleShot(0, self, QtCore.SIGNAL('readyRead()'))
        # [important] never remove this line
        QTimer.singleShot(0, self, QtCore.SIGNAL('finished()'))

    def abort(self):
        pass

    def bytesAvailable(self):
        return self._left + QNetworkReply.bytesAvailable(self)

    def readData(self, maxlen):
        data = self._data.read(maxlen)
        self._left = self._length - self._data.tell()
        if self._left == 0:
            QTimer.singleShot(0, self, QtCore.SIGNAL('finished()'))
        return data


    def _loadResource(self, url):
        chmfile = self.qwebview.chmfile
        if not chmfile:
            return ""

        print "[Netreply] asked to load %s " % \
            unicode(url.toString()).encode('utf-8')
        path = unicode(url.path())
        path = urllib.unquote_plus(path)

        data = chmfile.getContentsByURL(path)
        if data:
            self._setContentTypeHeader(path)
            return data
        else:
            print "[NetReply] failed to load %s" % path.encode('utf-8')
            self.setError(QNetworkReply.ContentNotFoundError,
                          "%s not found." % path,
                         )

            return ""

    def _setContentTypeHeader(self, path):
        "provide necessary charset info, so that webkit can show it nicely"
        ext = os.path.splitext(path)[1].lower()
        if ext :
            content_type = content_types.get(ext, 'binary/octet').lower()
            if content_type.startswith('text') and self.qwebview.encoding :
                content_type += ("; charset=%s" % self.qwebview.encoding)

            self.setHeader(QNetworkRequest.ContentTypeHeader,
                           QVariant(content_type),
                          )

class PyChmNetworkAccessManager(QNetworkAccessManager):
    def __init__(self, parent):
        QNetworkAccessManager.__init__(self, parent)
        self.qwebview = parent

    def createRequest(self, op, request, outgoingdata):
        # special case for links related with .CHM
        print "[createRequest] %s" % unicode(request.url().toString()).encode('utf-8')

        if request.url().scheme() == QString("ms-its"):
            return PyChmNetReply(self,
                                 request,
                                 self.qwebview,
                                 )
        else:
            return QNetworkAccessManager.createRequest(self,
                                                       op,
                                                       request,
                                                       outgoingdata
                                                       )


# [Note]
# setHtml(htmldata)  an alternative to load()
# loadProgress()
# loadStarted()

class PyChmWebView(QWebView):
    def __init__(self, tabmanager, chmfile, parent):
        '''
        signal 'openURL' will be emited(with param url:unicode)
        signal 'openURLatNewTab' will be emited(with param url:unicode)
        '''
        QWebView.__init__(self, parent)

        # Whenever a link is activated, the linkClicked() signal is emitted.
        self.page().setLinkDelegationPolicy(QWebPage.DelegateAllLinks)

        self.page().setNetworkAccessManager(PyChmNetworkAccessManager(self))

        self.connect(self,
                     QtCore.SIGNAL('linkClicked(const QUrl&)'),
                     self.onLinkClicked)
        self.connect(self,
                     QtCore.SIGNAL('loadFinished(bool)'),
                     self.onLoadFinished)
        self.connect(self,
                     QtCore.SIGNAL('loadStarted()'),
                     self.onLoadStarted)
        self.connect(self,
                     QtCore.SIGNAL('loadProgress(int)'),
                     self.onLoadProgress)

        self.tabmanager   = tabmanager
        self.session      = tabmanager.session
        self.chmfile      = chmfile
        #self.encoding     = chmfile.encoding or "gb18030"
        self.encoding     = "gb18030"
        self.loadedURL    = None
        self.suggestedPos = 0
        self.zoom         = 1.0


    # FIXME; maybe not needed?
    def clone(self):
        view = PyChmWebView(tabmanager=self.tabmanager,
                            chmfile=self.chmfile,
                            parent=self.parent() )

        view.encoding     = self.encoding
        view.loadedURL    = self.loadedURL
        view.suggestedPos = self.currentPos()

        return view

    def keyPressEvent(self, event):
        if event.matches(QtGui.QKeySequence.Refresh):
            self.reload()
        elif event.matches(QtGui.QKeySequence.Back):
            self.goBack()
        elif event.matches(QtGui.QKeySequence.Forward):
            self.goForward()
        else:
            QWebView.keyPressEvent(self, event)

    def contextMenuEvent(self, event):
        # triggerd when user right-click mouse or press context key
        menu = QtGui.QMenu(self)

        link = self.anchorAt(event.pos())
        if link :
            self.keepnewtaburl = link
            menu.addAction(u"Open in new tab", self.openURLatNewTab)

            copyLink = self.pageAction(QWebPage.CopyLinkToClipboard)
            copyLink.setText(u"Copy link ")
            menu.addAction(copyLink)

            menu.addSeparator()

        if self.selectedText().isEmpty():
            menu.addAction(u"Select all", self.onSelectAll)
        else:
            menu.addAction(u"Copy selected text", self.onCopy)

        menu.exec_(event.globalPos())

    def mousePressEvent(self, event):
        # open url at new tab, with middle button
        if event.button() == QtCore.Qt.MidButton:
            url = self.anchorAt(event.pos())
            if url:
                self.keepnewtaburl =  url
                self.openURLatNewTab()
        else:
            QWebView.mousePressEvent(self, event)

    def openURLatNewTab(self):
        if self.keepnewtaburl :
            self.emit(QtCore.SIGNAL('openURLatNewTab'), self.keepnewtaburl)

    def normalizeChmURL(self, chmurl):
        if chmurl.hasFragment():
            archor = u"#" + unicode( chmurl.encodedFragment() )
        else:
            archor = ""

        path = unicode(chmurl.path() ) + archor
        home = self.chmfile.home

        return path2ChmURL(path, home)

    def onLinkClicked(self, qurl):
        print "[linkClicked] original url: %s" \
                % unicode(qurl.toString()).encode('utf-8')

        if qurl.scheme() in [ "http", "https"] :
            self.emit(QtCore.SIGNAL('openURL'), qurl)
        elif qurl.scheme() == 'ms-its':
            url = self.normalizeChmURL(qurl)
            self.emit(QtCore.SIGNAL('openURL'), url)
        else:
            raise NotImplementedError("")

    # this method is only reponsible for loading url in itself
    # creating new tab is not with its concern
    def loadURL(self, url):
        assert isinstance(url, unicode) or isinstance(url, QUrl)

        if isinstance(url, QUrl):
            finalurl = url
        else:
            qurl = QUrl(url)
            finalurl = self.normalizeChmURL(qurl)

        print ("[loadURL] final url:  %s" % \
                unicode(finalurl.toString()).encode('utf-8') )

        self.load(finalurl)
        self.show()
        self.tabmanager.setTabName(self, self.title() )

        self.loadedURL = unicode(finalurl.toString())
        #self.loadedURL = finalurl

    def anchorAt(self, pos):
        # Performs a hit test on the frame contents at the given position
        result = self.page().currentFrame().hitTestContent(pos)
        qurl   = result.linkUrl()

        if not qurl.isValid():
            return None
        else:
            print "[contextLink] %s" % unicode(qurl.toString()).encode('utf-8')
            if qurl.scheme() in [ "http", "https"] :
                return unicode(qurl.toString())
            elif qurl.scheme() == "ms-its":
                return unicode( qurl.toString() )
            else:
                return None

    def onCopy(self):
        self.triggerPageAction(QWebPage.Copy)

    def onSelectAll(self):
        self.triggerPageAction(QWebPage.SelectAll)

    def zoomIn(self):
        self.zoom *= 1.2
        # only influence text
        self.setTextSizeMultiplier(self.zoom)
        # influence both text and image
        #self.setZoomFactor(self.zoom)

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
        self.loadURL(self.chmfile.home)

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
            print ("[loadFinished] failed to load page")

    def onLoadStarted(self):
        print "[onLoadStarted]"

    def onLoadProgress(self, percent):
        print "[onLoadProgress] %d" % percent


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
