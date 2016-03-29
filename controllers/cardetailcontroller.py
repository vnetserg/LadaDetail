# -*- coding: utf-8 -*-

from PyQt5.QtCore import QObject, Qt, QItemSelectionModel
from PyQt5.QtSql import QSqlTableModel, QSqlQueryModel, QSqlQuery
from PyQt5.QtWidgets import QInputDialog, QMessageBox

from models.complexlistmodel import ComplexListModel

class CarDetailController(QObject):
    def __init__(self, carList, detailList, addButton, deleteButton, dbase):
        super().__init__()
        self.carList = carList
        self.detailList = detailList
        self.addButton = addButton
        self.deleteButton = deleteButton
        self.dbase = dbase

        self.carModel = QSqlTableModel(db = dbase)
        self.carModel.setTable("car")
        self.carModel.select()
        self.carList.setModel(ComplexListModel(self.carModel, "{name}"))
        self.carList.selectionModel().currentChanged.connect(self.carListSelectionChanged)

        self._checkPrivileges()
        if self.only_select:
            self.addButton.setEnabled(False)
            self.deleteButton.setEnabled(False)

        self.addButton.clicked.connect(self.addButtonClicked)
        self.deleteButton.clicked.connect(self.deleteButtonClicked)

    def _checkPrivileges(self):
        query = QSqlQuery("SHOW GRANTS")
        only_select = None
        table_pattern = "`{}`".format("car_detail").lower()
        while query.next():
            s = query.value(0).lower()
            if table_pattern in s:
                if "select" in s and only_select is None:
                    only_select = True
                else:
                    only_select = False
        self.only_select = bool(only_select)

    def carListSelectionChanged(self, cur, prev):
        if not cur.isValid():
            return self.detailList.setModel(None)
        else:
            self.setCarIndex(cur.row())

    def setCarIndex(self, row):
        record = self.carModel.record(row)
        self.detailModel = QSqlQueryModel()
        query = "SELECT CONCAT(detail.article, \": \", detail.name) as dtl, detail.id as id \
            FROM car_detail INNER JOIN detail \
            ON car_detail.detail_id = detail.id \
            WHERE car_detail.car_id={} ORDER BY dtl".format(record.value("id"))
        self.detailModel.setQuery(query)
        self.detailList.setModel(self.detailModel)
        #self.detailList.hideColumn(1)
        #self.detailList.resizeColumnsToContents()
        self.detailList.selectionModel().currentChanged.connect(self.detailListSelectionChanged)
        if not self.detailModel.query().isActive():
            print(self.detailModel.lastError().text())
        self.deleteButton.setEnabled(False)

    def detailListSelectionChanged(self, cur, prev):
        if self.only_select: return
        if cur.isValid():
            self.deleteButton.setEnabled(True)
        else:
            self.deleteButton.setEnabled(False)
        self.addButton.setEnabled(True)

    def addButtonClicked(self):
        car = self.carModel.record(self.carList.currentIndex().row())
        query = QSqlQuery("SELECT detail.id as id, CONCAT(detail.article, \": \", detail.name) as name \
            FROM detail WHERE NOT(detail.id IN (SELECT detail_id FROM car_detail \
                WHERE car_id={}))".format(car.value("id")))
        details = {}
        while query.next():
            details[query.value("name")] = query.value("id")
        if not details:
            return QMessageBox.warning(None, "Ошибка добавления",
                "Не удалось добавить запчасть к машине: все возможные запчасти уже добавлены.")
        choice, ok = QInputDialog.getItem(None, "Товар", "Укажите товар:",
            list(details.keys()), 0, False)
        if not ok: return
        detail_id = details[choice]
        car_id = car.value("id")
        uery = QSqlQuery("INSERT INTO car_detail (car_id, detail_id) \
            VALUES ({}, {})".format(car_id, detail_id))
        if not query.isActive():
            print(query.lastError().text())
        self.setCarIndex(self.carList.currentIndex().row())
        self.detailList.selectionModel().clearSelection()

    def deleteButtonClicked(self):
        if not self.detailList.currentIndex().isValid(): return
        detail = self.detailModel.record(self.detailList.currentIndex().row())
        car = self.carModel.record(self.carList.currentIndex().row())
        query = QSqlQuery("DELETE FROM car_detail WHERE \
            car_id={} AND detail_id={} LIMIT 1".format(
                car.value("id"), detail.value("id")))
        if not query.isActive():
            print(query.lastError().text())
        self.setCarIndex(self.carList.currentIndex().row())

    def selectRow(self, row):
        self.carList.selectionModel().clearSelection()
        self.carList.selectionModel().setCurrentIndex(
            self.carModel.index(row, 0), QItemSelectionModel.Select)

    def update(self):
        cur = self.carList.currentIndex()
        if cur.isValid():
            row = cur.row()
        else:
            row = 0
        self.carModel.select()
        self.carList.reset()
        self.selectRow(row)