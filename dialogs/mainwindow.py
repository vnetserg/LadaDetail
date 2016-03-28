# -*- coding: utf-8 -*-

from PyQt5 import QtWidgets

from ui.ui_mainwindow import Ui_MainWindow
from util import get_icon
from controllers.genericformcontroller import GenericFormController
from controllers.photoformcontroller import PhotoFormController
from controllers.foreignformcontroller import ForeignFormController
from controllers.warehousecontroller import WarehouseController
from controllers.cardetailcontroller import CarDetailController
from controllers.ordercontroller import OrderController

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
        # Настраиваем переключение форм:
        actions = [self.ui.view_clients, self.ui.view_orders,
            self.ui.view_employees, self.ui.view_shops,
            self.ui.view_warehouse, self.ui.view_details,
            self.ui.view_cars, self.ui.view_cardetails]
        for act in actions:
            act.triggered.connect((lambda a: lambda: self.actionTriggered(a))(act))
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
        self.setupForm(self._clientForm, self.ui.clientEditButton, self.ui.clientStack,
            self.ui.clientReadPage, self.ui.clientWritePage)
        # Форма "Магазины":
        self._shopForm = GenericFormController("shop", self.dbase,
            {"widget": self.ui.shopListView, "role": "view",
                "format": "{name}"},
            {"widget": self.ui.shopAddButton, "role": "insert"},
            {"widget": self.ui.shopDeleteButton, "role": "delete"},
            {"widget": self.ui.shopSaveButton, "role": "commit"},
            {"widget": self.ui.shopCancelButton, "role": "rollback"},
            {"widget": self.ui.shopAddressLabel, "role": "display",
                "column": "address"},
            {"widget": self.ui.shopDescriptionLabel, "role": "display",
                "column": "description"},
            {"widget": self.ui.shopNameLabel, "role": "display",
                "column": "name"},
            {"widget": self.ui.shopPhoneLabel, "role": "display",
                "column": "phone"},
            {"widget": self.ui.shopDescriptionEdit, "role": "edit",
                "column": "description"},
            {"widget": self.ui.shopNameEdit, "role": "edit",
                "column": "name"},
            {"widget": self.ui.shopPhoneEdit, "role": "edit",
                "column": "phone"},
            {"widget": self.ui.shopAddressEdit, "role": "edit",
                "column": "address"},
        )
        self.setupForm(self._shopForm, self.ui.shopEditButton, self.ui.shopStack,
            self.ui.shopReadPage, self.ui.shopWritePage)
        # Форма "Машины":
        self._carForm = PhotoFormController("car", self.dbase,
            {"widget": self.ui.carListView, "role": "view",
                "format": "{name}"},
            {"widget": self.ui.carAddButton, "role": "insert"},
            {"widget": self.ui.carDeleteButton, "role": "delete"},
            {"widget": self.ui.carSaveButton, "role": "commit"},
            {"widget": self.ui.carCancelButton, "role": "rollback"},
            {"widget": self.ui.carDescriptionLabel, "role": "display",
                "column": "description"},
            {"widget": self.ui.carNameLabel, "role": "display",
                "column": "name"},
            {"widget": self.ui.carProddateLabel, "role": "display",
                "column": "proddate"},
            {"widget": self.ui.carDescriptionEdit, "role": "edit",
                "column": "description"},
            {"widget": self.ui.carNameEdit, "role": "edit",
                "column": "name"},
            {"widget": self.ui.carProddateEdit, "role": "edit",
                "column": "proddate"},
            {"widget": self.ui.carPhotoLabel, "role": "photo",
                "column": "photo"},
            {"widget": self.ui.carPhotoLabel_2, "role": "photo",
                "column": "photo"},
            {"widget": self.ui.carBrowsePhotoButton, "role": "browse_photo",
                "column": "photo"},
            {"widget": self.ui.carDeletePhotoButton, "role": "delete_photo",
                "column": "photo"}
        )
        self.setupForm(self._carForm, self.ui.carEditButton, self.ui.carStack,
            self.ui.carReadPage, self.ui.carWritePage)
        # Форма "Детали":
        self._detailForm = PhotoFormController("detail", self.dbase,
            {"widget": self.ui.detailListView, "role": "view",
                "format": "{article}: {name}"},
            {"widget": self.ui.detailAddButton, "role": "insert"},
            {"widget": self.ui.detailDeleteButton, "role": "delete"},
            {"widget": self.ui.detailSaveButton, "role": "commit"},
            {"widget": self.ui.detailCancelButton, "role": "rollback"},
            {"widget": self.ui.detailDescriptionLabel, "role": "display",
                "column": "description"},
            {"widget": self.ui.detailNameLabel, "role": "display",
                "column": "name"},
            {"widget": self.ui.detailArticleLabel, "role": "display",
                "column": "article"},
            {"widget": self.ui.detailCategoryLabel, "role": "display",
                "column": "category"},
            {"widget": self.ui.detailPriceLabel, "role": "display",
                "column": "price"},
            {"widget": self.ui.detailWarrantyLabel, "role": "display",
                "column": "warranty"},
            {"widget": self.ui.detailDescriptionEdit, "role": "edit",
                "column": "description"},
            {"widget": self.ui.detailNameEdit, "role": "edit",
                "column": "name"},
            {"widget": self.ui.detailArticleEdit, "role": "edit",
                "column": "article"},
            {"widget": self.ui.detailCategoryEdit, "role": "edit",
                "column": "category"},
            {"widget": self.ui.detailPriceEdit, "role": "edit",
                "column": "price"},
            {"widget": self.ui.detailWarrantyEdit, "role": "edit",
                "column": "warranty"},
            {"widget": self.ui.detailPhotoLabel, "role": "photo",
                "column": "photo"},
            {"widget": self.ui.detailPhotoLabel_2, "role": "photo",
                "column": "photo"},
            {"widget": self.ui.detailBrowsePhotoButton, "role": "browse_photo",
                "column": "photo"},
            {"widget": self.ui.detailDeletePhotoButton, "role": "delete_photo",
                "column": "photo"}
        )
        self.setupForm(self._detailForm, self.ui.detailEditButton, self.ui.detailStack,
            self.ui.detailReadPage, self.ui.detailWritePage)
        # Форма "Работники":
        self._empForm = ForeignFormController("employee", self.dbase,
            {"widget": self.ui.empListView, "role": "view",
                "format": "{lastname} {firstname:.1}. {middlename:.1}."},
            {"widget": self.ui.empAddButton, "role": "insert"},
            {"widget": self.ui.empDeleteButton, "role": "delete"},
            {"widget": self.ui.empSaveButton, "role": "commit"},
            {"widget": self.ui.empCancelButton, "role": "rollback"},
            {"widget": self.ui.empLastnameLabel, "role": "display",
                "column": "lastname"},
            {"widget": self.ui.empFirstnameLabel, "role": "display",
                "column": "firstname"},
            {"widget": self.ui.empMiddlenameLabel, "role": "display",
                "column": "middlename"},
            {"widget": self.ui.empBirthdateLabel, "role": "display",
                "column": "birthdate"},
            {"widget": self.ui.empDepartmentLabel, "role": "display",
                "column": "department"},
            {"widget": self.ui.empEmpdateLabel, "role": "display",
                "column": "empdate"},
            {"widget": self.ui.empPassportLabel, "role": "display",
                "column": "passport"},
            {"widget": self.ui.empPositionLabel, "role": "display",
                "column": "position"},
            {"widget": self.ui.empSalaryLabel, "role": "display",
                "column": "salary"},
            {"widget": self.ui.empLastnameEdit, "role": "edit",
                "column": "lastname"},
            {"widget": self.ui.empFirstnameEdit, "role": "edit",
                "column": "firstname"},
            {"widget": self.ui.empMiddlenameEdit, "role": "edit",
                "column": "middlename"},
            {"widget": self.ui.empBirthdateEdit, "role": "edit",
                "column": "birthdate"},
            {"widget": self.ui.empDepartmentEdit, "role": "edit",
                "column": "department"},
            {"widget": self.ui.empEmpdateEdit, "role": "edit",
                "column": "empdate"},
            {"widget": self.ui.empPassportEdit, "role": "edit",
                "column": "passport"},
            {"widget": self.ui.empPositionEdit, "role": "edit",
                "column": "position"},
            {"widget": self.ui.empSalaryEdit, "role": "edit",
                "column": "salary"},
            {"widget": self.ui.empShopEdit, "role": "edit",
                "column": "shop_id"},
            {"widget": self.ui.empShopProxyLabel, "role": "proxy_display",
                "source": self.ui.empShopEdit, "table": "shop",
                "column": "id", "format": "{name}"},
            {"widget": self.ui.empShopProxyCombo, "role": "proxy_edit",
                "source": self.ui.empShopEdit, "table": "shop",
                "column": "id", "format": "{name}"},
        )
        self.setupForm(self._empForm, self.ui.empEditButton, self.ui.empStack,
            self.ui.empReadPage, self.ui.empWritePage)
        # Форма "Склад":
        self._warehouseForm = WarehouseController(self.ui.warehouseShopView,
            self.ui.warehouseDetailView, self.ui.warehouseAddButton,
            self.ui.warehouseEditButton, self.ui.warehouseDeleteButton, self.dbase)
        # Форма "Запчасти машин":
        self._carDetailForm = CarDetailController(self.ui.carListView_2,
            self.ui.carDetailListView, self.ui.carDetailAddButton,
            self.ui.carDetailDeleteButton, self.dbase)
        # Форма "Заказы":
        orderForm = ForeignFormController("orders", self.dbase,
            {"widget": self.ui.orderListView, "role": "view",
                "format": "#{id}"},
            {"widget": self.ui.orderAddButton, "role": "insert"},
            {"widget": self.ui.orderDeleteButton, "role": "delete"},
            {"widget": self.ui.orderSaveButton, "role": "commit"},
            {"widget": self.ui.orderCancelButton, "role": "rollback"},
            {"widget": self.ui.orderDateLabel, "role": "display",
                "column": "regdate"},
            {"widget": self.ui.orderPriceLabel, "role": "display",
                "column": "price"},
            {"widget": self.ui.orderPriceLabel_2, "role": "display",
                "column": "price"},
            {"widget": self.ui.orderPriceSpin, "role": "edit",
                "column": "price"},
            {"widget": self.ui.orderClientSpin, "role": "edit",
                "column": "customer_id"},
            {"widget": self.ui.orderShopSpin, "role": "edit",
                "column": "shop_id"},
            {"widget": self.ui.orderEmpSpin, "role": "edit",
                "column": "employee_id"},
            {"widget": self.ui.orderDateEdit, "role": "edit",
                "column": "regdate"},

            {"widget": self.ui.orderClientLabel, "role": "proxy_display",
                "source": self.ui.orderClientSpin, "table": "customer",
                "column": "id", "format": "{lastname} {firstname:.1}. {middlename:.1}."},
            {"widget": self.ui.orderEmpLabel, "role": "proxy_display",
                "source": self.ui.orderEmpSpin, "table": "employee",
                "column": "id", "format": "{lastname} {firstname:.1}. {middlename:.1}."},
            {"widget": self.ui.orderShopLabel, "role": "proxy_display",
                "source": self.ui.orderShopSpin, "table": "shop",
                "column": "id", "format": "{name}"},

            {"widget": self.ui.orderClientCombo, "role": "proxy_edit",
                "source": self.ui.orderClientSpin, "table": "customer",
                "column": "id", "format": "{lastname} {firstname:.1}. {middlename:.1}."},
            {"widget": self.ui.orderEmpCombo, "role": "proxy_edit",
                "source": self.ui.orderEmpSpin, "table": "employee",
                "column": "id", "format": "{lastname} {firstname:.1}. {middlename:.1}."},
            {"widget": self.ui.orderShopCombo, "role": "proxy_edit",
                "source": self.ui.orderShopSpin, "table": "shop",
                "column": "id", "format": "{name}"},
        )
        self.setupForm(orderForm, self.ui.orderEditButton, self.ui.orderStack,
            self.ui.orderReadPage, self.ui.orderWritePage)
        self._orderForm = OrderController(orderForm, self.ui.orderDetailView,
            self.ui.orderDetailAddButton, self.ui.orderDetailEditButton,
            self.ui.orderDetailDeleteButton, self.dbase)

    def setupForm(self, form, editbutton, stack, readpage, writepage):
        form.currentRecordChanged.connect(
            lambda cur: editbutton.setEnabled(True))
        form.currentRecordChanged.connect(
            lambda cur: stack.setCurrentWidget(readpage))
        form.recordDeleted.connect(
            lambda: editbutton.setEnabled(False))
        form.recordInserted.connect(
            lambda: stack.setCurrentWidget(writepage))
        form.recordCommitted.connect(
            lambda: stack.setCurrentWidget(readpage))
        form.recordRollbacked.connect(
            lambda: stack.setCurrentWidget(readpage))
        editbutton.clicked.connect(
            lambda: stack.setCurrentWidget(writepage))
        if form.recordsCount() > 0:
            editbutton.setEnabled(True)
        else:
            editbutton.setEnabled(False)

    def actionTriggered(self, cur_action):
        mapping = {
            self.ui.view_clients: (self.ui.page_clients, self._clientForm),
            self.ui.view_orders: (self.ui.page_orders, self._orderForm),
            self.ui.view_employees: (self.ui.page_employees, self._empForm),
            self.ui.view_shops: (self.ui.page_shops, self._shopForm),
            self.ui.view_warehouse: (self.ui.page_warehouse, self._warehouseForm),
            self.ui.view_details: (self.ui.page_details, self._detailForm),
            self.ui.view_cars: (self.ui.page_cars, self._carForm),
            self.ui.view_cardetails: (self.ui.page_cardetails, self._carDetailForm)
        }
        for action in mapping.keys():
            action.setChecked(action == cur_action)
        page, form = mapping[cur_action]
        self.ui.stackedWidget.setCurrentWidget(page)
        if form:
            form.update()