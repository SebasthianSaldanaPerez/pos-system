from dao.article_dao import ArticleDAO
from dao.sale_dao import SaleDAO
from dao.sale_detail_dao import DetailSaleDAO
from models.sale import Sale
from services.stock_movement_service import StockMovementService


class SalesService:
    @staticmethod
    def get_sales(conn):
        return SaleDAO.select_all(conn)

    @staticmethod
    def get_sales_details(conn):
        return DetailSaleDAO.select_all(conn)

    @staticmethod
    def get_sales_by_id(sale_id: int, conn):
        if sale_id <= 0:
            raise ValueError('ID Inválido')
        sale = SaleDAO.select_by_id(sale_id, conn)
        if not sale:
            raise ValueError('Venta no encontrada')
        return sale

    @staticmethod
    def get_sale_details_by_sale_id(sale_id: int, conn):
        if sale_id <= 0:
            raise ValueError('ID Inválido')
        details = DetailSaleDAO.select_by_sales_id(sale_id, conn)
        return details if details else []

    @staticmethod
    def create_sale(sale: Sale, details: list, conn):
        if not details:
            raise ValueError('La venta debe tener al menos un artículo')
        try:
            total = 0
            articles_map = {}
            for d in details:
                if d.quantity <=0:
                    raise ValueError('Cantidad debe ser mayor a 0')
                if d.unit_price < 0:
                    raise ValueError('Precio inválido')
                article = ArticleDAO.select_by_id(d.article_id, conn)
                if not article:
                    raise ValueError(f'Articulo no encontrado: {d.article_id}')
                if article.stock < d.quantity:
                    raise ValueError('Sin disponibilidad de Stock')
                articles_map[d.article_id] = article
                d.subtotal = d.unit_price * d.quantity
                total += d.subtotal
            sale.total = total

            sale = SaleDAO.insert(sale, conn)

            for d in details:
                article = articles_map[d.article_id]
                d.sale_id = sale.id
                DetailSaleDAO.insert(d, conn)
                ArticleDAO.update_stock_sale(bar_code=article.bar_code, quantity=d.quantity, conn=conn)
                StockMovementService.register_sale_movement(id_article=article.id, quantity=d.quantity, sale_id=sale.id, conn=conn)
            conn.commit()
            return sale
        except Exception:
            conn.rollback()
            raise

    @staticmethod
    def get_all_paginated_sales(limit, offset, conn):
        return SaleDAO.get_all_paginated(limit, offset, conn)

    @staticmethod
    def get_all_paginated_sale_details(limit, offset, conn):
        return DetailSaleDAO.get_all_paginated(limit, offset, conn)