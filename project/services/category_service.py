from dao.category_dao import CategoryDAO
from models.category import Category


class CategoryService:

    @staticmethod
    def get_categories(conn):
        return  CategoryDAO.select_all(conn)

    @staticmethod
    def get_category_by_id(category_id: int, conn):
        if category_id <=0:
            raise ValueError('ID inválido')
        category = CategoryDAO.select_by_id(category_id, conn)
        if not category:
            raise ValueError('Categoría no encontrada')
        return category

    @staticmethod
    def create_category(category: Category, conn):
        if not category.name or not category.name.strip():
            raise ValueError('El nombre debe ser obligatorio')
        category.name = category.name.strip()
        existing = CategoryDAO.select_by_name(category.name, conn)
        if existing:
            raise ValueError('La categoria ya existe')
        try:
            result = CategoryDAO.insert(category, conn)
            conn.commit()
            return result
        except Exception:
            conn.rollback()
            raise

    @staticmethod
    def update_category(category: Category, conn):
        if not category.id or category.id <=0:
            raise ValueError('El ID debe ser obligatorio')
        if not category.name or not category.name.strip():
            raise ValueError('El nombre debe ser obligatorio')
        existing = CategoryDAO.select_by_id(category.id, conn)
        if not existing:
            raise ValueError('La categoria no existe')
        duplicate = CategoryDAO.select_by_name(category.name, conn)
        if duplicate and duplicate.id != category.id:
            raise ValueError('La categoria ya existe')
        try:
            result = CategoryDAO.update(category, conn)
            conn.commit()
            return result
        except Exception:
            conn.rollback()
            raise

    @staticmethod
    def get_all_paginated(limit, offset, conn):
        return CategoryDAO.get_all_paginated(limit, offset, conn)