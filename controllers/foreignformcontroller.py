# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QSpinBox, QLabel
from PyQt5.QtSql import QSqlQuery

from .genericformcontroller import GenericFormController

class ForeignFormController(GenericFormController):
    def __init__(self, *arg, **kw):
        self._sources = {}
        self._proxyDisplays = {}
        super().__init__(*arg, **kw)

    def addWidget(self, widget, role, **kw):
        if role == "proxy_display" and isinstance(widget, QLabel):
            source = kw["source"]
            assert isinstance(source, QSpinBox)
            if source not in self._sources:
                self._sources[source] = {"table": kw["table"], "column": kw["column"]}
            if source not in self._proxyDisplays:
                self._proxyDisplays[source] = []
            self._proxyDisplays[source].append({"widget": widget, "format": kw["format"]})
            source.valueChanged.connect(lambda value: self._sourceChanged(source, value))
        else:
            super().addWidget(widget, role, **kw)

    def _sourceChanged(self, source, value):
        table = self._sources[source]["table"]
        column = self._sources[source]["column"]
        query = QSqlQuery("SELECT * FROM {} WHERE {}={} LIMIT 1".format(table, column, value),
            self.dbase)
        if not query.next():
            return print("SQL error:", self.dbase.lastError().text())
        record = query.record()
        values = {record.field(i).name(): record.value(i) for i in range(record.count())}
        for display in self._proxyDisplays[source]:
            display["widget"].setText(display["format"].format(**values))
        
    def _updateSources(self):
        for source in self._sources.keys():
            self._sourceChanged(source, source.value())