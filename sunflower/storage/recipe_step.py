from sunflower.models.recipe_step import RecipeStep
from sunflower.storage.base_query import BaseQuery


class RecipeStepQuery(BaseQuery):

    @staticmethod
    def get_all_by_recipe_id(recipe_id: int):
        return RecipeStep.objects.filter(recipe__pk=recipe_id)
