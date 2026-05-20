from database.connection import Connection
from services.stock_movement_service import StockMovementService


class StockMovementController:

    @staticmethod
    def get_all():
        conn = Connection().get_connection()
        try:
            return StockMovementService.get_stock_movements(conn)
        finally:
            Connection().release_connections(conn)

    @staticmethod
    def get_by_id(stock_movement_id: int):
        conn = Connection().get_connection()
        try:
            return StockMovementService.get_stock_movement_by_id(stock_movement_id, conn)
        finally:
            Connection().release_connections(conn)

    @staticmethod
    def create_stock_movement(article_id, new_stock):
        conn = Connection().get_connection()
        try:
            return StockMovementService.register_adjustment(article_id, new_stock, conn)
        finally:
            Connection().release_connections(conn)

    @staticmethod
    def get_all_paginated(limit, offset):
        conn = Connection().get_connection()
        try:
            return StockMovementService.get_all_paginated(limit, offset, conn)
        finally:
            Connection().release_connections(conn)