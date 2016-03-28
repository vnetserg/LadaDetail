# -*- coding: utf-8 -*-

from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import QLabel, QPushButton, QFileDialog

from .genericformcontroller import GenericFormController

class PhotoFormController(GenericFormController):
    def __init__(self, *args, **kwarg):
        self._photoLabels = []
        self._browsePhotoButton = None
        self._deletePhotoButton = None
        self._currentImage = None
        self._photoColumn = None
        super().__init__(*args, **kwarg)

    def addWidget(self, widget, role, **kw):
        if role == "photo" and isinstance(widget, QLabel):
            self._photoLabels.append(widget)
            self._photoColumn = kw["column"]
        elif role == "browse_photo" and isinstance(widget, QPushButton):
            self._browsePhotoButton = widget
            widget.clicked.connect(self._browsePhotoPressed)
        elif role == "delete_photo" and isinstance(widget, QPushButton):
            self._deletePhotoButton = widget
            widget.clicked.connect(self._deletePhotoPressed)
        else:
            super().addWidget(widget, role, **kw)

    def _selectionChanged(self, cur, prev):
        if cur.isValid():
            row = cur.row()
            filename = self.model.record(row).value(self._photoColumn)
            self._setPhoto(filename)
        super()._selectionChanged(cur, prev)

    def _recordPostprocess(self, record):
        record.setValue(self._photoColumn, self._currentImage)

    def _browsePhotoPressed(self):
        filename = QFileDialog.getOpenFileName(None, u'Открыть', filter = u"Изображение (*.jpg *.jpeg *.gif *.bmp *.png)")[0]
        if filename:
            self._currentImage = filename
            self._setPhoto(filename)

    def _deletePhotoPressed(self):
        self._currentImage = None
        self._setPhoto(None)

    def _setPhoto(self, filename):
        for label in self._photoLabels:
            w, h = label.width(), label.height()
            pixmap = QtGui.QPixmap(filename)
            if not pixmap.isNull():
                label.setPixmap(pixmap.scaled(w, h, QtCore.Qt.KeepAspectRatio))
            else:
                label.setPixmap(pixmap)

    def _clearAll(self):
        self._setPhoto(None)
        super()._clearAll()