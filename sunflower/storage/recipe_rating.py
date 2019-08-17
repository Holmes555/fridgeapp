from sunflower.models.recipe_rating import RecipeRating
from sunflower.storage.base_query import BaseQuery


class RecipeRatingQuery(BaseQuery):

    @staticmethod
    def get_by_recipe_id(recipe_id: int):
        return RecipeRating.objects.get(recipe__pk=recipe_id)
