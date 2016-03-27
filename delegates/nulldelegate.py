from PyQt5 import QtWidgets

class NullDelegate(QtWidgets.QItemDelegate):
    def __init__(self, parent = None):
        super().__init__(parent)
    
    def setEditorData(self, editor, index):
        editor.setProperty("text", index.data());
    
    def setModelData(self, editor, model, index):
        text = editor.property("text").strip()
        if text == "":
            print("NULL")
            model.setData(index, None)
        else:
            print("NOT NULL")
            model.setData(index, text)