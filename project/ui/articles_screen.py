from PySide6 import QtCore
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLineEdit, QLabel, QComboBox, QPushButton, \
    QTableWidget, QHeaderView, QMessageBox, QTableWidgetItem, QScrollArea, QSizePolicy, QCompleter

from controller.article_controller import ArticleController
from controller.category_controller import CategoryController
from ui.categories_screen import Switch


class ArticleScreen(QWidget):
    def __init__(self):
        super().__init__()
        main_layout = QHBoxLayout()
        right = QWidget()
        self.limit = 25
        self.offset = 0

        layout_left = QVBoxLayout()
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        container = QWidget()
        container.setLayout(layout_left)
        scroll.setWidget(container)

        main_layout.addWidget(scroll,1)
        main_layout.addWidget(right, 3)
        layout_left.setSpacing(20)
        layout_left.setContentsMargins(20, 20, 20, 20)
        self.search_bar_code = QLineEdit()
        self.search_bar_code.setPlaceholderText("Buscar por Código de Barras...")
        self.search_description = QLineEdit()
        self.search_description.setPlaceholderText("Buscar por Nombre...")

        self.label_search = QLabel('------- Búsqueda -------')
        self.label_create = QLabel('---- Crear Artículo ----')

        self.bar_code = QLineEdit()
        self.bar_code.setPlaceholderText("Código de Barras...")
        self.description = QLineEdit()
        self.description.setPlaceholderText("Descripción...")
        self.purchase_price = QLineEdit()
        self.purchase_price.setPlaceholderText("Precio de Compra...")
        self.retail_price = QLineEdit()
        self.retail_price.setPlaceholderText("Precio de Menudeo...")
        self.wholesale_price = QLineEdit()
        self.wholesale_price.setPlaceholderText("Precio de Mayoreo...")
        self.stock = QLineEdit()
        self.stock.setPlaceholderText("Stock...")
        self.category = QComboBox()
        self.controller_categories = CategoryController()
        self.load_categories()

        self.switch_active = Switch()
        self.switch_active.setEnabled(True)
        self.switch_active.setChecked(True)

        self.btn_clear = QPushButton('Limpiar')
        self.btn_save = QPushButton('Guardar')
        self.btn_search = QPushButton('Buscar')

        for field in [self.search_description, self.search_bar_code, self.bar_code, self.description, self.purchase_price, self.retail_price, self.wholesale_price, self.stock]:
            field.setMinimumHeight(36)

        self.btn_save.setMinimumHeight(40)
        self.btn_search.setMinimumHeight(40)
        self.btn_clear.setMinimumHeight(40)
        self.category.setMinimumHeight(40)

        row_switch = QHBoxLayout()
        row_switch.addWidget(self.switch_active)
        row_switch.addStretch()
        row_switch.addWidget(self.btn_clear)

        layout_left.addWidget(self.label_search, alignment=Qt.AlignCenter)
        layout_left.addWidget(self.search_bar_code)
        layout_left.addWidget(self.search_description)
        #layout_left.addSpacing(5)
        layout_left.addWidget(self.label_create, alignment=Qt.AlignCenter)
        layout_left.addLayout(self.create_field("Código de Barra", self.bar_code))
        layout_left.addLayout(self.create_field("Descripción", self.description))

        layout_left.addLayout(self.create_field("Precio de Compra", self.purchase_price))
        layout_left.addLayout(self.create_field("Precio de Menudeo", self.retail_price))
        layout_left.addLayout(self.create_field("Precio de Mayoreo", self.wholesale_price))
        layout_left.addLayout(self.create_field("Stock", self.stock))

        layout_left.addWidget(self.category)

        layout_left.addLayout(row_switch)
        layout_left.addWidget(self.btn_search)
        layout_left.addWidget(self.btn_save)


        self.table = QTableWidget()
        self.table.setColumnCount(9)
        self.table.setHorizontalHeaderLabels(['ID', 'Código de Barras', 'Descripción', 'Precio de Compra',
                                              'Precio de Menudeo', 'Precio de Mayoreo', 'Stock', 'Categoría', 'Activo'])
        self.table.verticalHeader().setVisible(False)
        self.table.setColumnWidth(0, 50)
        self.table.setColumnWidth(1, 150)
        self.table.setColumnWidth(2, 200)
        self.table.setColumnWidth(3, 150)
        self.table.setColumnWidth(4, 150)
        self.table.setColumnWidth(5, 150)
        self.table.setColumnWidth(6, 150)  #
        self.table.setColumnWidth(7, 150)
        self.table.setColumnWidth(8, 70)  #

        self.table.setWordWrap(False)
        self.table.setTextElideMode(Qt.ElideRight)

        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Fixed)
        header.setSectionResizeMode(1, QHeaderView.Fixed)
        header.setSectionResizeMode(2, QHeaderView.Fixed)
        header.setSectionResizeMode(3, QHeaderView.Fixed)
        header.setSectionResizeMode(4, QHeaderView.Fixed)
        header.setSectionResizeMode(5, QHeaderView.Fixed)
        header.setSectionResizeMode(6, QHeaderView.Fixed)
        header.setSectionResizeMode(7, QHeaderView.Fixed)
        header.setSectionResizeMode(8, QHeaderView.Fixed)

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

        scroll.setStyleSheet("""
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
                    padding: 10px;
                    border-radius: 8px;
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
                            padding: 10px;
                    border-radius: 8px;
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
                            padding: 8px;
                    border-radius: 6px;
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

        self.category.setStyleSheet("""
        QComboBox {
            background-color: #fafafa;
            border: 1px solid #ddd;
            border-radius: 8px;
            padding: 8px 12px;
            padding-right: 30px;
            color: #2c3e50;
        }

        QComboBox::drop-down {
            subcontrol-origin: padding;
            subcontrol-position: top right;
            width: 30px;
            border: none;
            background-color: white;  /* 🔥 clave */
        }

        QComboBox::down-arrow {
            image: none;
            border-left: 5px solid transparent;
            border-right: 5px solid transparent;
            border-top: 6px solid #2c3e50;
            margin-right: 10px;
        }

        QComboBox:hover {
            border: 1px solid #3498db;
        }

        QComboBox:focus {
            border: 1px solid #3498db;
        }
        """)

        self.setLayout(main_layout)

        self.controller = ArticleController()
        self.current_id = None

        self.btn_save.clicked.connect(self.save_article)
        self.btn_search.clicked.connect(self.search_article)
        self.search_bar_code.returnPressed.connect(self.search_article)
        self.search_description.returnPressed.connect(self.search_article)
        self.table.cellClicked.connect(self.select_row)
        self.btn_clear.clicked.connect(self.clean_formular)
        self.btn_next.clicked.connect(self.next_page)
        self.btn_previous.clicked.connect(self.previous_page)
        self.table.setUpdatesEnabled(False)
        self.load_table()
        self.table.setUpdatesEnabled(True)
        self.load_article_suggestions()

    def load_categories(self):
        categories = self.controller_categories.get_all()
        self.category.clear()
        self.category.addItem('Selecciona categoría', None)
        for category in categories:
            if category.active:
                self.category.addItem(category.name, category.id)

    def update_page_label(self ):
        current_page = (self.offset // self.limit) + 1
        self.page_label.setText(f'Página {current_page}')

    def load_article_suggestions(self):
        articles = self.controller.get_all()

        self.article_map = {a.description: a for a in articles  if a.description and a.description.strip()}


        completer = QCompleter(list(self.article_map.keys()))
        completer.setCaseSensitivity(QtCore.Qt.CaseInsensitive)
        completer.setFilterMode(Qt.MatchContains)
        completer.popup().setStyleSheet("""
        QListView {
            background-color: white;
            border: 1px solid #ddd;
            padding: 0px;
            border-radius: 8px;
        }

        QListView::item {
            padding: 6px;
        }

        QListView::item:selected {
            background-color: #d0e7ff;
            color: black;
        }
        """)
        self.search_description.setCompleter(completer)
        completer.activated.connect(self.select_article_from_completer)

    def select_article_from_completer(self, text):
        article = self.article_map.get(text)
        if article:
            self.fill_form(article)

    def showEvent(self, event):
        super().showEvent(event)
        self.load_categories()
        self.load_article_suggestions()
        self.set_limit_offset()
        self.clean_formular()
        self.table.setUpdatesEnabled(False)
        self.load_table()
        self.table.setUpdatesEnabled(True)
        self.set_limit_offset()

    def hideEvent(self, event):
        super().hideEvent(event)
        self.clean_formular()

    def search_article(self):
        print('FUNCIONA')
        bar_code = self.search_bar_code.text().strip()
        description = self.search_description.text().strip()

        print("barcode", bar_code)
        print("description", description)

        if bar_code and description:
            QMessageBox.warning(self, "Error", "Solo puedes buscar por código o por nombre, no ambos")
            return  self.clean_search()

        if not bar_code and not description:
            QMessageBox.warning(self, "Error", "Debe ingresar un criterio de búsqueda")
            return self.clean_search()

        try:
            if bar_code:
                article = self.controller.get_by_bar_code(bar_code)
                self.fill_form(article)
            elif description:
                article = self.controller.get_by_description(description)
                if not article:
                    QMessageBox.information(self, "Sin resultados", "No se encontraron resultados")
                    return

                self.fill_form(article[0])

        except Exception as e:
            QMessageBox.warning(self, "Error", str(e))

    def clean_search(self):
        self.search_bar_code.clear()
        self.search_description.clear()

    def fill_form(self, article):
        self.bar_code.setText(article.bar_code)
        self.description.setText(article.description)
        self.purchase_price.setText(str(article.purchase_price))
        self.retail_price.setText(str(article.retail_price))
        self.wholesale_price.setText(str(article.wholesale_price))
        self.stock.setText(str(article.stock))

        self.switch_active.setChecked(article.active)
        index = self.category.findData(article.category_id)
        if index != -1:
            self.category.setCurrentIndex(index)
        self.current_id = article.id

    def save_article(self):
        bar_code = self.bar_code.text()
        description = self.description.text()
        purchase_price = self.purchase_price.text()
        retail_price = self.retail_price.text()
        wholesale_price = self.wholesale_price.text()
        stock = self.stock.text()
        active = self.switch_active.isChecked()
        category_id = self.category.currentData()
        try:
            if category_id is None:
                raise ValueError('Selecciona una categoría')

            if self.current_id is None:
                self.controller.create_article(bar_code, description, purchase_price,
                                               retail_price, wholesale_price, stock, category_id, active)
            else:
                self.controller.update_article(self.current_id, bar_code, description,
                                               purchase_price, retail_price, wholesale_price, stock, category_id, active)
            self.clean_formular()
            self.table.setUpdatesEnabled(False)
            self.load_table()
            self.table.setUpdatesEnabled(True)
            self.load_article_suggestions()
        except Exception as e:
            QMessageBox.warning(self, "Error", str(e))

    def load_table(self):
        articles = self.controller.get_all_paginated(self.limit, self.offset)
        self.fill_table(articles)
        self.update_page_label()

    def set_limit_offset(self):
        self.offset = 0
        self.limit = 25

    def next_page(self):
        self.offset += self.limit
        self.load_table()

    def previous_page(self):
        if self.offset >= self.limit:
            self.offset -= self.limit
            self.load_table()

    def fill_table(self, articles):
        self.table.setRowCount(len(articles))

        for row, art in enumerate(articles):
            item_id = QTableWidgetItem(str(art.id))
            item_id.setFlags(item_id.flags() ^ Qt.ItemIsEditable)
            self.table.setItem(row, 0, item_id)

            item_bar_code = QTableWidgetItem(art.bar_code)
            item_bar_code.setData(Qt.UserRole, art.bar_code)
            self.table.setItem(row, 1, item_bar_code)

            item_description = QTableWidgetItem(art.description)
            item_description.setData(Qt.UserRole, art.description)
            self.table.setItem(row, 2, item_description)

            item_purchase_price = QTableWidgetItem(str(art.purchase_price))
            item_purchase_price.setData(Qt.UserRole, art.purchase_price)
            self.table.setItem(row, 3, item_purchase_price)

            item_retail_price = QTableWidgetItem(str(art.retail_price))
            item_retail_price.setData(Qt.UserRole, art.retail_price)
            self.table.setItem(row, 4, item_retail_price)

            item_wholesale_price = QTableWidgetItem(str(art.wholesale_price))
            item_wholesale_price.setData(Qt.UserRole, art.wholesale_price)
            self.table.setItem(row, 5, item_wholesale_price)

            item_stock = QTableWidgetItem(str(art.stock))
            item_stock.setData(Qt.UserRole, art.stock)
            self.table.setItem(row, 6, item_stock)

            item_category = QTableWidgetItem(str(art.category_name))
            self.table.setItem(row, 7, item_category)

            item_active = QTableWidgetItem("Activo" if art.active else "Inactivo")
            self.table.setItem(row, 8, item_active)

    def clean_formular(self):
        self.search_bar_code.clear()
        self.search_description.clear()
        self.bar_code.clear()
        self.description.clear()
        self.purchase_price.clear()
        self.wholesale_price.clear()
        self.retail_price.clear()
        self.stock.clear()
        self.category.setCurrentIndex(0)
        self.switch_active.setChecked(True)
        self.current_id = None
        self.table.clearSelection()

    def select_row(self, row, column):
        id_ = int(self.table.item(row, 0).text())

        try:
            article = self.controller.get_by_id(id_)
            self.fill_form(article)

        except Exception as e:
            QMessageBox.warning(self, "Error", str(e))

    def create_field(self, label_text, field):
        layout = QVBoxLayout()
        layout.setSpacing(4)

        label = QLabel(label_text)
        label.setStyleSheet("""
            QLabel {
                font-size: 9pt;
                color: #555;
                padding-left: 4px;
            }
        """)

        layout.addWidget(label)
        layout.addWidget(field)

        return layout

