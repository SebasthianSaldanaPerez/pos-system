from database.connection import Connection
from services.sale_service import SalesService


class SalesController:

    @staticmethod
    def get_general_sales():
        conn = Connection().get_connection()
        try:
            return SalesService.get_sales(conn)
        finally:
            Connection.release_connections(conn)

    @staticmethod
    def get_details_sales():
        conn = Connection().get_connection()
        try:
            return SalesService.get_sales_details(conn)
        finally:
            Connection.release_connections(conn)

    @staticmethod
    def get_all_paginated_sales(limit, offset):
        conn = Connection().get_connection()
        try:
            return SalesService.get_all_paginated_sales(limit, offset, conn)
        finally:
            Connection.release_connections(conn)

    @staticmethod
    def get_all_paginated_sales_details(limit, offset):
        conn = Connection().get_connection()
        try:
            return SalesService.get_all_paginated_sale_details(limit, offset, conn)
        finally:
            Connection.release_connections(conn)