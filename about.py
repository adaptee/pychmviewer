#!/usr/bin/python
# vim: set fileencoding=utf-8 :

" Provides the  about dialog in help menu. "


from PyQt4 import QtGui
from Ui_about import Ui_Dialog

class AboutDialog(QtGui.QDialog, Ui_Dialog):
    " Impelment the about dialog. "
    def __init__(self, session, parent=None):
        " Fill various infomation into the dialog. "

        QtGui.QDialog.__init__(self, parent)
        self.setupUi(self)

        self.setWindowTitle( u"%s" % session.description)

        detail = u""
        detail += u"<html>"

        detail += u"<b>%s version %s</b>" % \
                (session.application, session.version)
        detail += u"<br>"
        detail += u"<br>"

        for author in session.authors:
            name, email, period = author
            detail += "<a href='mailto:%s'>%s</a> Copyright (C) %s" % \
                    (email, name, period)
            detail += "<br>"

        detail += "<br>"
        detail += u"<a href='%s'>%s</a>" % \
                (session.homepage, session.homepage)
        detail += "<br>"

        detail += u"Licensed under %s" % (session.license)
        detail += u"<br>"

        detail += u"</html>"

        self.labelDetailInfo.setText(detail)
