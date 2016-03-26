# -*- coding: utf-8 -*-

from PyQt5 import QtWidgets

from ui.ui_mainwindow import Ui_MainWindow
from util import get_icon
from controllers.genericformcontroller import GenericFormController

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, dbase, parent = None):
        super(MainWindow, self).__init__(parent)
        self.dbase = dbase
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.configUI()

    def configUI(self):
        # Устанавливаем иконки к действиям:
        self.setWindowIcon(get_icon("appicon"))
        self.ui.view_clients.setIcon(get_icon("customer"))
        self.ui.view_employees.setIcon(get_icon("employee"))
        self.ui.view_shops.setIcon(get_icon("shop"))
        self.ui.view_details.setIcon(get_icon("detail"))
        self.ui.view_cars.setIcon(get_icon("car"))
        self.ui.view_warehouse.setIcon(get_icon("warehouse"))
        self.ui.view_cardetails.setIcon(get_icon("cardetails"))
        self.ui.view_orders.setIcon(get_icon("order"))
        # Форма "Клиенты":
        self._clientForm = GenericFormController("customer", self.dbase,
            {"widget": self.ui.clientListView, "role": "view",
                "format": "{lastname} {firstname:.1}. {middlename:.1}."},
            {"widget": self.ui.clientAddButton, "role": "insert"},
            {"widget": self.ui.clientDeleteButton, "role": "delete"},
            {"widget": self.ui.clientSaveButton, "role": "commit"},
            {"widget": self.ui.clientCancelButton, "role": "rollback"},
            {"widget": self.ui.clientFirstnameLabel, "role": "display",
                "column": "firstname"},
            {"widget": self.ui.clientLastnameLabel, "role": "display",
                "column": "lastname"},
            {"widget": self.ui.clientMiddlenameLabel, "role": "display",
                "column": "middlename"},
            {"widget": self.ui.clientBirthdateLabel, "role": "display",
                "column": "birthdate"},
            {"widget": self.ui.clientRegdateLabel, "role": "display",
                "column": "regdate"},
            {"widget": self.ui.clientEmailLabel, "role": "display",
                "column": "email"},
            {"widget": self.ui.clientPhoneLabel, "role": "display",
                "column": "phone"},
            {"widget": self.ui.clientPassportLabel, "role": "display",
                "column": "passport"},
            {"widget": self.ui.clientFirstnameEdit, "role": "edit",
                "column": "firstname"},
            {"widget": self.ui.clientLastnameEdit, "role": "edit",
                "column": "lastname"},
            {"widget": self.ui.clientMiddlenameEdit, "role": "edit",
                "column": "middlename"},
            {"widget": self.ui.clientBirthdateEdit, "role": "edit",
                "column": "birthdate"},
            {"widget": self.ui.clientRegdateEdit, "role": "edit",
                "column": "regdate"},
            {"widget": self.ui.clientEmailEdit, "role": "edit",
                "column": "email"},
            {"widget": self.ui.clientPhoneEdit, "role": "edit",
                "column": "phone"},
            {"widget": self.ui.clientPassportEdit, "role": "edit",
                "column": "passport"}
        )
        self._clientForm.currentRecordChanged.connect(
            lambda: self.ui.clientEditButton.setEnabled(True))
        self._clientForm.recordDeleted.connect(
            lambda: self.ui.clientEditButton.setEnabled(False))
        self._clientForm.recordInserted.connect(
            lambda: self.ui.clientStack.setCurrentWidget(self.ui.clientWritePage))
        self._clientForm.recordCommitted.connect(
            lambda: self.ui.clientStack.setCurrentWidget(self.ui.clientReadPage))
        self._clientForm.recordRollbacked.connect(
            lambda: self.ui.clientStack.setCurrentWidget(self.ui.clientReadPage))
        self.ui.clientEditButton.clicked.connect(
            lambda: self.ui.clientStack.setCurrentWidget(self.ui.clientWritePage))
        
        if self._clientForm.recordsCount() > 0:
            self.ui.clientEditButton.setEnabled(True)
        else:
            self.ui.clientEditButton.setEnabled(False)