from PySide6.QtGui import  Qt
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QLabel, QPushButton, QMessageBox, \
    QTableWidget, QTableWidgetItem, QHeaderView, QSizePolicy

from controller.supplier_controller import SupplierController
from ui.categories_screen import Switch


class SuppliersScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.limit = 25
        self.offset = 0
        main_layout = QHBoxLayout()
        left = QWidget()
        right = QWidget()
        main_layout.addWidget(left,1)
        main_layout.addWidget(right,2)

        layout_left = QVBoxLayout()
        layout_left.setSpacing(20)
        layout_left.setContentsMargins(20, 20, 20, 20)
        self.search = QLineEdit()
        self.search.setPlaceholderText('Buscar ID...')

        self.label_search = QLabel('------- Búsqueda -------')
        self.label_create = QLabel('---- Crear Proveedor ----')

        self.name = QLineEdit()
        self.name.setPlaceholderText('Nombre...')
        self.telephone = QLineEdit()
        self.telephone.setPlaceholderText('Telefono...')


        self.switch_active = Switch()
        self.switch_active.setEnabled(True)
        self.switch_active.setChecked(True)

        self.btn_clear = QPushButton('Limpiar')
        self.btn_save = QPushButton('Guardar')
        self.btn_search = QPushButton('Buscar')

        row_switch = QHBoxLayout()
        row_switch.addWidget(self.switch_active)
        row_switch.addStretch()
        row_switch.addWidget(self.btn_clear)

        layout_left.addWidget(self.label_search, alignment=Qt.AlignCenter)
        layout_left.addWidget(self.search)
        layout_left.addSpacing(20)
        layout_left.addWidget(self.label_create, alignment=Qt.AlignCenter)
        layout_left.addWidget(self.name)
        layout_left.addSpacing(20)
        layout_left.addWidget(self.telephone)
        layout_left.addSpacing(20)
        layout_left.addLayout(row_switch)
        layout_left.addStretch()
        layout_left.addWidget(self.btn_search)
        layout_left.addWidget(self.btn_save)

        left.setLayout(layout_left)

        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(['ID', 'Nombre', 'Teléfono', 'Activo'])
        self.table.verticalHeader().setVisible(False)
        self.table.setColumnWidth(0, 50)
        self.table.setColumnWidth(1, 200)
        self.table.setColumnWidth(2, 200)
        self.table.setColumnWidth(3, 80)

        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Fixed)
        header.setSectionResizeMode(1, QHeaderView.Fixed)
        header.setSectionResizeMode(2, QHeaderView.Fixed)
        header.setSectionResizeMode(3, QHeaderView.Fixed)

        self.btn_next = QPushButton('Siguiente')
        self.btn_previous = QPushButton('Anterior')
        self.page_label = QLabel()

        layout_buttons_right = QHBoxLayout()
        layout_buttons_right.addStretch()
        layout_buttons_right.addWidget(self.btn_previous)
        layout_buttons_right.addSpacing(20)
        layout_buttons_right.addWidget(self.page_label)
        layout_buttons_right.addSpacing(20)
        layout_buttons_right.addWidget(self.btn_next)
        layout_buttons_right.addStretch()

        layout_right = QVBoxLayout()
        layout_right.addWidget(self.table)
        layout_right.addLayout(layout_buttons_right)

        right.setLayout(layout_right)

        left.setStyleSheet("""
                QWidget {
                    background-color: #ffffff;
                    border-radius: 10px;
                }

                QLineEdit {
                    border: 1px solid #ddd;
                    padding: 8px;
                    border-radius: 6px;
                }

                QLineEdit:focus {
                    border: 1px solid #3498db;
                }

                QPushButton {
                    background-color: #3498db;
                    color: white;
                    padding: 10px;
                    border-radius: 8px;
                    font-weight: bold;
                }

                QPushButton:hover {
                    background-color: #2980b9;
                }

                QCheckBox {
                    font-size: 14px;
                }
                """)

        self.table.setStyleSheet("""
                QTableWidget {
                    background-color: white;
                    border: none;
                    border-radius: 10px;
                    gridline-color: #eee;
                }

                QHeaderView::section {
                    background-color: #f8f9fa;
                    padding: 8px;
                    border: none;
                    font-weight: bold;
                }

                QTableWidget::item:selected {
                    background-color: #d0e7ff;
                    color: black; 
                }

                QTableWidget::item:hover {
                    background-color: #f5f5f5;
                }
                """)

        self.btn_save.setStyleSheet("""
                QPushButton {
            font-size: 16px;
            padding: 12px;
            border-radius: 10px;
            background-color: #3498db;
            color: white;
        }
                QPushButton:hover {
                    background-color: #2980b9;
                }
                """)

        self.btn_search.setStyleSheet("""
                QPushButton {
                font-size: 16px;
                    background-color: #2ecc71;
                    color: white;
                    padding: 12px;
                    border-radius: 10px;
                }
                QPushButton:hover {
                    background-color: #27ae60;
                }
                """)

        self.btn_clear.setStyleSheet("""
                QPushButton {
                font-size: 16px;
                    background-color: #e74c3c;
                    color: white;
                    padding: 12px;
                    border-radius: 10px;
                }
                QPushButton:hover {
                    background-color: #c0392b;
                }
                """)

        self.label_search.setStyleSheet("""
        QLabel {
            background-color: #eafaf1;
            color: #2c3e50;
            padding: 8px 18px;
            border-radius: 16px; 
            font-weight: bold;
        }
        """)

        self.label_create.setStyleSheet("""
        QLabel {
            background-color: #e8f0fe; 
            color: #2c3e50;
            padding: 8px 18px;
            border-radius: 16px;
            font-weight: bold;
        }
        """)

        self.setLayout(main_layout)

        self.controller = SupplierController()
        self.current_id = None

        self.btn_save.clicked.connect(self.save_supplier)
        self.btn_search.clicked.connect(self.search_supplier)
        self.search.returnPressed.connect(self.search_supplier)
        self.table.cellClicked.connect(self.select_row)
        self.btn_clear.clicked.connect(self.clean_formular)
        self.btn_next.clicked.connect(self.next_page)
        self.btn_previous.clicked.connect(self.previous_page)
        self.load_table()

    def reset_pagination(self):

        self.offset = 0

        self.load_table()

        self.update_page_label()

    def search_supplier(self):
        try:
            id_ = int(self.search.text())
            supplier = self.controller.get_by_id(id_)
            self.name.setText(supplier.name)
            self.telephone.setText(supplier.telephone_number)
            self.switch_active.setChecked(supplier.active)

            self.current_id = supplier.id

        except Exception as e:
            QMessageBox.warning(self, 'Error', str(e))
            self.clean_formular()

    def save_supplier(self):
        name = self.name.text()
        telephone = self.telephone.text()
        active = self.switch_active.isChecked()
        try:
            if self.current_id is None:
                self.controller.create_supplier(name, telephone, active)
            else:
                self.controller.update_supplier(self.current_id, name, telephone, active)

            self.clean_formular()
            self.load_table()
        except Exception as e:
            QMessageBox.warning(self, 'Error', str(e))

    def update_page_label(self ):
        current_page = (self.offset // self.limit) + 1
        self.page_label.setText(f'Página {current_page}')

    def load_table(self):
        suppliers = self.controller.get_all_paginated(self.limit, self.offset)
        self.fill_table(suppliers)
        self.update_page_label()

    def next_page(self):
        self.offset += self.limit
        self.load_table()

    def previous_page(self):
        if self.offset >= self.limit:
            self.offset -= self.limit
            self.load_table()

    def fill_table(self, suppliers):
        self.table.setRowCount(len(suppliers))

        for row, cat in enumerate(suppliers):
            item_id = QTableWidgetItem(str(cat.id))
            item_id.setFlags(item_id.flags() ^ Qt.ItemIsEditable)
            self.table.setItem(row, 0, item_id)

            item_name = QTableWidgetItem(cat.name)
            item_name.setData(Qt.UserRole, cat.id)
            self.table.setItem(row, 1, item_name)

            item_telephone = QTableWidgetItem(cat.telephone_number)
            item_telephone.setData(Qt.UserRole, cat.id)
            self.table.setItem(row, 2, item_telephone)

            item_active = QTableWidgetItem("Activo" if cat.active else "Inactivo")
            self.table.setItem(row, 3, item_active)

    def clean_formular(self):
        self.search.clear()
        self.name.clear()
        self.telephone.clear()
        self.switch_active.setChecked(True)
        self.current_id = None
        self.table.clearSelection()

    def select_row(self, row, column):
        id_ = int(self.table.item(row, 0).text())

        try:
            supplier = self.controller.get_by_id(id_)
            self.name.setText(supplier.name)
            self.telephone.setText(supplier.telephone_number)
            self.switch_active.setChecked(supplier.active)
            self.current_id = supplier.id

        except Exception as e:
            QMessageBox.warning(self, 'Error', str(e))

    def hideEvent(self, event):
        super().hideEvent(event)
        self.clean_formular()

