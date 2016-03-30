# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/data/data/Code/Python/LadaDetail/forms/getdate.ui'
#
# Created by: PyQt5 UI code generator 5.4.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_GetDate(object):
    def setupUi(self, GetDate):
        GetDate.setObjectName("GetDate")
        GetDate.resize(174, 86)
        self.verticalLayout = QtWidgets.QVBoxLayout(GetDate)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(GetDate)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.dateEdit = QtWidgets.QDateEdit(GetDate)
        self.dateEdit.setCalendarPopup(True)
        self.dateEdit.setObjectName("dateEdit")
        self.verticalLayout.addWidget(self.dateEdit)
        self.buttonBox = QtWidgets.QDialogButtonBox(GetDate)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(GetDate)
        self.buttonBox.accepted.connect(GetDate.accept)
        self.buttonBox.rejected.connect(GetDate.reject)
        QtCore.QMetaObject.connectSlotsByName(GetDate)

    def retranslateUi(self, GetDate):
        _translate = QtCore.QCoreApplication.translate
        GetDate.setWindowTitle(_translate("GetDate", "Ввод даты"))
        self.label.setText(_translate("GetDate", "Введите дату:"))

