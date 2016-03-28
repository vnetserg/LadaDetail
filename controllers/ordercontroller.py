# -*- coding: utf-8 -*-

from PyQt5.QtCore import QObject, Qt
from PyQt5.QtSql import QSqlQueryModel, QSqlQuery
from PyQt5.QtWidgets import QInputDialog

class OrderController(QObject):
    def __init__(self, form, orderTable, addButton, editButton, deleteButton, dbase):
        super().__init__()
        self.form = form
        self.orderTable = orderTable
        self.addButton = addButton
        self.editButton = editButton
        self.deleteButton = deleteButton
        self.dbase = dbase

        form.currentRecordChanged.connect(self.recordChanged)

        self.addButton.clicked.connect(self.addButtonClicked)
        self.editButton.clicked.connect(self.editButtonClicked)
        self.deleteButton.clicked.connect(self.deleteButtonClicked)

    def recordChanged(self, record):
        if record is None:
            for button in (self.addButton, self.editButton, self.deleteButton):
                button.setEnabled(False)
            self.orderTable.setModel(None)
        else:
            self.addButton.setEnabled(True)
            self.detailModel = QSqlQueryModel()
            query = "SELECT detail.id as id, CONCAT(detail.article, \": \", detail.name) as dtl, order_detail.quantity as qnt \
                FROM order_detail INNER JOIN detail \
                ON order_detail.detail_id = detail.id \
                WHERE order_detail.order_id={} ORDER BY dtl".format(record.value("id"))
            self.detailModel.setQuery(query)
            self.detailModel.setHeaderData(1, Qt.Horizontal, "Наименование")
            self.detailModel.setHeaderData(2, Qt.Horizontal, "Количество")
            self.orderTable.setModel(self.detailModel)
            self.orderTable.hideColumn(0)
            self.orderTable.resizeColumnsToContents()
            self.orderTable.selectionModel().currentChanged.connect(self.tableSelectionChanged)
            if not self.detailModel.query().isActive():
                print(self.detailModel.lastError().text())
            self.deleteButton.setEnabled(False)
            self.editButton.setEnabled(False)

    def tableSelectionChanged(self, cur, prev):
        if cur.isValid():
            self.deleteButton.setEnabled(True)
            self.editButton.setEnabled(True)
        else:
            self.deleteButton.setEnabled(False)
            self.editButton.setEnabled(False)
        self.addButton.setEnabled(True)

    def addButtonClicked(self):
        order = self.form.currentRecord()
        query = QSqlQuery("SELECT detail.id as id, CONCAT(detail.article, \": \", detail.name) as name \
            FROM detail WHERE NOT(detail.id IN (SELECT detail_id FROM order_detail \
                WHERE order_id={}))".format(order.value("id")))
        details = {}
        while query.next():
            details[query.value("name")] = query.value("id")
        if not details:
            return QMessageBox.warning(None, "Ошибка добавления",
                "Не удалось добавить новый товар к заказу: все возможные товары уже добавлены.")
        choice, ok = QInputDialog.getItem(None, "Товар", "Укажите товар:",
            list(details.keys()), 0, False)
        if not ok: return
        qnt, ok = QInputDialog.getInt(None, "Количество", "Укажите количество товара:", 1, 1)
        if not ok: return
        detail_id = details[choice]
        order_id = order.value("id")
        query = QSqlQuery("INSERT INTO order_detail (order_id, detail_id, quantity) \
            VALUES ({}, {}, {})".format(order_id, detail_id, qnt))
        query.exec_()
        if not query.isActive():
            print(query.lastError().text())
        self.form.update()

    def editButtonClicked(self):
        detail = self.detailModel.record(self.orderTable.currentIndex().row())
        qnt, ok = QInputDialog.getInt(None, "Количество", "Укажите количество товара:",
            detail.value("qnt"), 0)
        if not ok: return
        order = self.form.currentRecord()
        if qnt > 0:
            query = QSqlQuery("UPDATE order_detail SET quantity={} \
                WHERE order_id={} AND detail_id={}".format(qnt,
                    order.value("id"), detail.value("id")))
        else:
            query = QSqlQuery("DELETE FROM order_detail WHERE \
                order_id={} AND detail_id={} LIMIT 1".format(
                    order.value("id"), detail.value("id")))
        query.exec_()
        if not query.isActive():
            print(query.lastError().text())
        self.form.update()

    def deleteButtonClicked(self):
        if not self.orderTable.currentIndex().isValid(): return
        detail = self.detailModel.record(self.orderTable.currentIndex().row())
        order = self.form.currentRecord()
        query = QSqlQuery("DELETE FROM order_detail WHERE \
            order_id={} AND detail_id={} LIMIT 1".format(
                order.value("id"), detail.value("id")))
        query.exec_()
        if not query.isActive():
            print(query.lastError().text())
        self.form.update()

    def selectRow(self, row):
        self.form.selectRow(row)

    def update(self):
        self.form.update()