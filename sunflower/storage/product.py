from sunflower.models.product import Product
from sunflower.storage.base_query import BaseQuery


class ProductQuery(BaseQuery):

    @staticmethod
    def get_by_name(name: str):
        return Product.objects.get(name=name)
