from database.connection import Connection
from models.category import Category
from services.category_service import CategoryService


class CategoryController:

    @staticmethod
    def get_all():
        conn = Connection.get_connection()
        try:
            return CategoryService.get_categories(conn)
        finally:
            Connection.release_connections(conn)

    @staticmethod
    def get_by_id(category_id: int):
        conn = Connection.get_connection()
        try:
            return CategoryService.get_category_by_id(category_id, conn)
        finally:
            Connection.release_connections(conn)

    @staticmethod
    def create_category(name: str, active:bool):
        conn = Connection.get_connection()
        try:
            category = Category(id=None, name=name, active=active)
            return CategoryService.create_category(category, conn)
        finally:
            Connection.release_connections(conn)

    @staticmethod
    def update_category(category_id: int, name: str, active: bool):
        conn = Connection.get_connection()
        try:
            category = Category(id=category_id, name=name, active=active)
            return CategoryService.update_category(category, conn)
        finally:
            Connection.release_connections(conn)

    @staticmethod
    def get_all_paginated(limit, offset):
        conn = Connection.get_connection()
        try:
            return CategoryService.get_all_paginated(limit, offset, conn)
        finally:
            Connection.release_connections(conn)