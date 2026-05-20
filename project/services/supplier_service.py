from dao.supplier_dao import SupplierDAO
from models.supplier import Supplier


class SupplierService:

    @staticmethod
    def get_suppliers(conn):
        return SupplierDAO.select_all(conn)

    @staticmethod
    def get_supplier_by_id(supplier_id:int, conn):
        if supplier_id <=0:
            raise ValueError('ID inválido')
        supplier = SupplierDAO.select_by_id(supplier_id, conn)

        if not supplier:
            raise ValueError('Proveedor no encontrado')
        return supplier

    @staticmethod
    def create_supplier(supplier: Supplier, conn):
        if not supplier.name or not supplier.name.strip():
            raise ValueError('El nombre debe ser obligatorio')
        if not supplier.telephone_number or not supplier.telephone_number.strip():
            raise ValueError('El telefono no debe ser obligatorio')
        supplier.name = supplier.name.strip()
        existing = SupplierDAO.select_by_name(supplier.name, conn)
        if existing:
            raise ValueError('Proveedor ya existe')
        try:
            result = SupplierDAO.insert(supplier, conn)
            conn.commit()
            return result
        except Exception:
            conn.rollback()
            raise


    @staticmethod
    def update_supplier(supplier: Supplier, conn):
        if not supplier.id or supplier.id <=0:
            raise ValueError('El ID debe ser obligatorio')
        if not supplier.name or not supplier.name.strip():
            raise ValueError('El io')
        if not supplier.telephone_number or not supplier.name.strip():
            raise ValueError('El nombre y número de telefono obligatorio')
        supplier.name = supplier.name.strip()
        existing = SupplierDAO.select_by_id(supplier.id, conn)
        if not existing:
            raise ValueError('Proveedor no encontrado')
        duplicate = SupplierDAO.select_by_name(supplier.name, conn)
        if duplicate and duplicate.id != supplier.id:
            raise ValueError('Proveedor ya existe')
        try:
            result = SupplierDAO.update(supplier, conn)
            conn.commit()
            return result
        except Exception:
            conn.rollback()
            raise

    @staticmethod
    def get_all_paginated(limit, offset, conn):
        return SupplierDAO.get_all_paginated(limit, offset, conn)