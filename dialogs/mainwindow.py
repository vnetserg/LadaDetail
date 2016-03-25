# -*- coding: utf-8 -*-

from PyQt5 import QtWidgets
from ui.ui_mainwindow import Ui_MainWindow

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, dbase, parent = None):
        super(MainWindow, self).__init__(parent)
        self.dbase = dbase
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
    