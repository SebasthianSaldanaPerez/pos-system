from PySide6 import QtCore
from PySide6.QtCore import Qt, QRectF, QRect, Property, QPropertyAnimation
from PySide6.QtGui import QPainter, QColor
from PySide6.QtWidgets import QWidget, QLineEdit, QVBoxLayout, QCheckBox, QPushButton, QTableWidget, QHBoxLayout, \
    QMessageBox, QTableWidgetItem, QLabel, QHeaderView

from controller.category_controller import CategoryController


class CategoriesScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.limit = 25
        self.offset = 0
        main_layout = QHBoxLayout()
        left = QWidget()
        right = QWidget()
        main_layout.addWidget(left, 1)
        main_layout.addWidget(right, 2)

        layout_left = QVBoxLayout()
        layout_left.setSpacing(20)
        layout_left.setContentsMargins(20, 20, 20, 20)
        self.search = QLineEdit()
        self.search.setPlaceholderText('Buscar ID...')

        self.label_search = QLabel('------- Búsqueda -------')
        self.label_create = QLabel('---- Crear Categoría ----')

        self.name = QLineEdit()
        self.name.setPlaceholderText('Nombre...')

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
        layout_left.addLayout(row_switch)
        layout_left.addStretch()
        layout_left.addWidget(self.btn_search)
        layout_left.addWidget(self.btn_save)

        left.setLayout(layout_left)

        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(['ID', 'Nombre', 'Activo'])
        self.table.verticalHeader().setVisible(False)

        header = self.table.horizontalHeader()
        self.table.setColumnWidth(0, 50)
        self.table.setColumnWidth(1, 200)
        self.table.setColumnWidth(2, 150)
        header.setSectionResizeMode(0, QHeaderView.Fixed)
        header.setSectionResizeMode(1, QHeaderView.Fixed)
        header.setSectionResizeMode(2, QHeaderView.Fixed)

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

        self.controller = CategoryController()
        self.current_id = None

        self.btn_save.clicked.connect(self.save_category)
        self.btn_search.clicked.connect(self.search_category)
        self.search.returnPressed.connect(self.search_category)
        self.table.cellClicked.connect(self.select_row)
        self.btn_clear.clicked.connect(self.clean_formular)
        self.btn_next.clicked.connect(self.next_page)
        self.btn_previous.clicked.connect(self.previous_page)
        self.table.setUpdatesEnabled(False)
        self.load_table()
        self.table.setUpdatesEnabled(True)


    def hideEvent(self, event):
        super().hideEvent(event)
        self.clean_formular()

    def reset_pagination(self):

        self.offset = 0

        self.load_table()

        self.update_page_label()

    def search_category(self):
        try:
            id_ = int(self.search.text())
            category = self.controller.get_by_id(id_)
            self.name.setText(category.name)
            self.switch_active.setChecked(category.active)

            self.current_id = category.id

        except Exception as e:
            QMessageBox.warning(self, 'Error', str(e))
            self.clean_formular()

    def save_category(self):
        name = self.name.text()
        active = self.switch_active.isChecked()
        try:
            if self.current_id is None:
                self.controller.create_category(name, active)
            else:
                self.controller.update_category(self.current_id, name, active)

            self.clean_formular()
            self.load_table()
        except Exception as e:
            QMessageBox.warning(self, 'Error', str(e))

    def update_page_label(self ):
        current_page = (self.offset // self.limit) + 1
        self.page_label.setText(f'Página {current_page}')

    def load_table(self):
        categories = self.controller.get_all_paginated(self.limit, self.offset)
        self.fill_table(categories)
        self.update_page_label()

    def next_page(self):
        self.offset += self.limit
        self.load_table()

    def previous_page(self):
        if self.offset >= self.limit:
            self.offset -= self.limit
            self.load_table()

    def fill_table(self, categories):
        self.table.setRowCount(len(categories))

        for row, cat in enumerate(categories):
            item_id = QTableWidgetItem(str(cat.id))
            item_id.setFlags(item_id.flags() ^ Qt.ItemIsEditable)
            self.table.setItem(row, 0, item_id)

            item_name = QTableWidgetItem(cat.name)
            item_name.setData(Qt.UserRole, cat.id)
            self.table.setItem(row, 1, item_name)

            item_active = QTableWidgetItem("Activo" if cat.active else "Inactivo")
            self.table.setItem(row, 2, item_active)

    def clean_formular(self):
        self.search.clear()
        self.name.clear()
        self.switch_active.setChecked(True)
        self.current_id = None
        self.table.clearSelection()

    def select_row(self, row, column):
        id_ = int(self.table.item(row, 0).text())

        try:
            category = self.controller.get_by_id(id_)
            self.name.setText(category.name)
            self.switch_active.setChecked(category.active)
            self.current_id = category.id

        except Exception as e:
            QMessageBox.warning(self, 'Error', str(e))


class Switch(QCheckBox):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(60,30)

        self._circle_position = 3

        self.anim = QPropertyAnimation(self, b"circle_position", self)
        self.anim.setDuration(200)
        self.anim.setEasingCurve(QtCore.QEasingCurve.InOutCubic)

        self.stateChanged.connect(self.start_transition)

    def start_transition(self):
        if self.isChecked():
            self.anim.setEndValue(30)
        else:
            self.anim.setEndValue(3)
        self.anim.start()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        if self.isChecked():
            painter.setBrush(QColor("#2ecc71"))
        else:
            painter.setBrush(QColor("#ccc"))

        painter.setPen(Qt.NoPen)
        painter.drawRoundedRect(0, 0, 60, 30, 15, 15)

        painter.setBrush(QColor("#ffffff"))
        painter.drawEllipse(self._circle_position, 3 ,24 ,24)

    def get_circle_position(self):
        return self._circle_position

    def set_circle_position(self, position):
        self._circle_position = position
        self.update()

    def mousePressEvent(self, event):
        self.setChecked(not self.isChecked())
        super().mousePressEvent(event)

    circle_position = Property(int, get_circle_position, set_circle_position)














