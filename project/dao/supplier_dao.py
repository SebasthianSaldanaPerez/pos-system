from psycopg2.extras import RealDictCursor

from models.supplier import Supplier


class SupplierDAO:
    SELECT_ALL = 'SELECT id, name, telephone_number, active FROM purchases.suppliers ORDER BY id'
    SELECT_BY_ID = 'SELECT id, name, telephone_number, active FROM purchases.suppliers WHERE id = %s'
    SELECT_BY_NAME = 'SELECT id, name, telephone_number, active FROM purchases.suppliers WHERE name = %s'
    INSERT = 'INSERT INTO purchases.suppliers (name, telephone_number, active) VALUES (%s, %s, %s) RETURNING id'
    UPDATE = 'UPDATE purchases.suppliers SET name = %s, telephone_number = %s, active = %s WHERE id = %s'
    SELECT_PAGINATED = 'SELECT id, name, telephone_number, active FROM purchases.suppliers ORDER BY id DESC LIMIT %s OFFSET %s'

    @classmethod
    def select_all(cls, conn):
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(cls.SELECT_ALL)
            suppliers = cursor.fetchall()
            return [Supplier(id=supplier['id'], name=supplier['name'], telephone_number=supplier['telephone_number'], active=supplier['active']) for supplier in suppliers]

    @classmethod
    def select_by_id(cls, supplier_id: int, conn):
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(cls.SELECT_BY_ID, (supplier_id, ))
            supplier = cursor.fetchone()
            if supplier:
                return Supplier(id=supplier['id'], name=supplier['name'], telephone_number=supplier['telephone_number'], active=supplier['active'])
            return None

    @classmethod
    def select_by_name(cls, supplier_name: str, conn):
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(cls.SELECT_BY_NAME, (supplier_name,))
            supplier = cursor.fetchone()
            if supplier:
                return Supplier(id=supplier['id'], name=supplier['name'], telephone_number=supplier['telephone_number'],
                                active=supplier['active'])
            return None

    @classmethod
    def insert(cls, supplier: Supplier, conn):
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(cls.INSERT, (supplier.name, supplier.telephone_number, supplier.active))
            new_id = cursor.fetchone()['id']
            supplier.id = new_id
            return supplier
    @classmethod
    def update(cls, supplier:Supplier, conn):
        with conn.cursor() as cursor:
            cursor.execute(cls.UPDATE, (supplier.name, supplier.telephone_number, supplier.active, supplier.id))
            return supplier

    @classmethod
    def get_all_paginated(cls, limit, offset, conn):
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(cls.SELECT_PAGINATED, (limit, offset))
            suppliers = cursor.fetchall()
            return [Supplier(id=supplier['id'], name=supplier['name'], telephone_number=supplier['telephone_number'],
                             active=supplier['active']) for supplier in suppliers]