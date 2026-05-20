from models.purchase import Purchase
from models.purchase_detail import PurchaseDetail
from services.article_service import ArticleService
from services.purchase_service import PurchaseService


class PurchaseController:
    def __init__(self, conn):
        self.conn = conn
        self.cart = {}
        self.amount_paid = None
        self.supplier_id = None
        self.supplier_name = None

    def set_supplier(self, supplier_id: int, name: str):
        if not supplier_id:
            raise ValueError('Proveedor inválido')
        self.supplier_id = supplier_id
        self.supplier_name = name

    def get_by_bar_code(self, bar_code: str):
        article = ArticleService.get_article_by_bar_code(bar_code, self.conn)
        if not article:
            raise ValueError('Artículo no encontrado')

        if article.id in self.cart:
            self.cart[article.id]['quantity'] += 1
        else:
            self.cart[article.id] = {
                "article_id": article.id,
                "bar_code": article.bar_code,
                "description": article.description,
                "quantity": 1,
                "purchase_price": article.purchase_price,
            }

    def add_article(self, article):

        if article.id in self.cart:
            self.cart[article.id]['quantity'] += 1

        else:
            self.cart[article.id] = {
                "article_id": article.id,
                "bar_code": article.bar_code,
                "description": article.description,
                "quantity": 1,
                "purchase_price": article.purchase_price,
            }

    def remove_article(self, article_id: int):
        self.cart.pop(article_id, None)

    def increase_quantity(self, article_id: int):
        self.cart[article_id]['quantity'] += 1

    def decrease_quantity(self, article_id: int):
        self.cart[article_id]['quantity'] -= 1
        if self.cart[article_id]['quantity'] <= 0:
            self.remove_article(article_id)

    def update_quantity(self, article_id: int, quantity: int):
        if quantity <= 0:
            self.remove_article(article_id)
        else:
            self.cart[article_id]['quantity'] = quantity

    def get_total(self):
        total = sum(item['purchase_price']*item['quantity'] for item in self.cart.values())
        return float(total)

    def set_amount_paid(self, amount: float):
        self.amount_paid = amount

    def calculate_change(self):
        total = self.get_total()
        return float(self.amount_paid) - float(total)

    def clear_cart(self):
        self.cart.clear()
        self.supplier_id = None
        self.supplier_name = None

    def checkout(self):
        if not self.cart:
            raise ValueError('Carrito Vacío')
        if not self.supplier_id:
            raise ValueError('Debes seleccionar un proveedor')
        details=[
            PurchaseDetail(
                purchase_id=None,
                article_id=item['article_id'],
                quantity=item['quantity'],
                unit_price=item['purchase_price'],
                subtotal=None
            )
            for item in self.cart.values()
        ]
        purchase = Purchase(
            id=None,
            supplier_id=self.supplier_id,
            date=None,
            total=None,
        )
        purchase =PurchaseService.create_purchase(purchase, details, self.conn)
        self.clear_cart()
        return purchase

    def update_price(self, article_id, price):
        self.cart[article_id]['purchase_price'] = price