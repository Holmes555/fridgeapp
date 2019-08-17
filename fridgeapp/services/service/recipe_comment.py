""" This module provides a class RecipeCommentService for working with
    recipe comment data at a higher level (with error handling)

    Classes:
    ----------------
        RecipeCommentService
            working with recipe comment data in database at a higher level
            (with logical error handling)
"""
from typing import List

from fridgeapp.models.recipe import Recipe
from fridgeapp.models.recipe_comment import RecipeComment
from fridgeapp.services.service.base_service import BaseService
from fridgeapp.storage.recipe_comment import RecipeCommentQuery


class RecipeCommentService:
    @staticmethod
    def add(recipe_comment: RecipeComment) -> RecipeComment:
        return BaseService.add(recipe_comment)

    @staticmethod
    def get(recipe_comment_id: int) -> RecipeComment:
        return BaseService.get(RecipeComment, recipe_comment_id)

    @staticmethod
    def delete(user_id, recipe_comment_id: int):
        return BaseService.delete(RecipeComment, user_id, recipe_comment_id)

    @staticmethod
    def get_all_by_recipe_id(recipe_id: int) -> List[RecipeComment]:
        BaseService.is_object_exist(Recipe, recipe_id)
        return RecipeCommentQuery.get_all_by_recipe_id(recipe_id)
