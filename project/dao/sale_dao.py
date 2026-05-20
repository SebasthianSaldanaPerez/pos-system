from psycopg2.extras import RealDictCursor

from models.sale import Sale


class SaleDAO:
    SELECT_ALL = 'SELECT id, date, total, payment_method FROM sales.sales ORDER BY id'
    SELECT_BY_ID = 'SELECT id, date, total, payment_method FROM sales.sales WHERE id = %s'
    INSERT = 'INSERT INTO sales.sales (total, payment_method) VALUES (%s, %s) RETURNING id, date'
    SELECT_PAGINATED = 'SELECT id, date, total, payment_method FROM sales.sales ORDER BY id DESC LIMIT %s OFFSET %s'

    @classmethod
    def select_all(cls, conn):
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(cls.SELECT_ALL)
            sales = cursor.fetchall()
            return [Sale(id=sale["id"], date=sale["date"], total=sale["total"], payment_method=sale["payment_method"]) for sale in sales]

    @classmethod
    def select_by_id(cls, sale_id: int, conn):
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(cls.SELECT_BY_ID, (sale_id,))
            sale = cursor.fetchone()
            if sale:
                return Sale(id=sale["id"], date=sale["date"], total=sale["total"], payment_method=sale["payment_method"])
            return None

    @classmethod
    def insert(cls, sale: Sale, conn):
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(cls.INSERT, (sale.total, sale.payment_method))
            row = cursor.fetchone()
            sale.id = row["id"]
            sale.date = row["date"]
            return sale


    @classmethod
    def get_all_paginated(cls, limit, offset, conn):
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(cls.SELECT_PAGINATED, (limit, offset))
            sales = cursor.fetchall()
            return [Sale(id=sale["id"], date=sale["date"], total=sale["total"], payment_method=sale["payment_method"]) for sale in sales]
