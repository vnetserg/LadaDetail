#!/usr/bin/python3.4
# -*- coding: utf-8 -*-

import sys
from PyQt5 import QtWidgets, QtGui

from dialogs.logindialog import LoginDialog

def main():
    # Точка входа
    app = QtWidgets.QApplication(sys.argv)

    # Правим шрифт:
    font = QtWidgets.QApplication.font();
    font.setStyleStrategy(QtGui.QFont.PreferAntialias);
    QtWidgets.QApplication.setFont(font);

    # Создаём окно:
    window = LoginDialog()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()