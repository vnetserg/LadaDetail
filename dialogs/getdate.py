# -*- coding: utf-8 -*-

from PyQt5 import QtWidgets, QtCore
from ui.ui_getdate import Ui_GetDate

class GetDate(QtWidgets.QDialog):
    def __init__(self, parent = None, label = None):
        super(GetDate, self).__init__(parent)
        self.date = None
        self.ui = Ui_GetDate()
        self.ui.setupUi(self)
        if label:
            self.ui.label.setText(label)
        self.ui.dateEdit.setDate(QtCore.QDate.currentDate())
        self.ui.buttonBox.accepted.connect(self.accepted)
    
    def accepted(self):
        self.date = self.ui.dateEdit.date()