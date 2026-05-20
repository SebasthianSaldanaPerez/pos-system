from psycopg2.extras import RealDictCursor

from models.category import Category


class CategoryDAO:
    SELECT_ALL = 'SELECT id, name, active FROM inventory.categories ORDER BY id'
    SELECT_BY_ID = 'SELECT id, name, active FROM inventory.categories WHERE id=%s'
    SELECT_BY_NAME = 'SELECT id, name, active FROM inventory.categories WHERE name=%s'
    INSERT = 'INSERT INTO inventory.categories (name, active) VALUES (%s, %s) RETURNING id'
    UPDATE = 'UPDATE inventory.categories SET name = %s, active = %s WHERE id = %s'
    SELECT_PAGINATED = 'SELECT id, name, active FROM inventory.categories ORDER BY id DESC LIMIT %s OFFSET %s'

    @classmethod
    def select_all(cls, conn):
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(cls.SELECT_ALL)
            categories = cursor.fetchall()
            return [Category(id=category["id"], name=category["name"], active=category["active"]) for category in categories]

    @classmethod
    def select_by_id(cls, category_id: int, conn):
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(cls.SELECT_BY_ID, (category_id,))
            category = cursor.fetchone()
            if category:
                return Category(id=category["id"], name=category["name"], active=category["active"])
            return None

    @classmethod
    def select_by_name(cls, category_name: str, conn):
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(cls.SELECT_BY_NAME, (category_name,))
            category = cursor.fetchone()
            if category:
                return Category(id=category["id"], name=category["name"], active=category["active"])
            return None

    @classmethod
    def insert(cls, category: Category, conn):
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(cls.INSERT, (category.name, category.active))
            new_id = cursor.fetchone()["id"]
            category.id = new_id
            return category

    @classmethod
    def update(cls, category: Category, conn):
        with conn.cursor() as cursor:
            cursor.execute(cls.UPDATE, (category.name, category.active, category.id))
            return category

    @classmethod
    def get_all_paginated(cls, limit, offset, conn):
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(cls.SELECT_PAGINATED, (limit, offset))
            categories = cursor.fetchall()
            return [Category(id=category["id"], name=category["name"], active=category["active"]) for category in
                    categories]
