from dao.article_dao import ArticleDAO
from dao.stock_movement_dao import StockMovementDAO
from models.stock_movement import StockMovement


class StockMovementService:
    @staticmethod
    def get_stock_movements(conn):
        return StockMovementDAO.select_all(conn)

    @staticmethod
    def get_stock_movement_by_id(stock_movement_id: int, conn):
        if stock_movement_id <= 0:
            raise ValueError('ID inválido')
        stock_movement = StockMovementDAO.select_by_id(stock_movement_id, conn)
        if not stock_movement:
            raise ValueError('Movimiento no Encontrado')
        return stock_movement


    @staticmethod
    def register_adjustment(id_article: int, new_stock: float, conn):

        if new_stock < 0:
            raise ValueError('Stock no puede ser negativo')

        article = ArticleDAO.select_by_id(id_article, conn)
        if not article:
            raise ValueError('Articulo no encontrado')

        current_stock = article.stock
        difference = new_stock - current_stock

        if difference == 0:
            return None

        try:
            ArticleDAO.update_stock_adjustment(new_stock, id_article, conn)
            movement = StockMovement(id_article=id_article, type='AJUSTE', quantity=abs(difference), id_reference=None)
            result = StockMovementDAO.insert(movement,conn)
            conn.commit()
            return result
        except Exception:
            conn.rollback()
            raise


    @staticmethod
    def register_purchase_movement(id_article:int, quantity:float, purchase_id:int, conn):
        if quantity <= 0:
            raise ValueError('Cantidad mayor a 0')
        movement = StockMovement(id_article=id_article, type='COMPRA', quantity=quantity, id_reference=purchase_id)
        return StockMovementDAO.insert(movement, conn)


    @staticmethod
    def register_sale_movement(id_article:int, quantity:float, sale_id:int, conn):
        if quantity <= 0:
            raise ValueError('Cantidad mayor a 0')
        movement = StockMovement(id_article=id_article, type='VENTA', quantity=quantity,id_reference=sale_id)
        return StockMovementDAO.insert(movement, conn)

    @staticmethod
    def get_all_paginated(limit, offset, conn):
        return StockMovementDAO.get_all_paginated(limit, offset, conn)