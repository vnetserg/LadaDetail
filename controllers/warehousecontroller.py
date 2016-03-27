# -*- coding: utf-8 -*-

from PyQt5.QtCore import QObject, Qt
from PyQt5.QtSql import QSqlTableModel, QSqlQueryModel, QSqlQuery
from PyQt5.QtWidgets import QInputDialog, QMessageBox

from models.complexlistmodel import ComplexListModel

class WarehouseController(QObject):
    def __init__(self, list, table, addButton, editButton, deleteButton, dbase):
        super().__init__()
        self.list = list
        self.table = table
        self.addButton = addButton
        self.editButton = editButton
        self.deleteButton = deleteButton
        self.dbase = dbase

        self.shopModel = QSqlTableModel(db = dbase)
        self.shopModel.setTable("shop")
        self.shopModel.select()
        self.list.setModel(ComplexListModel(self.shopModel, "{name}"))
        self.list.selectionModel().currentChanged.connect(self.listSelectionChanged)

        self.addButton.clicked.connect(self.addButtonClicked)
        self.editButton.clicked.connect(self.editButtonClicked)
        self.deleteButton.clicked.connect(self.deleteButtonClicked)

    def listSelectionChanged(self, cur, prev):
        if not cur.isValid():
            return self.table.setModel(None)
        else:
            self.setShopIndex(cur.row())

    def setShopIndex(self, row):
        record = self.shopModel.record(row)
        self.detailModel = QSqlQueryModel()
        query = "SELECT detail.id as id, CONCAT(detail.article, \": \", detail.name) as dtl, shop_detail.quantity as qnt \
            FROM shop_detail INNER JOIN detail \
            ON shop_detail.detail_id = detail.id \
            WHERE shop_detail.shop_id={} ORDER BY dtl".format(record.value("id"))
        self.detailModel.setQuery(query)
        self.detailModel.setHeaderData(1, Qt.Horizontal, "Наименование")
        self.detailModel.setHeaderData(2, Qt.Horizontal, "Количество")
        self.table.setModel(self.detailModel)
        self.table.hideColumn(0)
        self.table.resizeColumnsToContents()
        self.table.selectionModel().currentChanged.connect(self.tableSelectionChanged)
        if not self.detailModel.query().isActive():
            print(self.detailModel.lastError().text())

    def tableSelectionChanged(self, cur, prev):
        if cur.isValid():
            self.deleteButton.setEnabled(True)
            self.editButton.setEnabled(True)
        else:
            self.deleteButton.setEnabled(False)
            self.editButton.setEnabled(False)
        self.addButton.setEnabled(True)

    def addButtonClicked(self):
        shop = self.shopModel.record(self.list.currentIndex().row())
        query = QSqlQuery("SELECT detail.id as id, CONCAT(detail.article, \": \", detail.name) as name \
            FROM detail WHERE NOT(detail.id IN (SELECT detail_id FROM shop_detail \
                WHERE shop_id={}))".format(shop.value("id")))
        details = {}
        while query.next():
            details[query.value("name")] = query.value("id")
        if not details:
            return QMessageBox.warning(None, "Ошибка добавления",
                "Не удалось добавить новый товар на склад: все возможные товары уже добавлены.")
        choice, ok = QInputDialog.getItem(None, "Товар", "Укажите товар:",
            list(details.keys()), 0, False)
        if not ok: return
        qnt, ok = QInputDialog.getInt(None, "Количество", "Укажите количество товара:",
            1, 1)
        if not ok: return
        detail_id = details[choice]
        shop_id = shop.value("id")
        query = QSqlQuery("INSERT INTO shop_detail (shop_id, detail_id, quantity) \
            VALUES ({}, {}, {})".format(shop_id, detail_id, qnt))
        query.exec_()
        if not query.isActive():
            print(query.lastError().text())
        self.setShopIndex(self.list.currentIndex().row())

        if len(details) == 1:
            self.addButton.setEnabled(False)

    def editButtonClicked(self):
        detail = self.detailModel.record(self.table.currentIndex().row())
        qnt, ok = QInputDialog.getInt(None, "Количество", "Укажите количество товара:",
            detail.value("qnt"), 0)
        if not ok: return
        shop = self.shopModel.record(self.list.currentIndex().row())
        if qnt > 0:
            query = QSqlQuery("UPDATE shop_detail SET quantity={} \
                WHERE shop_id={} AND detail_id={}".format(qnt,
                    shop.value("id"), detail.value("id")))
        else:
            query = QSqlQuery("DELETE FROM shop_detail WHERE \
                shop_id={} AND detail_id={} LIMIT 1".format(
                    shop.value("id"), detail.value("id")))
        query.exec_()
        if not query.isActive():
            print(query.lastError().text())
        self.setShopIndex(self.list.currentIndex().row())

    def deleteButtonClicked(self):
        if not self.table.currentIndex().isValid(): return
        detail = self.detailModel.record(self.table.currentIndex().row())
        shop = self.shopModel.record(self.list.currentIndex().row())
        query = QSqlQuery("DELETE FROM shop_detail WHERE \
            shop_id={} AND detail_id={} LIMIT 1".format(
                shop.value("id"), detail.value("id")))
        query.exec_()
        if not query.isActive():
            print(query.lastError().text())
        self.setShopIndex(self.list.currentIndex().row())

    def update(self):
        self.shopModel.select()
        self.list.reset()