from PyQt5 import QtWidgets

class NullDelegate(QtWidgets.QStyledItemDelegate):
    def __init__(self, parent = None):
        super(NullDelegate).__init__(parent)
    
    '''
    def createEditor(self, parent, option, index):
        editor = QtWidgets.QWidget(parent)
        # ...configure editor if needed...
        return editor
    '''
    
    '''
    def setEditorData(self, editor, index):
        # ...set editor data...
    '''
    
    '''
    def setModelData(self, editor, model, index):
        model.setData(index, "data")
    '''