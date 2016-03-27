# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QSpinBox, QLabel, QComboBox
from PyQt5.QtSql import QSqlQuery

from .genericformcontroller import GenericFormController

class ForeignFormController(GenericFormController):
    def __init__(self, *arg, **kw):
        self._sources = {}
        self._proxyDisplays = {}
        self._proxyEdits = {}
        super().__init__(*arg, **kw)

    def addWidget(self, widget, role, **kw):
        if role.startswith("proxy_"):
            source = kw["source"]
            assert isinstance(source, QSpinBox)
            if source not in self._sources:
                self._sources[source] = {"table": kw["table"], "column": kw["column"]}
                source.valueChanged.connect(lambda value: self._sourceChanged(source, value))
            if role == "proxy_display" and isinstance(widget, QLabel):
                if source not in self._proxyDisplays:
                    self._proxyDisplays[source] = []
                self._proxyDisplays[source].append({"widget": widget, "format": kw["format"]})
            elif role == "proxy_edit" and isinstance(widget, QComboBox):
                if source not in self._proxyEdits:
                    self._proxyEdits[source] = []
                self._proxyEdits[source].append({"widget": widget, "format": kw["format"]})
                widget.currentIndexChanged.connect(lambda index: self._proxyChanged(widget, source, index))
                self._updateSourceRecords(source)
            else:
                super().addWidget(widget, role, **kw)
        else:
            super().addWidget(widget, role, **kw)

    def _sourceChanged(self, source, value):  
        record = None
        for index, record in enumerate(self._sources[source]["records"]):
            if record.value(self._sources[source]["column"]) == value:
                break
        if record is None: return

        values = {record.field(i).name(): record.value(i) for i in range(record.count())}
        for display in self._proxyDisplays[source]:
            display["widget"].setText(display["format"].format(**values))

        for edit in self._proxyEdits[source]:
            if edit["widget"].currentIndex() != index:
                edit["widget"].setCurrentIndex(index)

    def _proxyChanged(self, proxy, source, index):
        record = self._sources[source]["records"][index]
        value = record.value(self._sources[source]["column"])
        if source.value() != value:
            source.setValue(value)

    def _updateSourceRecords(self, source):
        table = self._sources[source]["table"]
        query = QSqlQuery("SELECT * FROM {}".format(table), self.dbase)
        self._sources[source]["records"] = []
        while query.next():
            self._sources[source]["records"].append(query.record())
        for edit in self._proxyEdits[source]:
            edit["widget"].clear()
            for index, record in enumerate(self._sources[source]["records"]):
                values = {record.field(i).name(): record.value(i) for i in range(record.count())}
                edit["widget"].insertItem(edit["widget"].count(), edit["format"].format(**values))
                if record.value(self._sources[source]["column"]) == source.value():
                    edit["widget"].setCurrentIndex(index)
        
    def updateSources(self):
        for source in self._sources.keys():
            self._sourceChanged(source, source.value())

    def _clearAll(self):
        super()._clearAll()
        for source in self._sources.keys():
            source.setValue(self._sources[source]["records"][0].value(self._sources[source]["column"]))
            #for display in self._proxyDisplays[source]:
            #    display["widget"].setText("")

    def _doCommit(self):
        super()._doCommit()
        