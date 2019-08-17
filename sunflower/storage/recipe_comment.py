from sunflower.models.recipe_comment import RecipeComment
from sunflower.storage.base_query import BaseQuery


class RecipeCommentQuery(BaseQuery):

    @staticmethod
    def get_all_by_user_id(user_id: int):
        return RecipeComment.objects.filter(author__pk=user_id)

    @staticmethod
    def get_all_by_recipe_id(recipe_id: int):
        return RecipeComment.objects.filter(recipe__pk=recipe_id)
