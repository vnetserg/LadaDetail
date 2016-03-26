# -*- coding: utf-8 -*-

from PyQt5 import QtWidgets, QtSql
from ui.ui_logindialog import Ui_LoginDialog
from sqlalchemy.exc import OperationalError

from util import save_data, load_data, get_icon
from dialogs.mainwindow import MainWindow

class LoginDialog(QtWidgets.QDialog):
    def __init__(self, parent = None):
        super(LoginDialog, self).__init__(parent)
        self.ui = Ui_LoginDialog()
        self.ui.setupUi(self)
        self.setWindowIcon(get_icon("appicon"))
        self.ui.buttonBox.accepted.connect(self.accepted)
        self.loadText()
    
    def loadText(self):
        login, password, dbname = load_data()
        self.ui.loginEdit.setText(login)
        self.ui.passwordEdit.setText(password)
        self.ui.dbEdit.setText(dbname)
        self.ui.rememberPassword.setChecked(bool(password))
        if login:
            self.ui.passwordEdit.setFocus()
    
    def accepted(self):
        login = self.ui.loginEdit.text()
        password = self.ui.passwordEdit.text()
        dbname = self.ui.dbEdit.text()

        dbase = QtSql.QSqlDatabase.addDatabase("QMYSQL")
        dbase.setHostName("localhost")
        dbase.setDatabaseName(dbname)
        dbase.setUserName(login)
        dbase.setPassword(password)

        if not dbase.open():
            dbase.close()
            for name in QtSql.QSqlDatabase.connectionNames():
                QtSql.QSqlDatabase.removeDatabase(name)
            QtWidgets.QMessageBox.critical(self, "Ошибка авторизации", "Не удалось установить соединение с СУБД с заданными параметрами. Убедитесь, что СУБД запущена, а данные для входа введены верно.")
        else:
            LoginDialog.wnd = MainWindow(dbase)
            LoginDialog.wnd.show()
            password = password if self.ui.rememberPassword.isChecked() else ""
            save_data(login, password, dbname)
            self.accept()