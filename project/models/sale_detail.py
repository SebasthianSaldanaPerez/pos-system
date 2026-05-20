from dataclasses import dataclass
from datetime import datetime




@dataclass
class DetailSale:
    sale_id: int
    article_id: int
    quantity: float
    unit_price: float
    subtotal: float
    id: int | None = None
    article_description: str | None = None
    def __str__(self):
        return (f'Sale Datil: ID: {self.id}, ID Sale: {self.sale_id}, ID Article: {self.article_id} Quantity: {self.quantity}, '
                f'Unit Price: {self.unit_price} Subtotal: {self.subtotal}')