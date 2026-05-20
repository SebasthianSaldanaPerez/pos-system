from database.connection import Connection
from services.purchase_service import PurchaseService


class PurchasesController:

    @staticmethod
    def get_general_purchases():
        conn = Connection.get_connection()
        try:
            return PurchaseService.get_purchases(conn)
        finally:
            Connection.release_connections(conn)

    @staticmethod
    def get_details_purchases():
        conn = Connection.get_connection()
        try:
            return PurchaseService.get_purchases_details(conn)
        finally:
            Connection.release_connections(conn)

    @staticmethod
    def get_all_paginated_purchases(limit, offset):
        conn = Connection.get_connection()
        try:
            return PurchaseService.get_all_paginated_purchases(limit, offset, conn)
        finally:
            Connection.release_connections(conn)

    @staticmethod
    def get_all_paginated_purchase_details(limit, offset):
        conn = Connection.get_connection()
        try:
            return PurchaseService.get_all_paginated_purchase_details(limit, offset, conn)
        finally:
            Connection.release_connections(conn)
