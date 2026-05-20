from dataclasses import dataclass
from datetime import datetime


@dataclass
class Purchase:
    supplier_id: int
    date: datetime | None = None
    total: float | None = None
    id: int | None = None
    supplier_name : str | None = None
    def __str__(self):
        return f'Purchase: ID: {self.id}, ID Supplier: {self.supplier_id}, Date: {self.date}, Total: {self.total}'

@dataclass
class PurchaseBasic:
    date: datetime
    id: int | None = None
    def __str__(self):
        return f'Purchase: ID: {self.id}, Total: {self.date}'