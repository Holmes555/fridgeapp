from fridgeapp.models.ingredient import Ingredient
from fridgeapp.storage.base_query import BaseQuery


class IngredientQuery(BaseQuery):
    @staticmethod
    def get_by_name(name: str):
        return Ingredient.objects.get(product__name=name)

    @staticmethod
    def get_all_by_recipe_id(recipe_id):
        return Ingredient.objects.filter(recipe__pk=recipe_id)
