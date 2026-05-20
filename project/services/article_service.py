from dao.article_dao import ArticleDAO
from dao.category_dao import CategoryDAO
from models.article import Article
from services.stock_movement_service import StockMovementService


class ArticleService:
    @staticmethod
    def get_articles(conn):
        return ArticleDAO.select_all(conn)

    @staticmethod
    def get_article_by_id(article_id, conn):
        if article_id <= 0:
            raise ValueError('ID Inválido')
        article = ArticleDAO.select_by_id(article_id, conn)
        if not article:
            raise ValueError('Articulo no encontrado')
        return article

    @staticmethod
    def get_article_by_bar_code(bar_code, conn):
        article = ArticleDAO.select_by_bar_code(bar_code, conn)
        if not article:
            raise ValueError('Articulo no encontrado')
        return article

    @staticmethod
    def get_article_by_description(description, conn):
        article = ArticleDAO.select_by_description(description, conn)
        if not article:
            raise ValueError('Articulo no encontrado')
        return article

    @staticmethod
    def create_article(article: Article, conn):
        if not article.description or not article.description.strip():
            raise ValueError('La descripción debe ser obligatoria')
        if not article.bar_code or not article.bar_code.strip():
            raise ValueError('El código de barra debe ser obligatorio')
        try:
            article.purchase_price = float(article.purchase_price)
            article.retail_price = float(article.retail_price)
            article.wholesale_price = float(article.wholesale_price)
            article.stock = float(article.stock)
        except Exception:
            raise ValueError('Los precios y stock deben ser números')
        if article.stock < 0:
            raise ValueError('Stock no puede ser negativo')
        category = CategoryDAO.select_by_id(article.category_id, conn)
        if not category:
            raise ValueError('Categoría no encontrado')
        if not category.active:
            raise ValueError('La categoría está inactiva')
        existing = ArticleDAO.select_by_bar_code(article.bar_code, conn)
        if existing:
            raise ValueError('Articulo ya existente')
        try:
            result = ArticleDAO.insert(article, conn)
            conn.commit()
            return result
        except Exception:
            conn.rollback()
            raise

    @staticmethod
    def update_article(article: Article, conn):
        if not article.id or article.id <= 0:
            raise ValueError('El ID debe de ser obligatorio')
        if not article.description or not article.description.strip():
            raise ValueError('La descripción debe ser obligatoria')
        if not article.bar_code or not article.bar_code.strip():
            raise ValueError('El código de barra debe ser obligatorio')
        try:
            article.purchase_price = float(article.purchase_price)
            article.retail_price = float(article.retail_price)
            article.wholesale_price = float(article.wholesale_price)
            article.stock = float(article.stock)
        except Exception:
            raise ValueError('Los precios deben ser números')
        if article.stock < 0:
            raise ValueError('Stock no puede ser negativo')
        existing = ArticleDAO.select_by_id(article.id, conn)
        if not existing:
            raise ValueError('Articulo no encontrado')
        category = CategoryDAO.select_by_id(article.category_id, conn)
        if not category:
            raise ValueError('Categoría no encontrado')
        if not category.active:
            raise ValueError('La categoría está inactiva')
        duplicate = ArticleDAO.select_by_bar_code(article.bar_code, conn)
        if duplicate and duplicate.id != article.id:
            raise ValueError('Articulo ya existente')
        try:
            result = ArticleDAO.update(article, conn)
            conn.commit()
            return result
        except Exception:
            conn.rollback()
            raise

    @staticmethod
    def update_stock_sale(bar_code: str, quantity: float, sale_id: int, conn):
        if quantity <= 0:
            raise ValueError('Cantidad debe ser mayor a 0')
        article = ArticleDAO.select_by_bar_code(bar_code, conn)
        if not article:
            raise ValueError('Articulo no encontrado')
        try:
            ArticleDAO.update_stock_sale(bar_code, quantity, conn)
            StockMovementService.register_sale_movement(article.id, quantity, sale_id, conn)
            conn.commit()
        except Exception:
            conn.rollback()
            raise

    @staticmethod
    def update_stock_purchase(bar_code: str, quantity:float ,purchase_id: int, conn):
        if quantity <= 0:
            raise ValueError('Cantidad debe ser mayor a 0')
        article = ArticleDAO.select_by_bar_code(bar_code, conn)
        if not article:
            raise ValueError('Articulo no encontrado')
        try:
            ArticleDAO.update_stock_purchase(bar_code, quantity, conn)
            StockMovementService.register_purchase_movement(article.id, quantity, purchase_id, conn)
            conn.commit()
        except Exception:
            conn.rollback()
            raise

    @staticmethod
    def get_all_paginated(limit, offset, conn):
        return ArticleDAO.get_all_paginated(limit, offset, conn)