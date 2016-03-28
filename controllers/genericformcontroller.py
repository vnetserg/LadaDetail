# -*- coding: utf-8 -*-

from itertools import chain

from PyQt5.QtWidgets import QDataWidgetMapper, QListView, QLabel, QPushButton, \
    QLineEdit, QTextEdit, QDateEdit, QPlainTextEdit, QMessageBox, QSpinBox
from PyQt5.QtSql import QSqlTableModel, QSqlRecord
from PyQt5.QtCore import QObject, pyqtSignal, QModelIndex, \
    QItemSelectionModel, QDate

from models.complexlistmodel import ComplexListModel

class GenericFormController(QObject):
    currentRecordChanged = pyqtSignal(object)
    recordInserted = pyqtSignal()
    recordCommitted = pyqtSignal()
    recordRollbacked = pyqtSignal()
    recordDeleted = pyqtSignal()

    def __init__(self, tablename, dbase, *widgets):
        super().__init__()
        self._rebuildArgs = (tablename, dbase) + widgets
        self.tablename = tablename
        self.dbase = dbase

        self.model = QSqlTableModel(db = dbase)
        self.model.setTable(tablename)
        self.model.select()
        self.mapper = QDataWidgetMapper()
        self.mapper.setModel(self.model)
        self.mapper.setSubmitPolicy(QDataWidgetMapper.ManualSubmit)

        record = self.model.record()
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
            self.selectRow(0)

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
        else:
            raise ValueError("Unknown widget: {} (role '{}')".format(
                widget.__class__.__name__, role))

    def recordsCount(self):
        return self.model.rowCount()

    def _selectionChanged(self, cur, prev = None):
        if cur.isValid():
            self.mapper.setCurrentModelIndex(self.model.index(cur.row(), cur.column()))
            self._deleteButton.setEnabled(True)
            self.currentRecordChanged.emit(self.model.record(cur.row()))
        else:
            self._deleteButton.setEnabled(False)
            self._clearAll()
            self.currentRecordChanged.emit(None)

    def _doCommit(self):
        if self._insertionMode is False:
            ind = self.mapper.currentIndex()
            record = self._getRecord()
            old_record = self.model.record(ind)
            record.setValue("id", old_record.value("id"))
            if self.model.setRecord(ind, record):
                self.model.submitAll()
                self.model.select()
                self.recordCommitted.emit()
                self._view.reset()
                self.selectRow(ind)
            else:
                print("Commit error:", self.model.lastError().text())
                QMessageBox.critical(None, "Ошибка редактирования",
                    "Не удалось внести данные в таблицу: не все обязательные поля заполнены.")
        else:
            row = self.model.rowCount()
            self._view.model().beginInsertRows(QModelIndex(), row, row)
            res = self._appendCurrent()
            self._view.model().endInsertRows()
            if res:
                self._insertionMode = False
                self.model.submitAll()
                self.model.select()
                self.selectRow(row)
                self.recordCommitted.emit()
                for i in range(self.model.rowCount()):
                    self._view.setRowHidden(i, False)

    def _doRollback(self):
        self.mapper.revert()
        if self._insertionMode is True:
            self._insertionMode = False
            self.selectRow(0)
        self.recordRollbacked.emit()

    def _doDelete(self):
        row = self._view.selectionModel().currentIndex().row()
        self.model.removeRow(row)
        self._view.setRowHidden(row, True)
        self.recordDeleted.emit()
        for i in chain(range(row-1, -1, -1), range(row+1, self.model.rowCount())):
            if not self._view.isRowHidden(i):
                return self.selectRow(i)
        self._deleteButton.setEnabled(False)
        self._clearAll()
    
    def _doInsert(self):
        errText = self._insertPossible()
        if errText:
            return QMessageBox.critical(None, "Ошибка добавления", errText)
        self._insertionMode = True
        self._view.selectionModel().clearSelection()
        self._clearAll()
        self.recordInserted.emit()

    def _insertPossible(self):
        return False

    def _getRecord(self):
        record = QSqlRecord()
        for i, col in sorted((i, col) for col, i in self._columns.items()):
            record.append(self.model.record().field(i))
            if col in self._edits:
                record.setValue(i, self._getWidgetValue(self._edits[col]))
            else:
                record.setValue(i, None)
        self._recordPostprocess(record)
        return record

    def _appendCurrent(self):
        record = self._getRecord()
        if not self.model.insertRecord(-1, record):
            print("Append error:", self.model.lastError().text())
            QMessageBox.critical(None, "Ошибка редактирования",
                "Не удалось внести данные в таблицу: не все обязательные поля заполнены.")
            return False
        return True

    def _recordPostprocess(self, record):
        # Для переопределения в потомках
        pass

    def _clearAll(self):
        for widget in chain(self._displays, self._edits.values()):
            self._clearWidget(widget)

    def _clearWidget(self, widget):
        if isinstance(widget, QLabel) or isinstance(widget, QLineEdit):
            widget.setText("")
        elif isinstance(widget, QTextEdit) or isinstance(widget, QPlainTextEdit):
            widget.setPlainText("")
        elif isinstance(widget, QDateEdit):
            widget.setDate(QDate.currentDate())
        elif isinstance(widget, QSpinBox):
            widget.setValue(0)
        else:
            raise ValueError("Unknown widget type: {}".format(widget.__class__.__name__))

    def _getWidgetValue(self, widget):
        if isinstance(widget, QLabel) or isinstance(widget, QLineEdit):
            text = widget.text()
        elif isinstance(widget, QTextEdit) or isinstance(widget, QPlainTextEdit):
            text = widget.toPlainText()
        elif isinstance(widget, QDateEdit):
            return widget.date()
        elif isinstance(widget, QSpinBox):
            return widget.value()
        else:
            raise ValueError("Unknown widget type: {}".format(widget.__class__.__name__))
        text = text.strip()
        if not text:
            return None
        return text

    def update(self):
        cur = self._view.currentIndex()
        if cur.isValid():
            row = cur.row()
        else:
            row = 0
        self.model.select()
        for i in range(self.model.rowCount()):
            self._view.setRowHidden(i, False)
        self.selectRow(row)

    def selectRow(self, row):
        self._view.selectionModel().clearSelection()
        if self.model.rowCount():
            self._view.selectionModel().setCurrentIndex(
                self.model.index(row, 0), QItemSelectionModel.Select)
        else:
            self._selectionChanged(QModelIndex(), QModelIndex())

    def currentRecord(self):
        cur = self._view.currentIndex()
        if cur.isValid():
            return self.model.record(cur.row())
        else:
            return None