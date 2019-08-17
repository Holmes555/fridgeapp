""" This module provides a class RecipeCommentService for working with
    recipe comment data at a higher level (with error handling)

    Classes:
    ----------------
        RecipeCommentService
            working with recipe comment data in database at a higher level
            (with logical error handling)
"""
from typing import List

from sunflower.models import CustomUser
from sunflower.models.recipe import Recipe
from sunflower.models.recipe_comment import RecipeComment
from sunflower.services.logger import LogAllMethods
from sunflower.services.service.base_service import BaseService
from sunflower.storage.recipe_comment import RecipeCommentQuery


class RecipeCommentService(metaclass=LogAllMethods):
    
    @staticmethod
    def add(recipe_comment: RecipeComment) -> RecipeComment:
        return BaseService.add(recipe_comment)

    @staticmethod
    def get(recipe_comment_id: int) -> RecipeComment:
        return BaseService.get(RecipeComment, recipe_comment_id)

    @staticmethod
    def update(user_id, recipe_comment_id: int, kwargs) -> RecipeComment:
        return BaseService.update(RecipeComment, user_id, recipe_comment_id,
                                  kwargs)

    @staticmethod
    def delete(user_id, recipe_comment_id: int):
        return BaseService.delete(RecipeComment, user_id, recipe_comment_id)

    @staticmethod
    def get_all_by_user_id(user_id: int) -> List[RecipeComment]:
        BaseService.is_object_exist(CustomUser, user_id)
        return RecipeCommentQuery.get_all_by_user_id(user_id)

    @staticmethod
    def get_all_by_recipe_id(recipe_id: int) -> List[RecipeComment]:
        BaseService.is_object_exist(Recipe, recipe_id)
        return RecipeCommentQuery.get_all_by_recipe_id(recipe_id)