from PySide6 import QtCore
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from PySide6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLineEdit, QComboBox, QTableWidget, QSizePolicy, \
    QHeaderView, QLabel, QPushButton, QCompleter, QTableWidgetItem, QMessageBox

from controller.article_controller import ArticleController
from controller.pop_controller import PurchaseController
from controller.supplier_controller import SupplierController
from database.connection import Connection


class PopScreen(QWidget):
    def __init__(self, view_general, view_detail):
        super().__init__()
        self.view_general = view_general
        self.view_detail = view_detail
        self.view_general.refresh()
        self.view_detail.refresh()
        self.loading_table = False
        self.controller_suppliers = SupplierController()
        self.controller_articles = ArticleController()
        self.conn = Connection().get_connection()
        main_layout = QVBoxLayout()

        self.article = QLineEdit()
        self.article.setPlaceholderText('Buscar por Código de Barras o Nombre...')
        self.article.setMinimumHeight(60)
        self.supplier = QComboBox()
        self.supplier.setMinimumHeight(60)
        self.load_supplier()

        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(['Código de Barras', 'Artículo', 'Cantidad', 'Precio de Compra',  'Subtotal', 'Eliminar'])
        self.table.horizontalHeader().setDefaultAlignment(Qt.AlignCenter)
        self.table.verticalHeader().setVisible(False)
        self.table.verticalHeader().setDefaultSectionSize(60)
        self.table.itemChanged.connect(self.update_cart_from_table)
        self.table.setSizePolicy(
            QSizePolicy.Expanding,
            QSizePolicy.Expanding
        )

        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Stretch)
        header.setSectionResizeMode(1, QHeaderView.Stretch)
        header.setSectionResizeMode(2, QHeaderView.Stretch)
        header.setSectionResizeMode(3, QHeaderView.Stretch)
        header.setSectionResizeMode(4, QHeaderView.Stretch)

        row_amount_general = QHBoxLayout()
        row_amounts = QVBoxLayout()
        self.total = QLabel()
        self.total.setText("TOTAL: $0.00")
        self.payment = QLineEdit()
        self.payment.setPlaceholderText('Monto Pagado')
        self.payment.setMinimumHeight(70)
        self.payment.setSizePolicy(
            QSizePolicy.Expanding,
            QSizePolicy.Fixed
        )
        self.payment.textChanged.connect(self.update_change)
        self.change = QLabel()
        self.change.setText("CAMBIO: $0.00")

        row_space = QVBoxLayout()
        self.space = QLabel()

        row_amount_general.addLayout(row_space)
        row_amount_general.addStretch()
        row_amount_general.addLayout(row_amounts)


        row_buttons = QHBoxLayout()
        self.btn_clear = QPushButton('Cancelar')
        self.btn_save = QPushButton('Generar Comprar')
        row_buttons.addWidget(self.btn_clear)
        row_buttons.addWidget(self.btn_save)

        row_amounts.addWidget(self.total)
        row_amounts.addWidget(self.payment)
        row_amounts.addWidget(self.change)


        main_layout.addWidget(self.article)
        main_layout.addWidget(self.supplier)
        main_layout.addWidget(self.table)
        main_layout.addLayout(row_amount_general)
        main_layout.addLayout(row_buttons)

        self.supplier.setStyleSheet("""
        QComboBox {
            background-color: white;

            border: 2px solid #e0e0e0;
            border-radius: 12px;

            padding: 14px 18px;
            padding-right: 40px;

            color: #2c3e50;

            font-size: 22px;
            font-weight: bold;
        }

        QComboBox:hover {
            border: 2px solid #3498db;
        }

        QComboBox:focus {
            border: 2px solid #3498db;
            background-color: #f8fbff;
        }

        QComboBox::drop-down {
            border: none;
            width: 40px;
            background: transparent;
        }

        QComboBox::down-arrow {
            image: none;

            border-left: 7px solid transparent;
            border-right: 7px solid transparent;
            border-top: 10px solid #2c3e50;

            margin-right: 12px;
        }
        """)
        self.btn_clear.setStyleSheet("""
                        QPushButton {
                        font-size: 24px;
                        font-weight: bold;
                        letter-spacing: 1px;
                            background-color: #e74c3c;
                            color: white;
                            padding: 12px;
                    border-radius: 10px;
                        }
                        QPushButton:hover {
                            background-color: #c0392b;
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

    padding: 14px;

    border: none;

    font-size: 18px;
    font-weight: bold;

    color: #2c3e50;
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
                    font-size: 24px;
                    font-weight: bold;
                    letter-spacing: 1px;
                    padding: 12px;
                    border-radius: 10px;
                    background-color: #3498db;
                    color: white;
                }
                        QPushButton:hover {
                            background-color: #2980b9;
                        }
                        """)
        self.total.setStyleSheet("""
        QLabel {
            background-color: white;
            border: 2px solid #e0e0e0;
            border-radius: 12px;
            padding: 14px 18px;

            color: #2c3e50;

            font-size: 28px;
            font-weight: bold;
            letter-spacing: 1px;
        }
        """)
        self.change.setStyleSheet("""
        QLabel {
            background-color: #eafaf1;
            border: 2px solid #b7ebc6;
            border-radius: 12px;
            padding: 14px 18px;

            color: #27ae60;

            font-size: 28px;
            font-weight: bold;
            letter-spacing: 1px;
        }
        """)
        self.payment.setStyleSheet("""
        QLineEdit {
            background-color: white;
            border: 2px solid #e0e0e0;
            border-radius: 12px;

            padding: 14px 18px;

            color: #2c3e50;

            font-size: 28px;
            font-weight: bold;
            letter-spacing: 1px;
        }

        QLineEdit:hover {
            border: 2px solid #3498db;
        }

        QLineEdit:focus {
            border: 2px solid #3498db;
            background-color: #f8fbff;
        }
        """)
        self.article.setStyleSheet("""
        QLineEdit {
            background-color: white;

            border: 2px solid #e0e0e0;
            border-radius: 12px;

            padding: 14px 18px;

            color: #2c3e50;

            font-size: 22px;
            font-weight: bold;
        }

        QLineEdit:hover {
            border: 2px solid #3498db;
        }

        QLineEdit:focus {
            border: 2px solid #3498db;
            background-color: #f8fbff;
        }
        """)

        self.setLayout(main_layout)

        self.controller_pop = PurchaseController(self.conn)
        self.current_id = None

        self.article.returnPressed.connect(self.search_article)
        self.btn_save.clicked.connect(self.save_purchase)
        self.load_article_suggestions()
        self.btn_clear.clicked.connect(self.clear_order)

    
    def reset(self):
        self.controller_pop.clear_cart()
        self.table.setRowCount(0)
        self.article.clear()
        self.supplier.setCurrentIndex(0)
        self.payment.clear()

        self.total.setText('TOTAL: $0.00')
        self.change.setText('CAMBIO: $0.00')
    
    def refresh(self):
        self.load_article_suggestions()
        self.load_supplier()

    def load_supplier(self):
        suppliers = self.controller_suppliers.get_all()
        self.supplier.clear()
        self.supplier.addItem('Selecciona un Proveedor', None)
        for supplier in suppliers:
            if supplier.active:
                self.supplier.addItem(supplier.name, supplier.id)

    def closeEvent(self, event):
        Connection.release_connections(self.conn)
        super().closeEvent(event)

    def load_article_suggestions(self):
        articles = self.controller_articles.get_all()

        self.article_map = {a.description: a for a in articles if a.description and a.description.strip()}

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
        self.article.setCompleter(completer)
        completer.activated.connect(self.select_article_from_completer)

    def select_article_from_completer(self, text):
        article = self.article_map.get(text)
        if article:
            self.controller_pop.add_article(article)
            self.load_table()
            self.refresh_totals()
            QtCore.QTimer.singleShot(0, self.article.clear)

    def search_article(self):
        text = self.article.text().strip()
        if not text:
            return
        try:
            self.controller_pop.get_by_bar_code(text)
            self.load_table()
            self.refresh_totals()
            self.article.clear()
            self.article.setFocus()
            return

        except:
            pass

    def big_font(self):
        font = QFont()
        font.setPointSize(16)
        font.setBold(True)
        return font

    def change_quantity_input(self,article_id,input_widget):
        try:
            quantity = int(input_widget.text())
            self.controller_pop.update_quantity(article_id,quantity)
            self.load_table()
            self.refresh_totals()
        except:
            pass

    def increase_quantity(self, article_id):

        self.controller_pop.increase_quantity(article_id)

        self.load_table()
        self.refresh_totals()

    def decrease_quantity(self, article_id):

        self.controller_pop.decrease_quantity(
            article_id
        )

        self.load_table()

        self.refresh_totals()

    def delete_article(self, article_id):
        self.controller_pop.remove_article(article_id)
        self.load_table()
        self.refresh_totals()

    def save_purchase(self):
        try:
            supplier_id = self.supplier.currentData()
            supplier_name = self.supplier.currentText()
            self.controller_pop.set_supplier(supplier_id, supplier_name)
            purchase = self.controller_pop.checkout()
            self.view_general.refresh()
            self.view_detail.refresh()
            QMessageBox.information(self, "Compra Generada", f"Compra #{purchase.id} guardada correctamente")
            self.table.setRowCount(0)
            self.article.clear()
            self.payment.clear()
            self.supplier.setCurrentIndex(0)
            self.refresh_totals()
            self.change.setText("CAMBIO: $0.00")
            self.article.setFocus()

        except ValueError as e:
            QMessageBox.warning(self, "Error", str(e))
        except Exception as e:
            QMessageBox.warning(self, "Error Crítico", str(e))

    def update_amounts(self):
        total = self.controller_pop.get_total()
        self.total.setText(f"TOTAL: ${float(total):.2f}")

    def update_change(self):
        text = self.payment.text().strip()
        if not text:
            self.change.setText("CAMBIO: $0.00")
            return
        try:
            amount_paid = float(text)
            self.controller_pop.set_amount_paid(amount_paid)
            change = self.controller_pop.calculate_change()
            self.change.setText(f"CAMBIO: ${float(change):.2f}")
        except ValueError:
            self.change.setText("CAMBIO: $0.00")

    def update_cart_from_table(self, item):

        if self.loading_table:
            return

        row = item.row()
        column = item.column()

        if column !=3:
            return

        try:
            self.table.blockSignals(True)
            article_id = int(self.table.item(row, 0).data(Qt.UserRole))
            price = float(self.table.item(row, 3).text())
            self.controller_pop.update_price(article_id,price)
            subtotal = (self.controller_pop.cart[article_id]['quantity'] * price)
            self.table.item(row,4).setText(f"${subtotal:.2f}")
            self.refresh_totals()

        except Exception as e:

            print(e)
        finally:
            self.table.blockSignals(False)

    def clear_order(self):

        response = QMessageBox.question(self, "Cancelar Compra", "¿Deseas cancelar la compra?", QMessageBox.Yes, QMessageBox.No)

        if response == QMessageBox.No:
            return

        self.controller_pop.clear_cart()
        self.table.setRowCount(0)
        self.article.clear()
        self.supplier.setCurrentIndex(0)
        self.payment.clear()
        self.refresh_totals()

    def refresh_totals(self):
        cart = self.controller_pop.cart
        for row, item in enumerate(cart.values()):
            subtotal = (item['quantity'] * item['purchase_price'])
            self.table.item(row,4).setText(f"${float(subtotal):.2f}")

        self.update_amounts()
        self.update_change()

    def load_table(self):

        self.loading_table = True
        cart = self.controller_pop.cart

        self.table.setRowCount(len(cart))

        for row, item in enumerate(cart.values()):
            subtotal = (item['quantity']*item['purchase_price'])
            barcode_item = QTableWidgetItem(item['bar_code'])
            barcode_item.setTextAlignment(Qt.AlignCenter)
            barcode_item.setFont(self.big_font())
            barcode_item.setData(Qt.UserRole, item['article_id'])
            self.table.setItem(row,0,barcode_item)

            description_item = QTableWidgetItem(item['description'])
            description_item.setFont(self.big_font())
            self.table.setItem(row,1,description_item)

            quantity_item = QTableWidgetItem(str(item['quantity']))
            quantity_item.setTextAlignment(Qt.AlignCenter)
            quantity_widget = QWidget()
            quantity_layout = QHBoxLayout()
            quantity_layout.setContentsMargins( 4, 4, 4, 4)
            quantity_layout.setSpacing(10)
            btn_minus = QPushButton("-")
            btn_plus = QPushButton("+")
            btn_plus.setStyleSheet("""
            QPushButton {
                background-color: #2ecc71;
                color: white;

                border: none;
                border-radius: 6px;

                font-size: 16px;
                font-weight: bold;

                min-width: 40px;
                max-width: 40px;

                min-height: 28px;
                max-height: 28px;
            }

            QPushButton:hover {
                background-color: #27ae60;
            }

            QPushButton:pressed {
                background-color: #219150;
            }
            """)
            btn_minus.setStyleSheet("""
            QPushButton {
                background-color: #e74c3c;
                color: white;

                border: none;
                border-radius: 6px;

                font-size: 16px;
                font-weight: bold;

                min-width: 40px;
                max-width: 40px;

                min-height: 28px;
                max-height: 28px;
            }

            QPushButton:hover {
                background-color: #c0392b;
            }

            QPushButton:pressed {
                background-color: #a93226;
            }
            """)
            quantity_input = QLineEdit(str(item["quantity"]))
            quantity_input.setAlignment(Qt.AlignCenter)
            quantity_input.setFixedWidth(50)
            quantity_input.setStyleSheet("""
            QLineEdit {
                border: 1px solid #dcdcdc;
                border-radius: 6px;

                font-size: 16px;
                font-weight: bold;

                padding: 4px;
            }
            """)
            quantity_input.editingFinished.connect(lambda aid=item['article_id'],input_widget=quantity_input:self.change_quantity_input(aid,input_widget))

            btn_minus.clicked.connect(lambda _, aid=item['article_id']:self.decrease_quantity(aid))
            btn_plus.clicked.connect(lambda _, aid=item['article_id']:self.increase_quantity(aid))
            quantity_layout.addWidget(btn_minus)
            quantity_layout.addWidget(quantity_input)
            quantity_layout.addWidget(btn_plus)
            quantity_widget.setLayout(quantity_layout)
            self.table.setCellWidget(row,2,quantity_widget)

            price_item = QTableWidgetItem(f"{float(item['purchase_price']):.2f}")
            price_item.setTextAlignment(Qt.AlignCenter)
            price_item.setFont(self.big_font())
            self.table.setItem(row, 3, price_item)

            subtotal_item = QTableWidgetItem(f"{float(subtotal):.2f}")
            subtotal_item.setTextAlignment(Qt.AlignCenter)
            subtotal_item.setFont(self.big_font())
            subtotal_item.setFlags(subtotal_item.flags()& ~Qt.ItemIsEditable)
            self.table.setItem(row,4,subtotal_item)
            btn_delete = QPushButton('X')
            btn_delete.setStyleSheet("""
            QPushButton {
                background-color: #e74c3c;
                color: white;
                border: none;
                border-radius: 8px;
                font-weight: bold;
                padding: 6px;
            }

            QPushButton:hover {
                background-color: #c0392b;
            }
            """)
            btn_delete.clicked.connect(lambda _,aid=item['article_id']:self.delete_article(aid))
            self.table.setCellWidget(row, 5, btn_delete)

        self.loading_table = False
