from psycopg2.extras import RealDictCursor

from models.purchase_detail import PurchaseDetail


class PurchaseDetailDAO:
    SELECT_ALL = ('SELECT d.id, d.quantity, d.unit_price, d.subtotal, p.id AS id_purchase, p.date AS purchase_date, a.id AS id_article, a.description AS '
                  'article_description, a.purchase_price AS article_purchase_price '
                  'FROM purchases.details_purchases d JOIN purchases.purchases p ON d.id_purchase = p.id JOIN inventory.articles a ON d.id_article = a.id ORDER BY d.id')
    SELECT_BY_ID = ('SELECT d.id, d.quantity, d.unit_price, d.subtotal, p.id AS id_purchase, p.date AS purchase_date, a.id AS id_article, a.description AS '
                  'article_description, a.purchase_price AS article_purchase_price '
                  'FROM purchases.details_purchases d JOIN purchases.purchases p ON d.id_purchase = p.id JOIN inventory.articles a ON d.id_article = a.id WHERE d.id = %s')
    SELECT_BY_PURCHASE_ID = ('SELECT d.id, d.quantity, d.unit_price, d.subtotal, p.id AS id_purchase, p.date AS purchase_date, a.id AS id_article, a.description AS '
                  'article_description, a.purchase_price AS article_purchase_price '
                  'FROM purchases.details_purchases d JOIN purchases.purchases p ON d.id_purchase = p.id JOIN inventory.articles a ON d.id_article = a.id WHERE d.id_purchase = %s')
    INSERT = 'INSERT INTO purchases.details_purchases (id_purchase, id_article, quantity, unit_price, subtotal) VALUES (%s, %s, %s, %s, %s) RETURNING id'
    SELECT_PAGINATED = (
        'SELECT d.id, d.quantity, d.unit_price, d.subtotal, p.id AS id_purchase, p.date AS purchase_date, a.id AS id_article, a.description AS '
        'article_description, a.purchase_price AS article_purchase_price '
        'FROM purchases.details_purchases d JOIN purchases.purchases p ON d.id_purchase = p.id JOIN inventory.articles a ON d.id_article = a.id ORDER BY d.id DESC LIMIT %s OFFSET %s')

    @staticmethod
    def _map_row(row):
        return PurchaseDetail(
            id=row['id'],
            purchase_id=row['id_purchase'],
            article_id=row['id_article'],
            article_description=row['article_description'],
            quantity=row['quantity'],
            unit_price=row['unit_price'],
            subtotal=row['subtotal'],
        )

    @classmethod
    def select_all(cls, conn):
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(cls.SELECT_ALL)
            rows = cursor.fetchall()
            return [cls._map_row(row) for row in rows]

    @classmethod
    def select_by_id(cls, detail_id, conn):
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(cls.SELECT_BY_ID, (detail_id,))
            row = cursor.fetchone()
            return cls._map_row(row)

    @classmethod
    def select_by_purchase_id(cls, id_purchase, conn):
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(cls.SELECT_BY_PURCHASE_ID, (id_purchase,))
            values = cursor.fetchall()
            details = []
            for row in values:
                detail = PurchaseDetail(id=row['id'], purchase_id=row['id_purchase'], article_id=row['id_article'],
                                        quantity=row['quantity'], unit_price=row['unit_price'],
                                        subtotal=row['subtotal'], article_description=row['article_description'],)
                details.append(detail)
            return details

    @classmethod
    def insert(cls, detail: PurchaseDetail, conn):
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(cls.INSERT, (detail.purchase_id, detail.article_id, detail.quantity, detail.unit_price, detail.subtotal))
            detail.id = cursor.fetchone()['id']
            return detail

    @classmethod
    def get_all_paginated(cls, limit, offset, conn):
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(cls.SELECT_PAGINATED, (limit, offset))
            rows = cursor.fetchall()
            return [cls._map_row(row) for row in rows]