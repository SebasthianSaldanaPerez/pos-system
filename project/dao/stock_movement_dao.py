from psycopg2.extras import RealDictCursor

from models.stock_movement import StockMovement


class StockMovementDAO:
    SELECT_ALL = ('SELECT s.id, s.type, s.quantity, s.date, s.id_reference, a.id AS id_article, a.description AS article_name FROM inventory.stock_movements s JOIN inventory.articles a ON s.id_article = a.id '
                  'ORDER BY s.id')
    SELECT_BY_ID = ('SELECT s.id, s.type, s.quantity, s.date, s.id_reference, a.id AS id_article, a.name AS article_name FROM inventory.stock_movements s JOIN inventory.articles a ON s.id_article = a.id '
        'WHERE s.id = %s')
    INSERT = 'INSERT INTO inventory.stock_movements (id_article, type, quantity, id_reference) VALUES (%s, %s, %s, %s) RETURNING id'
    SELECT_PAGINATED = (
        'SELECT s.id, s.type, s.quantity, s.date, s.id_reference, a.id AS id_article, a.description AS article_name FROM inventory.stock_movements s JOIN inventory.articles a ON s.id_article = a.id '
        'ORDER BY s.id DESC LIMIT %s OFFSET %s')

    @staticmethod
    def _map_row(row):
        return StockMovement(
            id=row['id'],
            type=row['type'],
            quantity=row['quantity'],
            date=row['date'],
            id_reference=row['id_reference'],
            id_article=row['id_article'],
            article_name=row['article_name'],
        )

    @classmethod
    def select_all(cls, conn):
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(cls.SELECT_ALL)
            rows = cursor.fetchall()
            return [cls._map_row(row) for row in rows]

    @classmethod
    def select_by_id(cls, stock_movement_id, conn):
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(cls.SELECT_BY_ID, (stock_movement_id,))
            row = cursor.fetchone()
            return cls._map_row(row) if row else None

    @classmethod
    def insert(cls, stock_movement: StockMovement, conn):
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(cls.INSERT, (stock_movement.id_article, stock_movement.type, stock_movement.quantity, stock_movement.id_reference, ))
            stock_movement.id = cursor.fetchone()['id']
            return stock_movement

    @classmethod
    def get_all_paginated(cls, limit, offset, conn):
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(cls.SELECT_PAGINATED, (limit, offset))
            rows = cursor.fetchall()
            return [cls._map_row(row) for row in rows]