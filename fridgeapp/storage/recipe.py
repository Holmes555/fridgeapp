from fridgeapp.models.recipe import Recipe
from fridgeapp.storage.base_query import BaseQuery


class RecipeQuery(BaseQuery):
    def add(self, recipe: Recipe) -> Recipe:
        return BaseQuery.add(recipe)

    def get(self, recipe_id: int) -> Recipe:
        return BaseQuery.get(Recipe, recipe_id)

    def get_all(self):
        return BaseQuery.get_all(Recipe)

    def delete(self, recipe_id: int):
        return BaseQuery.delete(Recipe, recipe_id)

    @staticmethod
    def get_all_by_tag_id(tag_id: int):
        return Recipe.objects.filter(tags__pk=tag_id)
