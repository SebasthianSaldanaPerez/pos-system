import os
import sys

from PySide6.QtCore import QSize
from PySide6.QtGui import QIcon, QPixmap, Qt
from PySide6.QtWidgets import QLabel, QWidget, QVBoxLayout, QToolButton, QHBoxLayout



class HomeScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.buttons()


        main_layout = QHBoxLayout()
        main_layout.setSpacing(20)

        # Buttons
        buttons_container = QWidget()
        layout_buttons = QVBoxLayout()
        layout_buttons.setSpacing(30)

        row1 = QHBoxLayout()
        row2 = QHBoxLayout()
        row3 = QHBoxLayout()
        row4 = QHBoxLayout()

        row1.setSpacing(20)
        row2.setSpacing(20)
        row3.setSpacing(20)
        row4.setSpacing(20)

        row1.setAlignment(Qt.AlignCenter)
        row2.setAlignment(Qt.AlignCenter)
        row3.setAlignment(Qt.AlignCenter)
        row4.setAlignment(Qt.AlignCenter)

        row1.addWidget(self.button_categories)
        row1.addWidget(self.button_suppliers)

        row2.addWidget(self.button_articles)
        row2.addWidget(self.button_movements)

        row3.addWidget(self.button_sales)
        row3.addWidget(self.button_purchases)

        row4.addWidget(self.button_pos)
        row4.addWidget(self.button_pop)

        layout_buttons.addStretch()
        layout_buttons.addLayout(row1)
        layout_buttons.addLayout(row2)
        layout_buttons.addLayout(row3)
        layout_buttons.addLayout(row4)
        layout_buttons.addStretch()

        buttons_container.setLayout(layout_buttons)

        background = QWidget()

        layout_background = QVBoxLayout()

        image_route = self.get_asset('ui/assets/bodeguita.png')
        pixmap = QPixmap(image_route)
        image = QLabel()
        image.setPixmap(pixmap)
        image.setScaledContents(True)
        image.setFixedSize(700,700)

        image.setAlignment(Qt.AlignCenter)

        layout_background.addStretch()
        layout_background.addWidget(image, alignment=Qt.AlignCenter)
        layout_background.addStretch()
        background.setLayout(layout_background)

        main_layout.addWidget(buttons_container, 0)
        main_layout.addWidget(background, 3)
        self.setLayout(main_layout)

    def buttons(self):
        self.button_categories = QToolButton()
        self.button_categories.setFixedSize(160,160)
        self.button_categories.setText("Categorías")
        self.button_categories.setIcon(QIcon(self.get_asset('ui/assets/categories.png')))
        self.button_categories.setIconSize(QSize(64, 64))
        self.button_categories.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextUnderIcon)
        self.button_categories.setStyleSheet("""
            QToolButton {
                border: 1px solid #ccc;
                border-radius: 10px;
                padding: 10px;
                padding-top: 25px;
                background-color: white;
            }
            QToolButton:hover {
                background-color: #f0f0f0;
            }
        """)

        self.button_articles = QToolButton()
        self.button_articles.setFixedSize(160,160)
        self.button_articles.setText("Artículos")
        self.button_articles.setIcon(QIcon(self.get_asset('ui/assets/articles.png')))
        self.button_articles.setIconSize(QSize(64, 64))
        self.button_articles.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextUnderIcon)
        self.button_articles.setStyleSheet("""
                    QToolButton {
                        border: 1px solid #ccc;
                        border-radius: 10px;
                        padding: 10px;
                        padding-top: 25px;
                        background-color: white;
                    }
                    QToolButton:hover {
                        background-color: #f0f0f0;
                    }
                """)

        self.button_movements = QToolButton()
        self.button_movements.setFixedSize(160,160)
        self.button_movements.setText("Movimientos")
        self.button_movements.setIcon(QIcon(self.get_asset('ui/assets/movements.png')))
        self.button_movements.setIconSize(QSize(64, 64))
        self.button_movements.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextUnderIcon)
        self.button_movements.setStyleSheet("""
                            QToolButton {
                                border: 1px solid #ccc;
                                border-radius: 10px;
                                padding: 10px;
                                padding-top: 25px;
                                background-color: white;
                            }
                            QToolButton:hover {
                                background-color: #f0f0f0;
                            }
                        """)


        self.button_suppliers = QToolButton()
        self.button_suppliers.setFixedSize(160,160)
        self.button_suppliers.setText("Proveedores")
        self.button_suppliers.setIcon(QIcon(self.get_asset('ui/assets/suppliers.png')))
        self.button_suppliers.setIconSize(QSize(64, 64))
        self.button_suppliers.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextUnderIcon)
        self.button_suppliers.setStyleSheet("""
                                            QToolButton {
                                                border: 1px solid #ccc;
                                                border-radius: 10px;
                                                padding: 10px;
                                                padding-top: 25px;
                                                background-color: white;
                                            }
                                            QToolButton:hover {
                                                background-color: #f0f0f0;
                                            }
                                        """)

        self.button_sales = QToolButton()
        self.button_sales.setFixedSize(160,160)
        self.button_sales.setText("Ventas")
        self.button_sales.setIcon(QIcon(self.get_asset('ui/assets/sales.png')))
        self.button_sales.setIconSize(QSize(64, 64))
        self.button_sales.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextUnderIcon)
        self.button_sales.setStyleSheet("""
                                            QToolButton {
                                                border: 1px solid #ccc;
                                                border-radius: 10px;
                                                padding: 10px;
                                                padding-top: 25px;
                                                background-color: white;
                                            }
                                            QToolButton:hover {
                                                background-color: #f0f0f0;
                                            }
                                        """)

        self.button_purchases = QToolButton()
        self.button_purchases.setFixedSize(160, 160)
        self.button_purchases.setText("Compras")
        self.button_purchases.setIcon(QIcon(self.get_asset('ui/assets/purchases.png')))
        self.button_purchases.setIconSize(QSize(64, 64))
        self.button_purchases.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextUnderIcon)
        self.button_purchases.setStyleSheet("""
                                                    QToolButton {
                                                        border: 1px solid #ccc;
                                                        border-radius: 10px;
                                                        padding: 10px;
                                                        padding-top: 25px;
                                                        background-color: white;
                                                    }
                                                    QToolButton:hover {
                                                        background-color: #f0f0f0;
                                                    }
                                                """)

        self.button_pos = QToolButton()
        self.button_pos.setFixedSize(160, 160)
        self.button_pos.setText("Punto de Venta")
        self.button_pos.setIcon(QIcon(self.get_asset('ui/assets/pos.png')))
        self.button_pos.setIconSize(QSize(64, 64))
        self.button_pos.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextUnderIcon)
        self.button_pos.setStyleSheet("""
                                                            QToolButton {
                                                                border: 1px solid #ccc;
                                                                border-radius: 10px;
                                                                padding: 10px;
                                                                padding-top: 25px;
                                                                background-color: white;
                                                            }
                                                            QToolButton:hover {
                                                                background-color: #f0f0f0;
                                                            }
                                                        """)

        self.button_pop = QToolButton()
        self.button_pop.setFixedSize(160, 160)
        self.button_pop.setText("Punto de Compra")
        self.button_pop.setIcon(QIcon(self.get_asset('ui/assets/pop.png')))
        self.button_pop.setIconSize(QSize(64, 64))
        self.button_pop.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextUnderIcon)
        self.button_pop.setStyleSheet("""
                                                                    QToolButton {
                                                                        border: 1px solid #ccc;
                                                                        border-radius: 10px;
                                                                        padding: 10px;
                                                                        padding-top: 25px;
                                                                        background-color: white;
                                                                    }
                                                                    QToolButton:hover {
                                                                        background-color: #f0f0f0;
                                                                    }
                                                                """)

    def get_asset(self, relative_path):
        if hasattr(sys, '_MEIPASS'):
            return os.path.join(sys._MEIPASS, relative_path)
        return os.path.join(os.path.abspath("."), relative_path)
