#!/usr/bin/python
# coding: utf8
#########################################################################
# Author: Xinyu.Xiang(John)
# email: zorrohunter@gmail.com
# Created Time: 2009年05月26日 星期二 01时17分03秒
# File Name: pychmwebview.py
# Description:
#########################################################################

import sys
import os.path
import urllib
import cStringIO as StringIO

from PyQt4 import QtCore, QtGui
from PyQt4.QtNetwork import QNetworkReply, QNetworkRequest, QNetworkAccessManager
from PyQt4.QtWebKit import QWebView, QWebPage
from PyQt4.QtCore import QTimer, QLatin1String, QUrl, QVariant
from PyQt4.QtCore import QIODevice, Qt

import urltools
import globalvalue
from content_type import content_type

urldecode = urllib.unquote_plus

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
        chm = globalvalue.chmFile
        if not chm:
            return ''
        path = unicode(url.path())
        try:
            pos = path.index(u'#')
            path = path[0:pos]
        except:
            pass
        path = urldecode(path)
        data = chm.GetFileAsStrByUrl(path)
        if not data:
            self.setError(404,'')
            return None
        self.setContentTypeHeader(path)
        #self.setHeader(QNetworkRequest.ContentTypeHeader, QVariant("text/html; charset=UTF-8"))
#        ext=os.path.splitext(path)[1].lower()
#        if len(ext)>0:
#            ext=ext[1:]
#        ctt_type=content_type.get(ext,'binary/octet')
#        if ctt_type.lower().startswith('text'):
#            print data.decode('gb18030')
        return data

    def setContentTypeHeader(self, path):
        ext = os.path.splitext(path)[1].lower()
        if len(ext)>0:
            ext = ext[1:]
        ctt_type = content_type.get(ext, 'binary/octet')
        if ctt_type.lower().startswith('text') and globalvalue.encoding is not None:
            ctt_type += '; charset=' + globalvalue.encoding
        self.setHeader(QNetworkRequest.ContentTypeHeader, QVariant(ctt_type))


class PyChmNetworkAccessManager(QNetworkAccessManager):
    def __init__(self, parent):
        QNetworkAccessManager.__init__(self, parent)
        self.qwebview = parent

    def createRequest(self, op, request, outgoingdata):
        scheme = request.url().scheme()
#        print unicode(request.url().path())
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
        #self.setUrl(QtCore.QUrl('http://www.baidu.com'))
        self.connect(self, QtCore.SIGNAL('linkClicked(const QUrl&)'), self.onLinkClicked)
#        self.connect(self.zob, QtCore.SIGNAL('clicked()'), self.zoomout)
#        self.connect(self.zib, QtCore.SIGNAL('clicked()'), self.zoomin)
#        self.connect(self.normb, QtCore.SIGNAL('clicked()'), self.normsize)
#        self.connect(self.bb, QtCore.SIGNAL('clicked()'), self.back)
#        self.connect(self.fb, QtCore.SIGNAL('clicked()'), self.forward)
        self.connect(self, QtCore.SIGNAL('loadFinished(bool)'), self.onLoadFinished)
        self.zoom = 1.0
        self.setTextSizeMultiplier(1.0)
        self.reload()
        self.openedpg = None
        self.scrolltopos = 0

    def zoomout(self):
        '''
        zoom out fontsize
        '''
        self.zoom /= 1.2
        self.setTextSizeMultiplier(self.zoom)

    def zoomin(self):
        '''
        zoom in the fontsize
        '''
        self.zoom *= 1.2
        self.setTextSizeMultiplier(self.zoom)

    def normsize(self):
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
            self.page().currentFrame().setScrollBarValue(Qt.Vertical, self.scrolltopos)
            self.scrolltopos = 0
            globalvalue.tabs.setTabName(self)
        else:
#            mb=QtGui.QMessageBox(self)
#            mb.setText(u'file not found')
#            mb.exec_()
            #self.openPage(globalvalue.chmFile.HomeUrl)
            #tell user file not found!########################
            print 'file not found'

    def printPage(self):
        printer = QtGui.QPrinter(QtGui.QPrinter.HighResolution)
        dlg = QtGui.QPrintDialog(printer, self)
        if dlg.exec_()!=QtGui.QDialog.Accepted:
            return
        self.print_(printer)

    def back(self):
        self.history().back()

    def forward(self):
        self.history().forward()

    def contextMenuEvent(self, event):
        '''
        inner method
        '''
        menu = QtGui.QMenu(self)
        link = self.anchorAt(event.pos())
        if link is not None:
            self.keepnewtaburl = link
            menu.addAction(u'在新标签页打开', self.openinnewtab)
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
        link = self.anchorAt(event.pos())
        self.keepnewtaburl = link
        if self.keepnewtaburl is not None and len(self.keepnewtaburl) != 0:
            if self.keepnewtaburl[0:4] == 'http':
                self.emit(QtCore.SIGNAL('openremoteatnewtab'), self.keepnewtaburl)
                return
            self.emit(QtCore.SIGNAL('openatnewtab'), self.keepnewtaburl)


    def anchorAt(self, pos):
        '''
        inner method
        '''
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
            url = globalvalue.chmFile.HomeUrl
        isnew, ochm, pg = urltools.isnewchmurl(unicode(qurl.toString()))
        if isnew:
            ochm = os.path.join(os.path.dirname(globalvalue.chmpath), ochm)
            if ochm != globalvalue.chmpath:
                url = pg
            else:
                return None
        url = os.path.normpath(url)
        return url

    def openinnewtab(self):
        '''
        inner method
        '''
        if self.keepnewtaburl is not None and len(self.keepnewtaburl) != 0:
            if self.keepnewtaburl[0:4] == 'http':
                self.emit(QtCore.SIGNAL('openremoteatnewtab'), self.keepnewtaburl)
                return
            self.emit(QtCore.SIGNAL('openatnewtab'), self.keepnewtaburl)

    def onLinkClicked(self, qurl):
        '''
        inner method
        '''
        if qurl.scheme() == 'http' or qurl.scheme() == 'https':
            #self.openPage(unicode(qurl.toString())) #delete this and emit the url #######################################
            self.emit(QtCore.SIGNAL('openRemoteUrl'), unicode(qurl.toString()))
            return
        if qurl.scheme() != 'ms-its':
            return
        url = unicode(qurl.path())
        if url == u'/':
            url = globalvalue.chmFile.HomeUrl
        isnew, ochm, pg = urltools.isnewchmurl(unicode(qurl.toString()))
        if isnew:
            ochm = os.path.join(os.path.dirname(globalvalue.chmpath), ochm)
            if ochm != globalvalue.chmpath:
                url = pg
            else:
                return
        url = os.path.normpath(url)
        #self.openPage(url) #delete this and emit the url #######################################
        self.emit(QtCore.SIGNAL('openUrl'), url)

#    def clearurl(self, url):
#        if len(url)==0:
#            return None
#        if urltools.isjsurl(url):
#            return None
#        if urltools.isRemoteURL(url)[0]:
#            return None
#        isnew, ochm, pg=urltools.isnewchmurl(url)
#        if isnew:
#            if os.path.abspath(ochm)!=os.path.abspath(globalvalue.chmpath):
#                url=pg
#            else:
#                pass
#                return None
#        if url.lower().startswith(u'ms-its:'):
#            url=url[7:]
#        if url[0]!=u'/':
#            url=self.baseurl+u'/'+url
#        url=os.path.normpath(url)
#        return url

    def openPage(self, url):
        '''
        url: unicode or Qstring. must be absolute url(ignore the first '/' is ok) in current chmfile
        '''
        assert isinstance(url, QtCore.QString) or isinstance(url, unicode)
        if isinstance(url, QtCore.QString):
            url = unicode(url)
        if url[0:4] == 'http':
#            if not globalvalue.globalcfg.openremote:
#                return
            self.load(QtCore.QUrl(url))
            globalvalue.tabs.setTabName(self)
            self.openedpg = url
            return
        if url == u'/':
            url = globalvalue.chmFile.HomeUrl
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
            url = u'ms-its://'+url
        #self.setUrl(QtCore.QUrl(url))
        self.load(QtCore.QUrl(url))
        #set title on tab
        globalvalue.tabs.setTabName(self)
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
        self.scrolltopos = pos
        self.page().currentFrame().setScrollBarValue(Qt.Vertical, pos)

    def canback(self):
        return self.history().canGoBack()

    def canforward(self):
        return self.history().canGoForward()

if __name__ == '__main__':

    import sys
    import locale
    from pychmfile import PyChmFile

    default_encoding = locale.getdefaultlocale()[1]

    if len(sys.argv) > 1:

        globalvalue.chmpath = sys.argv[1].decode(default_encoding)
        globalvalue.chmFile = PyChmFile()
        globalvalue.chmFile.loadFile(globalvalue.chmpath)

        app = QtGui.QApplication(sys.argv)
        Form = PyChmWebView()
    #    Form.code = 'gbk'
        Form.openPage(globalvalue.chmFile.HomeUrl)
        Form.show()
        sys.exit(app.exec_())
