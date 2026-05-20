from database.connection import Connection
from models.supplier import Supplier
from services.supplier_service import SupplierService


class SupplierController:

    @staticmethod
    def get_all():
        conn = Connection.get_connection()
        try:
            return SupplierService.get_suppliers(conn)
        finally:
            Connection.release_connections(conn)

    @staticmethod
    def get_by_id(supplier_id):
        conn = Connection.get_connection()
        try:
            return SupplierService.get_supplier_by_id(supplier_id, conn)
        finally:
            Connection.release_connections(conn)

    @staticmethod
    def create_supplier(name:str, telephone_number:str, active:bool):
        conn = Connection.get_connection()
        try:
            supplier = Supplier(id=None, name=name, telephone_number=telephone_number, active=active)
            return SupplierService.create_supplier(supplier, conn)
        finally:
            Connection.release_connections(conn)

    @staticmethod
    def update_supplier(supplier_id: int, name:str, telephone_number:str, active:bool):
        conn = Connection.get_connection()
        try:
            supplier = Supplier(id=supplier_id, name=name, telephone_number=telephone_number, active=active)
            return SupplierService.update_supplier(supplier, conn)
        finally:
            Connection.release_connections(conn)

    @staticmethod
    def get_all_paginated(limit, offset):
        conn = Connection.get_connection()
        try:
            return SupplierService.get_all_paginated(limit, offset, conn)
        finally:
            Connection.release_connections(conn)