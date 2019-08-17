from fridgeapp.models.recipe_comment import RecipeComment
from fridgeapp.storage.base_query import BaseQuery


class RecipeCommentQuery(BaseQuery):
    @staticmethod
    def get_all_by_recipe_id(recipe_id: int):
        return RecipeComment.objects.filter(recipe__pk=recipe_id)
