from dao.article_dao import ArticleDAO
from dao.purchase_dao import PurchaseDAO
from dao.purchase_detail_dao import PurchaseDetailDAO
from dao.supplier_dao import SupplierDAO
from models.purchase import Purchase
from services.stock_movement_service import StockMovementService


class PurchaseService:
    @staticmethod
    def get_purchases(conn):
        return PurchaseDAO.select_all(conn)

    @staticmethod
    def get_purchases_details(conn):
        return PurchaseDetailDAO.select_all(conn)

    @staticmethod
    def get_purchase_by_id(purchase_id : int, conn):
        if purchase_id <= 0:
            raise ValueError('ID Inválido')
        purchase = PurchaseDAO.select_by_id(purchase_id, conn)
        if not purchase:
            raise ValueError('Compra no encontrada')
        return purchase

    @staticmethod
    def get_purchase_details_by_purchase_id(purchase_id: int, conn):
        if purchase_id <= 0:
            raise ValueError('ID Inválido')
        details = PurchaseDetailDAO.select_by_purchase_id(purchase_id, conn)
        return details if details else []

    @staticmethod
    def create_purchase(purchase: Purchase, details:list, conn):
        if not details:
            raise ValueError('La compra debe tener al menos un artículo')
        supplier = SupplierDAO.select_by_id(purchase.supplier_id, conn)
        if not supplier:
            raise ValueError('Proveedor no encontrado')
        try:
            total = 0
            for d in details:
                if d.quantity <= 0:
                    raise ValueError('Cantidad debe ser mayor a 0')
                if d.unit_price <= 0:
                    raise ValueError('Precio inválido')
                d.subtotal = d.unit_price * d.quantity
                total += d.subtotal
            purchase.total = total

            purchase = PurchaseDAO.insert(purchase, conn)

            for d in details:
                article = ArticleDAO.select_by_id(d.article_id, conn)
                if not article:
                    raise ValueError(f'Artículo no encontrado: {d.article_id}')
                d.purchase_id = purchase.id
                PurchaseDetailDAO.insert(d, conn)
                ArticleDAO.update_stock_purchase(bar_code=article.bar_code, quantity=d.quantity, conn=conn)
                StockMovementService.register_purchase_movement(id_article=article.id, quantity=d.quantity, purchase_id=purchase.id, conn=conn)
            conn.commit()
            return purchase
        except Exception:
            conn.rollback()
            raise

    @staticmethod
    def get_all_paginated_purchases(limit, offset, conn):
        return PurchaseDAO.get_all_paginated(limit, offset, conn)

    @staticmethod
    def get_all_paginated_purchase_details(limit, offset, conn):
        return PurchaseDetailDAO.get_all_paginated(limit, offset, conn)