from dataclasses import dataclass
from datetime import datetime



@dataclass
class StockMovement:
    id_article: int
    type: str
    quantity: float
    date: datetime | None = None
    id_reference: int | None = None
    id: int | None = None
    article_name: str | None = None

    def __str__(self):
        return f'Stock Movement: ID: {self.id}, ID Article: {self.id_article}, Type: {self.type}, Quantity: {self.quantity}, Date: {self.date}, Reference: {self.id_reference}'