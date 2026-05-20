from dataclasses import dataclass
from datetime import datetime


@dataclass
class Sale:
    total: float
    payment_method: str
    date: datetime | None = None
    id: int | None = None

    def __str__(self):
        return f'Sale:ID: {self.id}, Date: {self.date}, Total: {self.total}, Payment: {self.payment_method}'

@dataclass
class SaleBasic:
    date: datetime
    id: int | None = None
    def __str__(self):
        return f'Sale:ID: {self.id}, Total: {self.date}'