from PySide6.QtGui import QStandardItemModel, QStandardItem
from PySide6.QtWidgets import (QVBoxLayout, QWidget, QGridLayout, 
                               QTreeView, QPushButton, QLineEdit,
                               QComboBox)

from bookkeeper.utils import read_tree
from bookkeeper.repository.memory_repository import MemoryRepository
from bookkeeper.models.category import Category


class CategoryEditorWindow(QWidget):
    def __init__(self, data):
        super(CategoryEditorWindow, self).__init__()
        self.layout = QVBoxLayout(self)
        self.tree = QTreeView(self)
        self.layout.addWidget(self.tree)
        
        self.bottom_controls = QGridLayout()
        self.model = None
        
        self.new_category_line_edit = QLineEdit()
        self.new_category_line_edit.setPlaceholderText('Новая категория')
        self.bottom_controls.addWidget(self.new_category_line_edit, 0, 0)
        
        self.category_dropdown = QComboBox()
        self.bottom_controls.addWidget(self.category_dropdown, 1, 0)
        
        self.category_add_button = QPushButton('Добавить')
        self.bottom_controls.addWidget(self.category_add_button, 2, 0)
        self.category_delete_button = QPushButton('Удалить')
        self.bottom_controls.addWidget(self.category_delete_button, 2, 1)
        
        self.bottom_widget = QWidget()
        self.bottom_widget.setLayout(self.bottom_controls)
        self.layout.addWidget(self.bottom_widget)
        
        self.update_data(data)
    
    def init_model(self):
        if self.model:
            self.model.clear()
        self.model = QStandardItemModel()
        self.model.setHorizontalHeaderLabels(['Категория'])
        self.root = self.model.invisibleRootItem()
        self.tree.setModel(self.model)
        self.tree.expandAll()
    
    def update_data(self, data):
        seen = {}
        self._data = data
        self.init_model()
        for value in self._data:
            pk, name, parent = value
                
            if parent == None:
                parent = self.root
            else:
                parent = seen[parent]
            
            parent.appendRow([
                QStandardItem(name)])
            seen[pk] = parent.child(parent.rowCount() - 1)
        self.set_category_dropdown()
            
    def set_category_dropdown(self):
        self.category_dropdown.clear()
        self.category_dropdown.addItem('')
        for value in self._data:
            self.category_dropdown.addItem(value[1], value[0])
            
    def get_new_category(self) -> str:
        return str(self.new_category_line_edit.text())
    
    def get_selected_parent(self) -> int:
        return self.category_dropdown.itemData(
            self.category_dropdown.currentIndex())
   
    def on_category_add_button_clicked(self, slot):
        self.category_add_button.clicked.connect(slot)
        