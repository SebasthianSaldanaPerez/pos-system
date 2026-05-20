from psycopg2.extras import RealDictCursor

from models.purchase import Purchase


class PurchaseDAO:
    SELECT_ALL = ('SELECT p.id, p.date, p.total, s.id AS supplier_id, s.name AS supplier_name '
                  'FROM purchases.purchases p JOIN purchases.suppliers s ON p.id_supplier = s.id ORDER BY p.id')
    SELECT_BY_ID = 'SELECT p.id, p.date, p.total, s.id AS supplier_id, s.name AS supplier_name FROM purchases.purchases p JOIN purchases.suppliers s ON p.id_supplier = s.id WHERE p.id = %s'
    INSERT = 'INSERT INTO purchases.purchases (id_supplier, total) VALUES (%s, %s) RETURNING id, date'
    SELECT_PAGINATED = ('SELECT p.id, p.date, p.total, s.id AS supplier_id, s.name AS supplier_name '
                  'FROM purchases.purchases p JOIN purchases.suppliers s ON p.id_supplier = s.id ORDER BY p.id DESC LIMIT %s OFFSET %s')

    @staticmethod
    def _map_row(row):
        return Purchase(
            id = row['id'],
            supplier_id = row['supplier_id'],
            supplier_name = row['supplier_name'],
            date = row['date'],
            total = row['total']
        )

    @classmethod
    def select_all(cls, conn):
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(cls.SELECT_ALL)
            rows = cursor.fetchall()
            return [cls._map_row(row) for row in rows]

    @classmethod
    def select_by_id(cls, purchase_id, conn):
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(cls.SELECT_BY_ID, (purchase_id,))
            row = cursor.fetchone()
            return cls._map_row(row) if row else None


    @classmethod
    def insert(cls, purchase: Purchase, conn):
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(cls.INSERT, (purchase.supplier_id, purchase.total))
            row = cursor.fetchone()
            purchase.id = row['id']
            purchase.date = row['date']
            return purchase

    @classmethod
    def get_all_paginated(cls, limit, offset, conn):
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(cls.SELECT_PAGINATED, (limit, offset))
            rows = cursor.fetchall()
            return [cls._map_row(row) for row in rows]