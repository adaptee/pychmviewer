#!/usr/bin/python
# vim: set fileencoding=utf-8 :

from PyQt4 import QtGui
from Ui_about import Ui_Dialog

class AboutDialog(QtGui.QDialog, Ui_Dialog):
    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self, parent)
        self.setupUi(self)
