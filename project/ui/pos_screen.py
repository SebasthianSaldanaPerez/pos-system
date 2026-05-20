from PySide6 import QtCore
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QTableWidget, QHeaderView, QSizePolicy, QLabel, \
    QHBoxLayout, QComboBox, QPushButton, QCompleter, QMessageBox, QTableWidgetItem, QDoubleSpinBox

from controller.article_controller import ArticleController
from controller.pos_controller import PosController
from database.connection import Connection


class PosScreen(QWidget):
    def __init__(self, view_general, view_detail):
        super().__init__()
        self.view_general = view_general
        self.view_detail = view_detail
        self.view_general.refresh()
        self.view_detail.refresh()
        self.loading_table = False
        self.controller_articles = ArticleController()
        self.conn = Connection().get_connection()
        self.controller_pos = PosController(self.conn)
        main_layout = QVBoxLayout()

        row_principal = QHBoxLayout()
        self.article = QLineEdit()
        self.article.setPlaceholderText("Buscar por Código de Barras o Nombre...")
        self.article.setMinimumHeight(60)

        self.price_mode = QComboBox()
        self.price_mode.addItems(['MENUDEO', 'MAYOREO'])
        self.price_mode.setMinimumHeight(70)

        row_principal.addWidget(self.article)
        row_principal.addWidget(self.price_mode)

        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(['Código de Barras', 'Artículo', 'Cantidad', 'Precio de Venta', 'Subtotal', 'Eliminar'])
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

        row_method = QVBoxLayout()
        self.method = QComboBox()
        self.method.addItems(['EFECTIVO', 'TARJETA', 'TRANSFERENCIA'])
        self.method.setMinimumHeight(70)
        self.commission = QDoubleSpinBox()
        self.commission.setSuffix("%")
        self.commission.setValue(5.0)
        self.commission.setDecimals(2)
        self.commission.setMaximum(100)
        self.commission.hide()
        row_method.addWidget(self.method)
        row_method.addWidget(self.commission)

        row_amount_general.addLayout(row_method)
        row_amount_general.addStretch()
        row_amount_general.addLayout(row_amounts)

        row_buttons = QHBoxLayout()
        self.btn_clear = QPushButton('Cancelar')
        self.btn_save = QPushButton('Generar Venta')
        row_buttons.addWidget(self.btn_clear)
        row_buttons.addWidget(self.btn_save)

        row_amounts.addWidget(self.total)
        row_amounts.addWidget(self.payment)
        row_amounts.addWidget(self.change)

        main_layout.addLayout(row_principal)
        main_layout.addWidget(self.table)
        main_layout.addLayout(row_amount_general)
        main_layout.addLayout(row_buttons)

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
        self.method.setStyleSheet("""
        QComboBox {
            background-color: white;

            border: 2px solid #dfe6e9;
            border-radius: 14px;

            padding: 14px 20px;
            padding-right: 45px;

            color: #2c3e50;

            font-size: 24px;
            font-weight: bold;
            letter-spacing: 1px;
        }

        QComboBox:hover {
            border: 2px solid #3498db;
            background-color: #f8fbff;
        }

        QComboBox:focus {
            border: 2px solid #2980b9;
            background-color: #eef7ff;
        }

        QComboBox::drop-down {
            border: none;
            width: 45px;
            background: transparent;
        }

        QComboBox::down-arrow {
            image: none;

            border-left: 8px solid transparent;
            border-right: 8px solid transparent;
            border-top: 10px solid #3498db;

            margin-right: 14px;
        }

        QComboBox QAbstractItemView {
            background-color: white;

            border: 2px solid #dfe6e9;
            border-radius: 10px;

            padding: 8px;

            font-size: 20px;
            font-weight: bold;

            selection-background-color: #3498db;
            selection-color: white;

            outline: none;
        }
        """)
        self.price_mode.setStyleSheet("""
                QComboBox {
                    background-color: white;

                    border: 2px solid #dfe6e9;
                    border-radius: 14px;

                    padding: 14px 20px;
                    padding-right: 45px;

                    color: #2c3e50;

                    font-size: 24px;
                    font-weight: bold;
                    letter-spacing: 1px;
                }

                QComboBox:hover {
                    border: 2px solid #3498db;
                    background-color: #f8fbff;
                }

                QComboBox:focus {
                    border: 2px solid #2980b9;
                    background-color: #eef7ff;
                }

                QComboBox::drop-down {
                    border: none;
                    width: 45px;
                    background: transparent;
                }

                QComboBox::down-arrow {
                    image: none;

                    border-left: 8px solid transparent;
                    border-right: 8px solid transparent;
                    border-top: 10px solid #3498db;

                    margin-right: 14px;
                }

                QComboBox QAbstractItemView {
                    background-color: white;

                    border: 2px solid #dfe6e9;
                    border-radius: 10px;

                    padding: 8px;

                    font-size: 20px;
                    font-weight: bold;

                    selection-background-color: #3498db;
                    selection-color: white;

                    outline: none;
                }
                """)
        self.commission.setStyleSheet("""
        QDoubleSpinBox {
            background-color: white;

            border: 2px solid #f1c40f;
            border-radius: 14px;

            padding: 14px 18px;

            color: #2c3e50;

            font-size: 24px;
            font-weight: bold;
            letter-spacing: 1px;
        }

        QDoubleSpinBox:hover {
            border: 2px solid #f39c12;
            background-color: #fffdf5;
        }

        QDoubleSpinBox:focus {
            border: 2px solid #f39c12;
            background-color: #fffbea;
        }

        QDoubleSpinBox::up-button {
            subcontrol-origin: border;
            subcontrol-position: top right;

            width: 28px;

            border-left: 1px solid #f1c40f;
            border-bottom: 1px solid #f1c40f;

            border-top-right-radius: 12px;

            background-color: #fff8dc;
        }

        QDoubleSpinBox::up-button:hover {
            background-color: #fef3c7;
        }

        QDoubleSpinBox::down-button {
            subcontrol-origin: border;
            subcontrol-position: bottom right;

            width: 28px;

            border-left: 1px solid #f1c40f;

            border-bottom-right-radius: 12px;

            background-color: #fff8dc;
        }

        QDoubleSpinBox::down-button:hover {
            background-color: #fef3c7;
        }

        QDoubleSpinBox::up-arrow {
            image: none;

            width: 0px;
            height: 0px;

            border-left: 6px solid transparent;
            border-right: 6px solid transparent;
            border-bottom: 8px solid #f39c12;
        }

        QDoubleSpinBox::down-arrow {
            image: none;

            width: 0px;
            height: 0px;

            border-left: 6px solid transparent;
            border-right: 6px solid transparent;
            border-top: 8px solid #f39c12;
        }
        """)

        self.setLayout(main_layout)


        self.current_id = None

        self.article.returnPressed.connect(self.search_article)
        self.btn_save.clicked.connect(self.save_sale)
        self.load_article_suggestions()
        self.btn_clear.clicked.connect(self.clear_order)
        self.price_mode.currentTextChanged.connect(self.change_price_mode)
        self.method.currentTextChanged.connect(self.change_payment_method)
        self.commission.valueChanged.connect(self.change_commission)

    def change_commission(self):
        percent = self.commission.value()
        self.controller_pos.set_commission_percent(percent)
        self.refresh_totals()

    def change_payment_method(self, text):
        self.controller_pos.set_payment_method(text)
        self.controller_pos.set_commission_percent(self.commission.value())
        self.refresh_totals()
        if text == "TARJETA":
            self.commission.show()
        else:
            self.commission.hide()
        self.refresh_totals()

    def change_price_mode(self, text):
        if text == "MAYOREO":
            self.controller_pos.set_price_mode("LOYAL")
        else:
            self.controller_pos.set_price_mode("NORMAL")
        self.refresh_prices()

    def refresh_prices(self):
        cart = self.controller_pos.cart

        for row, item in enumerate(cart.values()):
            price = self.controller_pos._get_unit_price(item)
            subtotal = (price * item['quantity'])
            self.table.item(row, 3).setText(f"${float(price):.2f}")
            self.table.item(row, 4).setText(f"${float(subtotal):.2f}")
        self.refresh_totals()

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
            self.controller_pos.add_article(article)
            self.load_table()
            self.refresh_totals()
            QtCore.QTimer.singleShot(0, self.article.clear)

    def search_article(self):
        text = self.article.text().strip()
        if not text:
            return
        try:
            self.controller_pos.get_by_bar_code(text)
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
            self.controller_pos.update_quantity(article_id,quantity)
            self.load_table()
            self.refresh_totals()
        except:
            pass

    def increase_quantity(self, article_id):

        self.controller_pos.increase_quantity(article_id)

        self.load_table()
        self.refresh_totals()

    def decrease_quantity(self, article_id):
        self.controller_pos.decrease_quantity(article_id)
        self.load_table()
        self.refresh_totals()

    def delete_article(self, article_id):
        self.controller_pos.remove_article(article_id)
        self.load_table()
        self.refresh_totals()

    def save_sale(self):
        try:
            purchase = self.controller_pos.checkout()
            self.view_general.refresh()
            self.view_detail.refresh()
            QMessageBox.information(self, "Venta Generada", f"Venta #{purchase.id} guardada correctamente")
            self.table.setRowCount(0)
            self.article.clear()
            self.payment.clear()
            self.refresh_totals()
            self.method.setCurrentIndex(0)
            self.change.setText("CAMBIO: $0.00")
            self.article.setFocus()

        except ValueError as e:
            QMessageBox.warning(self, "Error", str(e))
        except Exception as e:
            QMessageBox.warning(self, "Error Crítico", str(e))

    def update_amounts(self):
        total = self.controller_pos.get_final_total()
        self.total.setText(f"TOTAL: ${float(total):.2f}")

    def update_change(self):
        text = self.payment.text().strip()
        if not text:
            self.change.setText("CAMBIO: $0.00")
            return
        try:
            amount_paid = float(text)
            self.controller_pos.set_amount_paid(amount_paid)
            change = self.controller_pos.calculate_change()
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
            price_text = float(self.table.item(row, 3).text().replace("$", "").strip())
            price = float(price_text)
            self.controller_pos.update_price(article_id,price)
            subtotal = (self.controller_pos.cart[article_id]['quantity'] * price)
            self.table.item(row,4).setText(f"${subtotal:.2f}")
            self.refresh_totals()

        except Exception as e:

            print(e)
        finally:
            self.table.blockSignals(False)

    def clear_order(self):

        response = QMessageBox.question(self, "Cancelar Venta", "¿Deseas cancelar la venta?", QMessageBox.Yes, QMessageBox.No)

        if response == QMessageBox.No:
            return

        self.controller_pos.clear_cart()
        self.table.setRowCount(0)
        self.article.clear()
        self.payment.clear()
        self.method.setCurrentIndex(0)
        self.refresh_totals()

    def refresh_totals(self):
        cart = self.controller_pos.cart
        for row, item in enumerate(cart.values()):
            price = self.controller_pos._get_unit_price(item)
            subtotal = (item['quantity'] * price)
            self.table.item(row,4).setText(f"${subtotal:.2f}")
        self.update_amounts()
        self.update_change()

        self.update_amounts()
        self.update_change()

    def load_table(self):

        self.loading_table = True
        cart = self.controller_pos.cart

        self.table.setRowCount(len(cart))

        for row, item in enumerate(cart.values()):
            price = self.controller_pos._get_unit_price(item)
            subtotal = (item['quantity'] * price)
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

            price_item = QTableWidgetItem(f"{float(price):.2f}")
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