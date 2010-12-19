#!/usr/bin/python
# vim: set fileencoding=utf-8 :

" Provides the dialog for viewing Html Source code. "

from PyQt4 import QtGui

from Ui_htmlsourcedlg import Ui_Dialog

class HtmlDialog(QtGui.QDialog, Ui_Dialog):
    " Implement the dialog for viewing Html Source code. "
    def __init__(self, parent=None):
        " Initialize all widgets contained. "
        QtGui.QDialog.__init__(self, parent)
        self.setupUi(self)
