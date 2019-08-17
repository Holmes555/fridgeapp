from fridgeapp.models.recipe_step import RecipeStep
from fridgeapp.storage.base_query import BaseQuery


class RecipeStepQuery(BaseQuery):
    @staticmethod
    def get_all_by_recipe_id(recipe_id: int):
        return RecipeStep.objects.filter(recipe__pk=recipe_id)
