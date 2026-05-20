from psycopg2.extras import RealDictCursor

from models.sale_detail import DetailSale


class DetailSaleDAO:
    SELECT_ALL = ('SELECT d.id, d.quantity, d.unit_price, d.subtotal, s.id AS id_sale, s.date AS sale_date, a.id AS id_article, a.description AS '
                  'article_description, a.retail_price AS article_retail_price, a.wholesale_price AS article_wholesale_price  FROM sales.details_sales d '
                  'JOIN sales.sales s ON d.id_sale = s.id JOIN inventory.articles a ON d.id_article = a.id ORDER BY d.id')
    SELECT_BY_ID = ('SELECT d.id, d.quantity, d.unit_price, d.subtotal, s.id AS id_sale, s.date AS sale_date, a.id AS id_article, a.description AS '
                  'article_description, a.retail_price AS article_retail_price, a.wholesale_price AS article_wholesale_price  FROM sales.details_sales d '
                  'JOIN sales.sales s ON d.id_sale = s.id JOIN inventory.articles a ON d.id_article = a.id WHERE d.id = %s')
    SELECT_BY_SALES_ID = ('SELECT d.id, d.quantity, d.unit_price, d.subtotal, s.id AS id_sale, s.date AS sale_date, a.id AS id_article, a.description AS '
                  'article_description, a.retail_price AS article_retail_price, a.wholesale_price AS article_wholesale_price  FROM sales.details_sales d '
                  'JOIN sales.sales s ON d.id_sale = s.id JOIN inventory.articles a ON d.id_article = a.id WHERE d.id_sale = %s')
    INSERT = 'INSERT INTO sales.details_sales (id_sale, id_article, quantity, unit_price, subtotal) VALUES (%s, %s, %s, %s, %s) RETURNING id'
    SELECT_PAGINATED = (
        'SELECT d.id, d.quantity, d.unit_price, d.subtotal, s.id AS id_sale, s.date AS sale_date, a.id AS id_article, a.description AS '
        'article_description, a.retail_price AS article_retail_price, a.wholesale_price AS article_wholesale_price  FROM sales.details_sales d '
        'JOIN sales.sales s ON d.id_sale = s.id JOIN inventory.articles a ON d.id_article = a.id ORDER BY d.id DESC LIMIT %s OFFSET %s')


    @staticmethod
    def _map_row(row):
        return DetailSale(
            id = row['id'],
            sale_id = row['id_sale'],
            article_id=row['id_article'],
            article_description = row['article_description'],
            quantity = row['quantity'],
            unit_price = row['unit_price'],
            subtotal = row['subtotal'],
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
            return cls._map_row(row) if row else None

    @classmethod
    def select_by_sales_id(cls, sale_id, conn):
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(cls.SELECT_BY_SALES_ID, (sale_id,))
            values = cursor.fetchall()
            details = []
            for row in values:
                detail = DetailSale(id=row['id'], sale_id=row['id_sale'], article_id=row['id_sale'], quantity=row['quantity'],
                                    unit_price=row['unit_price'], subtotal=row['subtotal'], article_description=row['article_description'],)
                details.append(detail)
            return details

    @classmethod
    def insert(cls, detail: DetailSale, conn):
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(cls.INSERT, (detail.sale_id, detail.article_id, detail.quantity, detail.unit_price, detail.subtotal))
            detail.id = cursor.fetchone()['id']
            return detail

    @classmethod
    def get_all_paginated(cls, limit, offset, conn):
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(cls.SELECT_PAGINATED, (limit, offset))
            rows = cursor.fetchall()
            return [cls._map_row(row) for row in rows]