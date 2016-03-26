# -*- coding: utf-8 -*-

from itertools import chain

from PyQt5.QtWidgets import QDataWidgetMapper, QListView, QLabel, QPushButton, \
    QLineEdit, QTextEdit, QDateEdit, QPlainTextEdit
from PyQt5.QtSql import QSqlRelationalTableModel, QSqlRecord
from PyQt5.QtCore import QObject, pyqtSignal, QModelIndex, \
    QItemSelectionModel

from models.complexlistmodel import ComplexListModel

class GenericFormController(QObject):
    currentRecordChanged = pyqtSignal()
    recordInserted = pyqtSignal()
    recordCommitted = pyqtSignal()
    recordRollbacked = pyqtSignal()
    recordDeleted = pyqtSignal()

    def __init__(self, tablename, dbase, *widgets):
        super().__init__()
        self.tablename = tablename
        self.dbase = dbase

        self.model = QSqlRelationalTableModel(db = dbase)
        self.model.setTable(tablename)
        self.model.select()
        self.mapper = QDataWidgetMapper()
        self.mapper.setModel(self.model)
        self.mapper.setSubmitPolicy(QDataWidgetMapper.ManualSubmit)

        record = self.model.record(0)
        self._columns = {record.field(i).name(): i for i in range(record.count())}
        
        self._view = None
        self._insertButton = None
        self._deleteButton = None
        self._commitButton = None
        self._rollbackButton = None

        self._displays = []
        self._edits = {}
        self._insertionMode = False

        for widget in widgets:
            self.addWidget(**widget)

        if self.model.rowCount() > 0:
            self._view.selectionModel().setCurrentIndex(
                self.model.index(0, 0), QItemSelectionModel.Select)

    def addWidget(self, widget, role, **kw):
        if role == "view" and isinstance(widget, QListView):
            self._view = widget
            widget.setModel(ComplexListModel(self.model, kw["format"]))
            widget.selectionModel().currentChanged.connect(self._selectionChanged)
        elif role == "display":
            self._displays.append(widget)
            self.mapper.addMapping(widget, self._columns[kw["column"]], "text")
        elif role == "edit":
            self._edits[kw["column"]] = widget
            self.mapper.addMapping(widget, self._columns[kw["column"]])
        elif role == "insert" and isinstance(widget, QPushButton):
            self._insertButton = widget
            widget.clicked.connect(self._doInsert)
        elif role == "delete" and isinstance(widget, QPushButton):
            self._deleteButton = widget
            widget.clicked.connect(self._doDelete)
        elif role == "commit" and isinstance(widget, QPushButton):
            self._commitButton = widget
            widget.clicked.connect(self._doCommit)
        elif role == "rollback" and isinstance(widget, QPushButton):
            self._rollbackButton = widget
            widget.clicked.connect(self._doRollback)

    def recordsCount(self):
        return self.model.rowCount()

    def _selectionChanged(self, cur, prev):
        if cur.isValid():
            self.mapper.setCurrentModelIndex(self.model.index(cur.row(), cur.column()))
            self._deleteButton.setEnabled(True)
        else:
            self._deleteButton.setEnabled(False)
        self.currentRecordChanged.emit()

    def _doCommit(self):
        if self._insertionMode is False:
            if self.mapper.submit():
                self.model.select()
                self.recordCommitted.emit()
            else:
                QtWidgets.QMessageBox.critical(self, "Ошибка редактирования",
                    "Не удалось внести данные в таблицу: не все обязательные поля заполнены.")
        else:
            self._insertionMode = False
            row = self.model.rowCount()
            self._view.model().beginInsertRows(QModelIndex(), row, row)
            self._appendCurrent()
            self._view.model().endInsertRows()
            self.recordCommitted.emit()
            self._view.selectionModel().clearSelection()
            self._view.selectionModel().setCurrentIndex(
                self.model.index(row, 0), QItemSelectionModel.Select)

    def _doRollback(self):
        self.mapper.revert()
        self.recordRollbacked.emit()

    def _doDelete(self):
        row = self._view.selectionModel().currentIndex().row()
        self.model.removeRow(row)
        self._view.setRowHidden(row, True)
        for i in chain(range(row-1, -1, -1), range(row+1, self.model.rowCount())):
            if not self._view.isRowHidden(i):
                self._view.selectionModel().setCurrentIndex(
                    self.model.index(i, 0), QItemSelectionModel.Select)
                return
        self._deleteButton.setEnabled(False)
        for widget in chain(self._displays, self._edits.values()):
            self._setWidgetText(widget, "")
    
    def _doInsert(self):
        self._insertionMode = True
        for widget in chain(self._displays, self._edits.values()):
            self._setWidgetText(widget, "")
        self.recordInserted.emit()
        '''
        row = self.model.rowCount()
        self._view.model().beginInsertRows(QModelIndex(), row, row)
        self.model.insertRows(row, 1)
        self._view.model().endInsertRows()
        self._view.selectionModel().setCurrentIndex(
            self.model.index(row, 0), QItemSelectionModel.Select)
        self._deleteButton.setEnabled(True)
        '''

    def _appendCurrent(self):
        record = QSqlRecord()
        for i, col in sorted((i, col) for col, i in self._columns.items()):
            record.append(self.model.record(0).field(i))
            if col in self._edits:
                record.setValue(i, self._getWidgetText(self._edits[col]))
            else:
                record.setValue(i, None)
        if not self.model.insertRecord(-1, record):
            print(self.model.lastError().text())
        self.model.submitAll()
        self.model.select()

    def _setWidgetText(self, widget, text):
        if isinstance(widget, QLabel) or isinstance(widget, QLineEdit):
            widget.setText(text)
        elif isinstance(widget, QTextEdit) or isinstance(widget, QPlainTextEdit):
            widget.setPlainText(text)
        elif isinstance(widget, QDateEdit):
            pass
        else:
            raise ValueError("Unknown widget type: {}".format(widget.__class__.__name__))

    def _getWidgetText(self, widget):
        if isinstance(widget, QLabel) or isinstance(widget, QLineEdit):
            return widget.text()
        elif isinstance(widget, QTextEdit) or isinstance(widget, QPlainTextEdit):
            return widget.toPlainText()
        elif isinstance(widget, QDateEdit):
            return widget.date().toString("YYYY-MM-dd")
        else:
            raise ValueError("Unknown widget type: {}".format(widget.__class__.__name__))