from models.article import Article
from models.sale import Sale
from models.sale_detail import DetailSale
from services.article_service import ArticleService
from services.sale_service import SalesService


class PosController:
    def __init__(self, conn):
        self.conn = conn
        self.cart = {}
        self.price_mode = 'NORMAL'
        self.payment_method = 'EFECTIVO'
        self.amount_paid = None
        self.commission_percent = 0

    def set_payment_method(self, method: str):
        if method not in ('EFECTIVO', 'TARJETA', 'TRANSFERENCIA'):
            raise ValueError('Método de pago inválido')
        self.payment_method = method

    def set_price_mode(self, mode: str):
        if mode not in ('NORMAL', 'LOYAL'):
            raise ValueError('Modo de precio inválido')
        self.price_mode = mode

    def _get_unit_price(self, item):
        if self.price_mode == 'LOYAL':
            return item['price_loyal']
        return item['price_normal']

    def get_by_bar_code(self, bar_code: str):
        article = ArticleService.get_article_by_bar_code(bar_code, self.conn)

        if not article:
            raise ValueError('Artículo no encontrado')

        if article.id in self.cart:
            self.cart[article.id]['quantity'] += 1
        else:
            self.cart[article.id] = {
                "article_id": article.id,
                "bar_code": bar_code,
                "description": article.description,
                "quantity": 1,
                "price_normal": article.retail_price,
                "price_loyal": article.wholesale_price,
            }

    def add_article(self, article: Article):
        if article.id in self.cart:
            self.cart[article.id]['quantity'] += 1
        else:
            self.cart[article.id] = {
                "article_id": article.id,
                "bar_code": article.bar_code,
                "description": article.description,
                "quantity": 1,
                "price_normal": article.retail_price,
                "price_loyal": article.wholesale_price,
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
        return sum(float(self._get_unit_price(item))* item['quantity']for item in self.cart.values())

    def set_amount_paid(self, amount: float):
        self.amount_paid = float(amount)

    def calculate_change(self):
        total = self.get_final_total()
        return self.amount_paid - total

    def clear_cart(self):
        self.cart.clear()

    def checkout(self):
        if not self.cart:
            raise ValueError('Carrito vacío')

        if not self.payment_method:
            raise ValueError('Selecciona un método de pago')

        details = [
            DetailSale(
                sale_id=None,
                article_id=item['article_id'],
                quantity=item['quantity'],
                unit_price=self._get_unit_price(item),
                subtotal=None
            )
            for item in self.cart.values()
        ]

        sale = Sale(
            id=None,
            total=0,
            date=None,
            payment_method=self.payment_method,
        )
        sale = SalesService.create_sale(sale, details, self.conn)
        self.clear_cart()
        return sale

    def update_price(self, article_id, price):
        if self.price_mode == 'LOYAL':
            self.cart[article_id]['price_loyal'] = price
        else:
            self.cart[article_id]['price_normal'] = price

    def get_final_total(self):
        total = self.get_total()
        if self.payment_method == "TARJETA":
            commission = (total * (self.commission_percent / 100))
            total += commission
        return total

    def set_commission_percent(self, percent):
        self.commission_percent = percent