from PySide6.QtGui import QIcon, QAction
from PySide6.QtWidgets import QWidget, QStackedWidget, QVBoxLayout, QLabel, QPushButton, QApplication, QMenuBar, \
    QMainWindow, QTextEdit

from ui.articles_screen import ArticleScreen
from ui.categories_screen import CategoriesScreen
from ui.home_screen import HomeScreen
from ui.pop_screen import PopScreen
from ui.pos_screen import PosScreen
from ui.purchases_screen import PurchasesScreen
from ui.sales_screen import SalesScreen
from ui.stock_movement_screen import StockMovementScreen
from ui.suppliers_screen import SuppliersScreen


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        # Main configuration

        self.setWindowTitle("Sistema 'Abarrotes La Bodeguita'")
        self.setWindowIcon(QIcon('assets/main_icon.ico'))
        self.helpwindow = HelpWindow()
        self.home_screen = HomeScreen()
        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        # Screens
        self.home_screen = HomeScreen()
        self.categories = CategoriesScreen()
        self.suppliers = SuppliersScreen()
        self.articles = ArticleScreen()
        self.movements = StockMovementScreen()
        self.sales = SalesScreen()
        self.purchases = PurchasesScreen()
        self.pop_screen = PopScreen(self.purchases.view_general, self.purchases.view_detail)
        self.pos_screen = PosScreen(self.sales.view_general, self.sales.view_detail)

        # Stacks
        self.stack.addWidget(self.home_screen)
        self.stack.addWidget(self.categories)
        self.stack.addWidget(self.suppliers)
        self.stack.addWidget(self.articles)
        self.stack.addWidget(self.movements)
        self.stack.addWidget(self.sales)
        self.stack.addWidget(self.purchases)
        self.stack.addWidget(self.pop_screen)
        self.stack.addWidget(self.pos_screen)
        self.stack.currentChanged.connect(self.change_tab)


        # Connnected buttons
        self.home_screen.button_categories.clicked.connect(lambda: self.stack.setCurrentWidget(self.categories))
        self.home_screen.button_suppliers.clicked.connect(lambda: self.stack.setCurrentWidget(self.suppliers))
        self.home_screen.button_articles.clicked.connect(lambda: self.stack.setCurrentWidget(self.articles))
        self.home_screen.button_movements.clicked.connect(lambda: self.stack.setCurrentWidget(self.movements))
        self.home_screen.button_sales.clicked.connect(self.open_sales)
        self.home_screen.button_purchases.clicked.connect(self.open_purchase)
        self.home_screen.button_pop.clicked.connect(lambda: self.stack.setCurrentWidget(self.pop_screen))
        self.home_screen.button_pos.clicked.connect(lambda: self.stack.setCurrentWidget(self.pos_screen))

        self.add_menu_bar()

    def change_tab(self, index):
        current_widget = self.stack.widget(index)

        if hasattr(current_widget, 'reset_pagination'):
            current_widget.reset_pagination()

    def add_menu_bar(self):
        menu_bar = self.menuBar()
        screen_menu = menu_bar.addMenu('Vista')
        # Button
        button_home = screen_menu.addAction('Inicio')
        button_categories = screen_menu.addAction('Categorias')
        button_suppliers = screen_menu.addAction('Proveedores')
        button_articles = screen_menu.addAction('Artículos')
        button_movements = screen_menu.addAction('Movimientos')
        button_sales = screen_menu.addAction('Ventas')
        button_purchases = screen_menu.addAction('Compras')

        menu_sales = menu_bar.addMenu('Ventas')
        pos = menu_sales.addAction('Punto de Venta')
        action_general_sale = menu_sales.addAction('General')
        action_detail_sale = menu_sales.addAction('Detalle')

        action_detail_sale.triggered.connect(self.open_sales_detail)
        action_general_sale.triggered.connect(self.open_sales_general)
        pos.triggered.connect(lambda: self.stack.setCurrentWidget(self.pos_screen))


        menu_purchases = menu_bar.addMenu('Compras')
        pop = menu_purchases.addAction('Punto de Compra')
        action_general_purchase = menu_purchases.addAction('General')
        action_detail_purchase = menu_purchases.addAction('Detalle')

        action_detail_purchase.triggered.connect(self.open_purchases_detail)
        action_general_purchase.triggered.connect(self.open_purchases_general)
        pop.triggered.connect(lambda: self.stack.setCurrentWidget(self.pop_screen))


        # Connection
        button_home.triggered.connect(lambda: self.stack.setCurrentWidget(self.home_screen))
        button_categories.triggered.connect(lambda: self.stack.setCurrentWidget(self.categories))
        button_suppliers.triggered.connect(lambda: self.stack.setCurrentWidget(self.suppliers))
        button_articles.triggered.connect(lambda: self.stack.setCurrentWidget(self.articles))
        button_movements.triggered.connect(lambda: self.stack.setCurrentWidget(self.movements))
        button_sales.triggered.connect(self.open_sales)
        button_purchases.triggered.connect(self.open_purchase)

        help_menu = menu_bar.addMenu("Ayuda")
        button_info = QAction('Información', self)
        help_menu.addAction(button_info)
        button_info.triggered.connect(self.show_info)


    def show_info(self):
        if self.helpwindow.isVisible():
            self.helpwindow.hide()
        else:
            self.helpwindow.show()

    def open_sales(self):
        self.stack.setCurrentWidget(self.sales)
        self.sales.show_menu()
    def open_sales_general(self):
        self.stack.setCurrentWidget(self.sales)
        self.sales.show_sales_general()

    def open_sales_detail(self):
        self.stack.setCurrentWidget(self.sales)
        self.sales.show_sales_detail()

    def open_purchase(self):
        self.stack.setCurrentWidget(self.purchases)
        self.purchases.show_menu_purchase()

    def open_purchases_general(self):
        self.stack.setCurrentWidget(self.purchases)
        self.purchases.show_purchases_general()

    def open_purchases_detail(self):
        self.stack.setCurrentWidget(self.purchases)
        self.purchases.show_purchases_detail()

class HelpWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Ayuda")
        self.setFixedSize(500, 450)
        layout=QVBoxLayout()
        self.text = QTextEdit()
        self.text.setReadOnly(True)
        self.text.setText("""
Sistema de Gestión — Versión 1.0

Este sistema ha sido desarrollado para facilitar la administración de operaciones, permitiendo gestionar de manera eficiente categorías, movimientos y demás funciones clave del negocio en un solo lugar.

La aplicación está diseñada para ser intuitiva, rápida y práctica, con el objetivo de optimizar los procesos diarios y mejorar el control de la información.

Soporte y contacto
Para cualquier duda, aclaración o reporte de errores, favor de comunicarse con el responsable del sistema:

Nombre: Sebasthian Saldaña Pérez
Contacto: sebasthiansaldanaperez@gmail.com | 449 492 8553

Agradecemos su uso y confianza en este sistema.
        """)
        layout.addWidget(self.text)
        self.setLayout(layout)


#
# app = QApplication([])
# app.setWindowIcon(QIcon('assets/main_icon.png'))
# ventana = MainWindow()
# ventana.showMaximized()
# app.exec()