from dataclasses import dataclass


@dataclass
class Article:
    bar_code: str
    description : str
    purchase_price: float
    retail_price: float
    wholesale_price: float
    stock : float
    category_id : int
    active: bool = True
    id: int | None = None
    category_name: str | None = None

    def __str__(self):
        return (f'Article: ID: {self.id} Bar Code: {self.bar_code} Description: {self.description}, Purchase Price: {self.purchase_price} '
                f'Retail Price: {self.retail_price} Wholesale Price: {self.wholesale_price} Stock: {self.stock} Active: {self.active} Category: {self.category_id}')

