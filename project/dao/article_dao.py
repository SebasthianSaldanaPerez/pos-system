from psycopg2.extras import RealDictCursor

from models.article import Article


class ArticleDAO:
    SELECT_ALL = ('SELECT a.id, a.bar_code, a.description, a.purchase_price, a.retail_price, a.wholesale_price, a.stock, a.active, c.id AS category_id, c.name AS category_name '
                  'FROM inventory.articles a JOIN inventory.categories c ON a.category_id = c.id ORDER BY a.id')
    SELECT_BY_ID = ('SELECT a.id, a.bar_code, a.description, a.purchase_price, a.retail_price, a.wholesale_price, a.stock, a.active, c.id AS category_id, c.name AS category_name '
                  'FROM inventory.articles a JOIN inventory.categories c ON a.category_id = c.id WHERE a.id = %s')
    SELECT_BY_BAR_CODE = ('SELECT a.id, a.bar_code, a.description, a.purchase_price, a.retail_price, a.wholesale_price, a.stock, a.active, c.id AS category_id, c.name AS category_name '
                  'FROM inventory.articles a JOIN inventory.categories c ON a.category_id = c.id WHERE a.bar_code = %s AND a.active = true')
    SELECT_BY_DESCRIPTION = ('SELECT a.id, a.bar_code, a.description, a.purchase_price, a.retail_price, a.wholesale_price, a.stock, a.active, c.id AS category_id, c.name AS category_name '
                  'FROM inventory.articles a JOIN inventory.categories c ON a.category_id = c.id WHERE a.description LIKE %s AND a.active = true')
    INSERT = ('INSERT INTO inventory.articles (bar_code, description, purchase_price, retail_price, wholesale_price, stock, active, category_id) '
              'VALUES (%s, %s, %s, %s, %s, %s, %s, %s) RETURNING id')
    UPDATE = ('UPDATE inventory.articles SET bar_code = %s, description = %s, purchase_price = %s, '
              'retail_price = %s, wholesale_price = %s, stock = %s, active = %s, category_id = %s WHERE id = %s')
    UPDATE_STOCK_SALE = 'UPDATE inventory.articles SET stock = stock - %s WHERE bar_code = %s AND stock >= %s'
    UPDATE_STOCK_PURCHASE = 'UPDATE inventory.articles SET stock = stock + %s WHERE bar_code = %s'
    UPDATE_STOCK_ADJUSTMENT = 'UPDATE inventory.articles SET stock =  %s WHERE id = %s'
    SELECT_PAGINATED = ('SELECT a.id, a.bar_code, a.description, a.purchase_price, a.retail_price, a.wholesale_price, a.stock, a.active, c.id AS category_id, c.name AS category_name '
                  'FROM inventory.articles a JOIN inventory.categories c ON a.category_id = c.id ORDER BY a.id DESC LIMIT %s OFFSET %s')

    @staticmethod
    def _map_row(row):
        return Article(
            id=row["id"],
            bar_code=row['bar_code'],
            description=row['description'],
            purchase_price=row['purchase_price'],
            retail_price=row['retail_price'],
            wholesale_price=row['wholesale_price'],
            stock=row['stock'],
            active=row['active'],
            category_id=row['category_id'],
            category_name=row['category_name']
        )


    @classmethod
    def select_all(cls, conn):
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(cls.SELECT_ALL)
            rows = cursor.fetchall()
            return [cls._map_row(row) for row in rows]

    @classmethod
    def select_by_id(cls, article_id: int, conn):
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(cls.SELECT_BY_ID, (article_id,))
            row = cursor.fetchone()
            return cls._map_row(row) if row else None

    @classmethod
    def select_by_bar_code(cls, article_bar_code: str, conn):
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(cls.SELECT_BY_BAR_CODE, (article_bar_code,))
            row = cursor.fetchone()
            return cls._map_row(row) if row else None

    @classmethod
    def select_by_description(cls, article_description: str, conn):
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(cls.SELECT_BY_DESCRIPTION, (f"%{article_description}%",))
            rows = cursor.fetchall()
            return [cls._map_row(row) for row in rows]

    @classmethod
    def insert(cls, article: Article, conn):
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(cls.INSERT, (article.bar_code, article.description, article.purchase_price, article.retail_price, article.wholesale_price
                                        , article.stock, article.active, article.category_id))
            article.id = cursor.fetchone()['id']
            return article

    @classmethod
    def update(cls, article: Article, conn):
        with conn.cursor() as cursor:
            cursor.execute(cls.UPDATE, (article.bar_code, article.description, article.purchase_price, article.retail_price, article.wholesale_price,
                                        article.stock, article.active, article.category_id, article.id))
            return article

    @classmethod
    def update_stock_sale(cls, bar_code:str, quantity:float, conn):
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(cls.UPDATE_STOCK_SALE, (quantity, bar_code, quantity))
            if cursor.rowcount == 0:
                raise Exception('Stock insuficiente')

    @classmethod
    def update_stock_purchase(cls, bar_code:str, quantity:float, conn):
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(cls.UPDATE_STOCK_PURCHASE, (quantity, bar_code))

    @classmethod
    def update_stock_adjustment(cls, new_stock, article_id, conn):
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(cls.UPDATE_STOCK_ADJUSTMENT, (new_stock, article_id))

    @classmethod
    def get_all_paginated(cls, limit, offset, conn):
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(cls.SELECT_PAGINATED, (limit, offset))
            rows = cursor.fetchall()
            return [cls._map_row(row) for row in rows]