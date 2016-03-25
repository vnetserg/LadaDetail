# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/data/data/Code/Python/LadaDetail/forms/logindialog.ui'
#
# Created by: PyQt5 UI code generator 5.4.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_LoginDialog(object):
    def setupUi(self, LoginDialog):
        LoginDialog.setObjectName("LoginDialog")
        LoginDialog.resize(190, 142)
        self.gridLayout = QtWidgets.QGridLayout(LoginDialog)
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtWidgets.QLabel(LoginDialog)
        self.label.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.loginEdit = QtWidgets.QLineEdit(LoginDialog)
        self.loginEdit.setObjectName("loginEdit")
        self.gridLayout.addWidget(self.loginEdit, 0, 1, 1, 1)
        self.label_2 = QtWidgets.QLabel(LoginDialog)
        self.label_2.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.passwordEdit = QtWidgets.QLineEdit(LoginDialog)
        self.passwordEdit.setEchoMode(QtWidgets.QLineEdit.Password)
        self.passwordEdit.setObjectName("passwordEdit")
        self.gridLayout.addWidget(self.passwordEdit, 1, 1, 1, 1)
        self.label_3 = QtWidgets.QLabel(LoginDialog)
        self.label_3.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 3, 0, 1, 1)
        self.dbEdit = QtWidgets.QLineEdit(LoginDialog)
        self.dbEdit.setObjectName("dbEdit")
        self.gridLayout.addWidget(self.dbEdit, 3, 1, 1, 1)
        self.buttonBox = QtWidgets.QDialogButtonBox(LoginDialog)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout.addWidget(self.buttonBox, 4, 0, 1, 2)
        self.rememberPassword = QtWidgets.QCheckBox(LoginDialog)
        self.rememberPassword.setChecked(True)
        self.rememberPassword.setObjectName("rememberPassword")
        self.gridLayout.addWidget(self.rememberPassword, 2, 0, 1, 2)

        self.retranslateUi(LoginDialog)
        self.buttonBox.rejected.connect(LoginDialog.close)
        QtCore.QMetaObject.connectSlotsByName(LoginDialog)

    def retranslateUi(self, LoginDialog):
        _translate = QtCore.QCoreApplication.translate
        LoginDialog.setWindowTitle(_translate("LoginDialog", "Авторизация"))
        self.label.setText(_translate("LoginDialog", "Логин:"))
        self.label_2.setText(_translate("LoginDialog", "Пароль:"))
        self.label_3.setText(_translate("LoginDialog", "Имя БД:"))
        self.rememberPassword.setText(_translate("LoginDialog", "Запомнить пароль"))

