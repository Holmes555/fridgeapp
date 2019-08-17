from sunflower.models.recipe import Recipe
from sunflower.storage.base_query import BaseQuery


class RecipeQuery(BaseQuery):

    def add(self, recipe: Recipe) -> Recipe:
        return BaseQuery.add(recipe)

    def get(self, recipe_id: int) -> Recipe:
        return BaseQuery.get(Recipe, recipe_id)

    def get_all(self):
        return BaseQuery.get_all(Recipe)

    def update(self, recipe_id: int, kwargs):
        return BaseQuery.update(Recipe, recipe_id, kwargs)

    def delete(self, recipe_id: int):
        return BaseQuery.delete(Recipe, recipe_id)

    @staticmethod
    def get_all_by_user_id(user_id: int):
        return Recipe.objects.filter(author__pk=user_id)

    @staticmethod
    def get_all_by_tag_id(tag_id: int):
        return Recipe.objects.filter(tags__pk=tag_id)

    @staticmethod
    def get_all_by_product_id(product_id: int):
        return Recipe.objects.filter(
            ingredients__product__pk=product_id)

    @staticmethod
    def get_all_by_cookbook_id(cookbook_id: int):
        return Recipe.objects.filter(cookbook__pk=cookbook_id)
