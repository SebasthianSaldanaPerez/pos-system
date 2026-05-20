import os

from PySide6.QtCore import QSize
from PySide6.QtGui import QIcon, Qt
from PySide6.QtWidgets import QWidget, QStackedWidget, QToolButton, QGridLayout, QHBoxLayout, QVBoxLayout, QTableWidget, \
    QTableWidgetItem, QHeaderView, QSizePolicy, QPushButton, QLabel

from controller.sales_controller import SalesController
from ui.pos_screen import PosScreen


class SalesScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.stack = QStackedWidget()

        self.view_general = ViewGeneral()
        self.view_detail = ViewDetail()
        self.pos_screen = PosScreen(self.view_general, self.view_detail)
        self.menu_view = QWidget()
        self.menu_view.setSizePolicy(
            QSizePolicy.Expanding,
            QSizePolicy.Expanding
        )


        main_layout = QVBoxLayout()
        menu_layout  = QVBoxLayout()
        menu_layout.setAlignment(Qt.AlignCenter)


        self.btn_general = QToolButton()
        self.btn_detail = QToolButton()

        self.btn_general.setText("General")
        self.btn_detail.setText("Detalle")


        self.btn_general.setIcon(QIcon(self.get_asset('general.png')))
        self.btn_general.setIconSize(QSize(300, 300))

        self.btn_detail.setIcon(QIcon(self.get_asset('details.png')))
        self.btn_detail.setIconSize(QSize(250, 250))

        self.btn_general.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextUnderIcon)
        self.btn_detail.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextUnderIcon)

        self.btn_general.setMinimumSize(300, 300)
        self.btn_detail.setMinimumSize(300, 300)
        self.btn_general.setMaximumSize(400, 400)
        self.btn_detail.setMaximumSize(400, 400)


        row = QHBoxLayout()

        row.setAlignment(Qt.AlignCenter)

        row.addWidget(self.btn_general)
        row.addSpacing(20)
        row.addWidget(self.btn_detail)

        menu_layout.addStretch()
        menu_layout.addLayout(row)
        menu_layout.addStretch()
        self.menu_view.setLayout(menu_layout)

        self.stack.addWidget(self.menu_view)
        self.stack.addWidget(self.view_general)
        self.stack.addWidget(self.view_detail)


        main_layout.addWidget(self.stack)
        self.setLayout(main_layout)

        self.btn_general.clicked.connect(self.show_sales_general)
        self.btn_detail.clicked.connect(self.show_sales_detail)

        self.btn_detail.setStyleSheet(f"""
QToolButton {{
    background-color: white;
    border: 2px solid #e0e0e0;
    border-radius: 25px;
    padding: 20px;
    color: #2c3e50;
    font-weight: bold;
    font-size: 32px;
}}

QToolButton:hover {{
    border: 2px solid #3498db;
    background-color: #f5faff;
}}

QToolButton:pressed {{
    background-color: #d6eaff;
   
}} """)

        self.btn_general.setStyleSheet(f"""
        QToolButton {{
            background-color: white;
            border: 2px solid #e0e0e0;
            border-radius: 25px;
            padding: 20px;
            color: #2c3e50;
            font-weight: bold;
            font-size: 32px;
        }}

        QToolButton:hover {{
            border: 2px solid #3498db;
            background-color: #f5faff;
        }}

        QToolButton:pressed {{
            background-color: #d6eaff;

        }} """)

    def get_asset(self,name):
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        return os.path.normpath(os.path.join(BASE_DIR, '', 'assets', name))

    def show_sales_general(self):
        self.view_general.reset_pagination()
        self.stack.setCurrentWidget(self.view_general)

    def show_sales_detail(self):
        self.view_detail.reset_pagination()
        self.stack.setCurrentWidget(self.view_detail)

    def show_menu(self):
        self.stack.setCurrentWidget(self.menu_view)


class ViewGeneral(QWidget):
    def __init__(self):
        super().__init__()
        self.limit = 25
        self.offset = 0
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(10)
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(['ID', 'Fecha', 'Método de pago', 'Total'])
        self.table.horizontalHeader().setDefaultAlignment(Qt.AlignCenter)
        self.table.verticalHeader().setVisible(False)
        self.table.setSizePolicy(
            QSizePolicy.Expanding,
            QSizePolicy.Expanding
        )
        self.table.setColumnWidth(0, 100)
        self.table.setColumnWidth(1, 200)
        self.table.setColumnWidth(2, 200)
        self.table.setColumnWidth(3, 200)

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

        main_layout.addLayout(layout_right)
        self.setLayout(main_layout)

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

        self.controller = SalesController()
        self.btn_next.clicked.connect(self.next_page)
        self.btn_previous.clicked.connect(self.previous_page)
        self.load_table()

    def reset_pagination(self):

        self.offset = 0

        self.load_table()

        self.update_page_label()

    def refresh(self):
        self.load_table()

    def load_table(self):
        sales = self.controller.get_all_paginated_sales(self.limit, self.offset)
        self.fill_table(sales)
        self.update_page_label()

    def update_page_label(self ):
        current_page = (self.offset // self.limit) + 1
        self.page_label.setText(f'Página {current_page}')

    def next_page(self):
        self.offset += self.limit
        self.load_table()

    def previous_page(self):
        if self.offset >= self.limit:
            self.offset -= self.limit
            self.load_table()

    def fill_table(self, sales):
        self.table.setRowCount(len(sales))

        for row, sale in enumerate(sales):
            item_id = QTableWidgetItem(str(sale.id))
            item_id.setTextAlignment(Qt.AlignCenter)
            self.table.setItem(row, 0, item_id)

            item_date = QTableWidgetItem(str(sale.date))
            item_date.setTextAlignment(Qt.AlignCenter)
            self.table.setItem(row, 1, item_date)

            item_payment = QTableWidgetItem(str(sale.payment_method))
            item_payment.setTextAlignment(Qt.AlignCenter)
            self.table.setItem(row, 2, item_payment)

            item_total = QTableWidgetItem(str(sale.total))
            item_total.setTextAlignment(Qt.AlignCenter)
            self.table.setItem(row, 3, item_total)


class ViewDetail(QWidget):
    def __init__(self):
        super().__init__()
        self.limit = 50
        self.offset = 0
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(10)
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(['ID', 'ID de Venta', 'Artículo', 'Cantidad', 'Precio de Venta', 'Total'])
        self.table.horizontalHeader().setDefaultAlignment(Qt.AlignCenter)
        self.table.verticalHeader().setVisible(False)
        self.table.setSizePolicy(
            QSizePolicy.Expanding,
            QSizePolicy.Expanding
        )
        self.table.setColumnWidth(0, 50)
        self.table.setColumnWidth(1, 100)
        self.table.setColumnWidth(2, 200)
        self.table.setColumnWidth(3, 150)
        self.table.setColumnWidth(4, 200)
        self.table.setColumnWidth(5, 200)

        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Fixed)
        header.setSectionResizeMode(1, QHeaderView.Fixed)
        header.setSectionResizeMode(2, QHeaderView.Fixed)
        header.setSectionResizeMode(3, QHeaderView.Fixed)
        header.setSectionResizeMode(4, QHeaderView.Fixed)
        header.setSectionResizeMode(5, QHeaderView.Fixed)

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

        main_layout.addLayout(layout_right)
        self.setLayout(main_layout)

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

        self.controller = SalesController()
        self.btn_next.clicked.connect(self.next_page)
        self.btn_previous.clicked.connect(self.previous_page)
        self.load_table()

    def reset_pagination(self):

        self.offset = 0

        self.load_table()

        self.update_page_label()

    def refresh(self):
        self.load_table()

    def update_page_label(self ):
        current_page = (self.offset // self.limit) + 1
        self.page_label.setText(f'Página {current_page}')

    def load_table(self):
        sales = self.controller.get_all_paginated_sales_details(self.limit, self.offset)
        self.fill_table(sales)
        self.update_page_label()

    def next_page(self):
        self.offset += self.limit
        self.load_table()

    def previous_page(self):
        if self.offset >= self.limit:
            self.offset -= self.limit
            self.load_table()

    def fill_table(self, sales):
        self.table.setRowCount(len(sales))

        for row, dtl in enumerate(sales):
            item_id = QTableWidgetItem(str(dtl.id))
            item_id.setTextAlignment(Qt.AlignCenter)
            self.table.setItem(row, 0, item_id)

            item_id_sale = QTableWidgetItem(str(dtl.sale_id))
            item_id_sale.setTextAlignment(Qt.AlignCenter)
            self.table.setItem(row, 1, item_id_sale)

            item_article = QTableWidgetItem(str(dtl.article_description))
            item_article.setTextAlignment(Qt.AlignCenter)
            self.table.setItem(row, 2, item_article)

            item_quantity = QTableWidgetItem(str(dtl.quantity))
            item_quantity.setTextAlignment(Qt.AlignCenter)
            self.table.setItem(row, 3, item_quantity)

            item_unit_price = QTableWidgetItem(str(dtl.unit_price))
            item_unit_price.setTextAlignment(Qt.AlignCenter)
            self.table.setItem(row, 4, item_unit_price)

            item_subtotal = QTableWidgetItem(str(dtl.subtotal))
            item_subtotal.setTextAlignment(Qt.AlignCenter)
            self.table.setItem(row, 5, item_subtotal)