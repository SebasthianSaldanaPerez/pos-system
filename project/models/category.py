from dataclasses import dataclass

@dataclass
class Category:
    name: str
    active: bool = True
    id: int | None = None

    def __str__(self):
        return f'Category: ID: {self.id}, Name: {self.name}, Active: {self.active}'