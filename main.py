#!/usr/bin/python3.4
# -*- coding: utf-8 -*-

import sys
from PyQt5 import QtWidgets

from dialogs.logindialog import LoginDialog

def main():
    # Точка входа
    app = QtWidgets.QApplication(sys.argv)
    window = LoginDialog()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()