""" This module provides a class ProductService for working with product data
    at a higher level (with error handling)

    Classes:
    ----------------
        ProductService
            working with product data in database at a higher level
            (with logical error handling)
"""
from typing import List

from fridgeapp.models.product import Product
from fridgeapp.services.service.base_service import BaseService
from fridgeapp.storage.product import ProductQuery


class ProductService:
    @staticmethod
    def add(product: Product) -> Product:
        BaseService.is_duplicated(Product, "name", product.name)
        return BaseService.add(product)

    @staticmethod
    def get_or_create(kwargs) -> Product:
        return BaseService.get_or_create(Product, kwargs)

    @staticmethod
    def get(product_id: int) -> Product:
        return BaseService.get(Product, product_id)

    @staticmethod
    def get_all() -> List[Product]:
        return BaseService.get_all(Product)

    @staticmethod
    def get_by_name(name: str) -> Product:
        return ProductQuery.get_by_name(name)
