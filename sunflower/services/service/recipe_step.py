""" This module provides a class RecipeStepService for working with
    recipe step data at a higher level (with error handling)

    Classes:
    ----------------
        RecipeStepService
            working with recipe step data in database at a higher level
            (with logical error handling)
"""
from sunflower.models.recipe import Recipe
from sunflower.models.recipe_step import RecipeStep
from sunflower.services.logger import LogAllMethods
from sunflower.services.service.base_service import BaseService
from sunflower.storage.recipe_step import RecipeStepQuery


class RecipeStepService(metaclass=LogAllMethods):

    @staticmethod
    def add(recipe_step: RecipeStep) -> RecipeStep:
        return BaseService.add(recipe_step)

    @staticmethod
    def get(recipe_step_id: int) -> RecipeStep:
        BaseService.is_object_exist(RecipeStep, recipe_step_id)
        return BaseService.get(RecipeStep, recipe_step_id)

    @staticmethod
    def update(user_id, recipe_step_id: int, kwargs: dict):
        BaseService.is_object_exist(RecipeStep, recipe_step_id)
        BaseService.is_has_rights(RecipeStep, user_id, recipe_step_id)

        return BaseService.update(RecipeStep, user_id, recipe_step_id, kwargs)

    @staticmethod
    def delete(user_id, recipe_step_id: int):
        BaseService.is_object_exist(RecipeStep, recipe_step_id)
        BaseService.is_has_rights(RecipeStep, user_id, recipe_step_id)

        return BaseService.delete(RecipeStep, user_id, recipe_step_id)

    @staticmethod
    def get_all_by_recipe_id(recipe_id: int):
        BaseService.is_object_exist(Recipe, recipe_id)
        return RecipeStepQuery.get_all_by_recipe_id(recipe_id)
