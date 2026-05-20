from dataclasses import dataclass



@dataclass
class PurchaseDetail:
    purchase_id: int
    article_id: int
    quantity: float
    unit_price: float
    subtotal: float
    id: int | None = None
    article_description : str | None = None
    def __str__(self):
        return (f'Purchase Detail: ID {self.id}, ID Purchase: {self.purchase_id}, ID Article: {self.article_id}, '
                f'Quantity: {self.quantity}, Unit Price: {self.unit_price}, Subtotal: {self.subtotal}')