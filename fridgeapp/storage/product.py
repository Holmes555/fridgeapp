from fridgeapp.models.product import Product
from fridgeapp.storage.base_query import BaseQuery


class ProductQuery(BaseQuery):
    @staticmethod
    def get_by_name(name: str):
        return Product.objects.get(name=name)
