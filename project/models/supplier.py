from dataclasses import dataclass


@dataclass
class Supplier:
    name: str
    telephone_number: str
    active: bool = True
    id: int | None = None
    def __str__(self):
        return f'Supplier: ID: {self.id}, Name: {self.name}, Telephone: {self.telephone_number} Active: {self.active}'

@dataclass
class SupplierBasic:
    name: str
    id: int | None = None

    def __str__(self):
        return f'Supplier: ID: {self.id}, Name: {self.name}'