from database.connection import Connection
from models.article import Article
from services.article_service import ArticleService


class ArticleController:

    @staticmethod
    def get_all():
        conn = Connection.get_connection()
        try:
            return ArticleService.get_articles(conn)
        finally:
            Connection.release_connections(conn)

    @staticmethod
    def get_by_id(article_id):
        conn = Connection.get_connection()
        try:
            return ArticleService.get_article_by_id(article_id, conn)
        finally:
            Connection.release_connections(conn)

    @staticmethod
    def get_by_bar_code(bar_code):
        conn = Connection.get_connection()
        try:
            return ArticleService.get_article_by_bar_code(bar_code, conn)
        finally:
            Connection.release_connections(conn)

    @staticmethod
    def get_by_description(description):
        conn = Connection.get_connection()
        try:
            return ArticleService.get_article_by_description(description, conn)
        finally:
            Connection.release_connections(conn)

    @staticmethod
    def create_article(bar_code: str, description: str, purchase_price: float, retail_price: float, wholesale_price: float, stock : float, category_id: int, active: bool):
        conn = Connection.get_connection()
        try:
            article = Article(id=None, bar_code=bar_code, description=description, purchase_price=purchase_price, retail_price=retail_price,
                              wholesale_price=wholesale_price, stock=stock, category_id=category_id, active=active)
            return ArticleService.create_article(article, conn)
        finally:
            Connection.release_connections(conn)

    @staticmethod
    def update_article(article_id:int, bar_code: str, description: str, purchase_price: float, retail_price: float, wholesale_price: float, stock : float, category_id: int, active: bool):
        conn = Connection.get_connection()
        try:
            article = Article(id=article_id, bar_code=bar_code, description=description, purchase_price=purchase_price,
                              retail_price=retail_price, wholesale_price=wholesale_price, stock=stock, category_id=category_id, active=active)
            return ArticleService.update_article(article, conn)
        finally:
            Connection.release_connections(conn)

    @staticmethod
    def get_all_paginated(limit, offset):
        conn = Connection.get_connection()
        try:
            return ArticleService.get_all_paginated(limit, offset, conn)
        finally:
            Connection.release_connections(conn)