# -*- coding: utf-8 -*-

from PyQt5 import QtCore

class ComplexListModel(QtCore.QAbstractListModel):
    def __init__(self, model, format, parent = None):
        super(ComplexListModel, self).__init__(parent)
        self._model = model
        self.format = format
    
    def columnCount(self, index = None):
       return 1
    
    def rowCount(self, index = QtCore.QModelIndex()):
       return self._model.rowCount()
    
    def data(self, index, role = QtCore.Qt.DisplayRole):
        if role == QtCore.Qt.DisplayRole:
            record = self._model.record(index.row())
            return self.format.format(**{record.field(i).name(): str(record.field(i).value())
                for i in range(record.count())})
    
    def flags(self, index):
        if index.isValid():
            flags = QtCore.Qt.ItemIsEnabled \
                | QtCore.Qt.ItemIsSelectable
            return flags
