from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLineEdit, QLabel, QPushButton, QTableWidget, \
    QHeaderView, QSizePolicy, QMessageBox, QTableWidgetItem
from decimal import Decimal

from controller.article_controller import ArticleController
from controller.movements_controller import StockMovementController


class StockMovementScreen(QWidget):
    def __init__(self):
        super().__init__()
        main_layout = QHBoxLayout()
        left = QWidget()
        right = QWidget()
        main_layout.addWidget(left, 1)
        main_layout.addWidget(right, 2)
        self.limit = 25
        self.offset = 0

        layout_left = QVBoxLayout()
        layout_left.setSpacing(20)
        layout_left.setContentsMargins(20, 20, 20, 20)

        self.label_create = QLabel('---- Crear Ajuste ----')

        self.bar_code = QLineEdit()
        self.bar_code.setPlaceholderText('Código de Barras...')
        self.article_name = QLineEdit()
        self.article_name.setPlaceholderText('Articulo...')
        self.article_name.setReadOnly(True)
        self.new_stock = QLineEdit()
        self.new_stock.setPlaceholderText('Cantidad Correcta...')

        self.btn_clear = QPushButton('Limpiar')
        self.btn_clear.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.btn_save = QPushButton('Guardar')


        layout_left.addWidget(self.label_create, alignment=Qt.AlignCenter)
        layout_left.addWidget(self.bar_code)
        layout_left.addSpacing(20)
        layout_left.addWidget(self.article_name)
        layout_left.addSpacing(20)
        layout_left.addWidget(self.new_stock)
        layout_left.addSpacing(20)
        layout_left.addWidget(self.btn_clear)
        layout_left.addStretch()
        layout_left.addWidget(self.btn_save)

        left.setLayout(layout_left)

        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(['ID', 'Tipo', 'Cantidad', 'Artículo', 'Fecha'])
        self.table.verticalHeader().setVisible(False)
        self.table.setColumnWidth(0, 50)
        self.table.setColumnWidth(1, 100)
        self.table.setColumnWidth(2, 100)
        self.table.setColumnWidth(3, 150)
        self.table.setColumnWidth(4, 200)

        self.table.setWordWrap(False)
        self.table.setTextElideMode(Qt.ElideRight)

        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Fixed)
        header.setSectionResizeMode(1, QHeaderView.Fixed)
        header.setSectionResizeMode(2, QHeaderView.Fixed)
        header.setSectionResizeMode(3, QHeaderView.Fixed)
        header.setSectionResizeMode(4, QHeaderView.Fixed)

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
        self.setLayout(main_layout)

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

        self.label_create.setStyleSheet("""
        QLabel {
            background-color: #e8f0fe; 
            color: #2c3e50;
            padding: 8px 18px;
            border-radius: 16px;
            font-weight: bold;
        }
        """)

        self.article_name.setStyleSheet("""QLineEdit {
                                  background-color: #fafafa;
                                   }""")

        self.controller = StockMovementController()
        self.controller_article = ArticleController()
        self.btn_save.clicked.connect(self.save_stock_movement)
        self.btn_clear.clicked.connect(self.clean_formular)
        self.bar_code.returnPressed.connect(self.load_article_data)
        self.btn_next.clicked.connect(self.next_page)
        self.btn_previous.clicked.connect(self.previous_page)
        self.load_table()

    def reset_pagination(self):

        self.offset = 0

        self.load_table()

        self.update_page_label()

    def save_stock_movement(self):
        bar_code = self.bar_code.text().strip()
        new_stock = Decimal(self.new_stock.text())

        article = ArticleController().get_by_bar_code(str(bar_code))

        try:
            self.controller.create_stock_movement(article.id, new_stock)
            self.clean_formular()
            self.load_table()
        except Exception as e:
            QMessageBox.warning(self, "Error", str(e))
        self.load_table()

    def update_page_label(self ):
        current_page = (self.offset // self.limit) + 1
        self.page_label.setText(f'Página {current_page}')

    def load_table(self):
        stock_movements = self.controller.get_all_paginated(self.limit, self.offset)
        self.fill_table(stock_movements)
        self.update_page_label()

    def next_page(self):
        self.offset += self.limit
        self.load_table()

    def previous_page(self):
        if self.offset >= self.limit:
            self.offset -= self.limit
            self.load_table()


    def fill_table (self, stock_movements):
        self.table.setRowCount(len(stock_movements))

        for row, stc in enumerate(stock_movements):
            item_id = QTableWidgetItem(str(stc.id))
            item_id.setFlags(item_id.flags() ^ Qt.ItemIsEditable)
            self.table.setItem(row, 0, item_id)

            item_type = QTableWidgetItem(stc.type)
            item_type.setData(Qt.UserRole, stc.type)
            self.table.setItem(row, 1, item_type)

            item_quantity = QTableWidgetItem(str(stc.quantity))
            item_quantity.setData(Qt.UserRole, stc.quantity)
            self.table.setItem(row, 2, item_quantity)

            item_article = QTableWidgetItem(stc.article_name)
            item_article.setData(Qt.UserRole, stc.article_name)
            self.table.setItem(row, 3, item_article)

            item_date = QTableWidgetItem(str(stc.date))
            item_date.setData(Qt.UserRole, stc.date)
            self.table.setItem(row, 4, item_date)

    def clean_formular(self):
        self.bar_code.clear()
        self.new_stock.clear()
        self.article_name.clear()

    def load_article_data(self):
        bar_code = self.bar_code.text().strip()

        if not bar_code:
            return
        try:
            article = ArticleController().get_by_bar_code(bar_code)
            if not article:
                QMessageBox.warning(self, "Error", "Articulo no encontrado")
                self.article_name.clear()
                return
            self.article_name.setText(article.description)

        except Exception as e:
            QMessageBox.warning(self, "Error", str(e))

    def showEvent(self, event):
        super().showEvent(event)
        self.clean_formular()
        self.load_table()



