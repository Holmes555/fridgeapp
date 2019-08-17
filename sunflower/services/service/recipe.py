""" This module provides a class RecipeService for working with
    recipe data at a higher level (with error handling)

    Classes:
    ----------------
        RecipeService
            working with recipe data in database at a higher level
            (with logical error handling)
"""
from typing import List

from sunflower.models import CustomUser
from sunflower.models.cookbook import CookBook
from sunflower.models.ingredient import Ingredient
from sunflower.models.product import Product
from sunflower.models.recipe import Recipe
from sunflower.models.recipe_step import RecipeStep
from sunflower.models.tag import Tag
from sunflower.services.logger import LogAllMethods
from sunflower.services.service.base_service import BaseService
from sunflower.services.service.recipe_step import RecipeStepService
from sunflower.storage.recipe import RecipeQuery


class RecipeService(metaclass=LogAllMethods):

    @staticmethod
    def add(recipe: Recipe) -> Recipe:
        return BaseService.add(recipe)

    @staticmethod
    def get(recipe_id: int) -> Recipe:
        return BaseService.get(Recipe, recipe_id)

    @staticmethod
    def get_all() -> List[Recipe]:
        return BaseService.get_all(Recipe)

    @staticmethod
    def update(user_id: int, recipe_id: int, kwargs) -> Recipe:
        return BaseService.update(Recipe, user_id, recipe_id, kwargs)

    @staticmethod
    def delete(user_id: int, recipe_id: int):
        return BaseService.delete(Recipe, user_id, recipe_id)

    @staticmethod
    def get_all_by_user_id(user_id: int) -> List[Recipe]:
        BaseService.is_object_exist(CustomUser, user_id)
        return RecipeQuery.get_all_by_user_id(user_id)

    @staticmethod
    def get_all_by_tag_id(tag_id: int) -> List[Recipe]:
        BaseService.is_object_exist(Tag, tag_id)
        return RecipeQuery.get_all_by_tag_id(tag_id)

    @staticmethod
    def get_all_by_product_id(product_id: int) -> List[Recipe]:
        BaseService.is_object_exist(Product, product_id)
        return RecipeQuery.get_all_by_product_id(product_id)

    @staticmethod
    def get_all_by_cookbook_id(cookbook_id: int) -> List[Recipe]:
        BaseService.is_object_exist(CookBook, cookbook_id)
        return RecipeQuery.get_all_by_cookbook_id(cookbook_id)

    @staticmethod
    def add_ingredient(user_id: int, recipe_id: int, ingredient: Ingredient
                       ) -> Recipe:
        BaseService.is_object_exist(Recipe, recipe_id)
        BaseService.is_has_rights(Recipe, user_id, recipe_id)

        recipe = RecipeService.get(recipe_id)
        recipe.ingredients.add(ingredient)
        return recipe

    @staticmethod
    def _increase_steps_count(recipe: Recipe) -> Recipe:
        recipe.steps_count += 1
        recipe.save()
        return recipe

    @staticmethod
    def _set_step_number(recipe: Recipe, recipe_step: RecipeStep) -> Recipe:
        steps_count = recipe.steps_count
        recipe_step.step_number = steps_count
        recipe_step.save()
        return recipe

    @staticmethod
    def add_recipe_step(user_id: int, recipe_id: int, recipe_step: RecipeStep
                        ) -> Recipe:
        BaseService.is_object_exist(Recipe, recipe_id)
        BaseService.is_has_rights(Recipe, user_id, recipe_id)

        recipe = RecipeService.get(recipe_id)
        RecipeService._increase_steps_count(recipe)
        RecipeService._set_step_number(recipe, recipe_step)

        recipe.recipe_steps.add(recipe_step)
        return recipe

    @staticmethod
    def _decrease_steps_count(recipe: Recipe) -> Recipe:
        recipe.steps_count += 1
        recipe.save()
        return recipe

    @staticmethod
    def remove_recipe_step(user_id: int, recipe_id: int, recipe_step_id: int
                           ) -> Recipe:
        BaseService.is_object_exist(Recipe, recipe_id)
        BaseService.is_has_rights(Recipe, user_id, recipe_id)

        recipe = RecipeService.get(recipe_id)
        RecipeService._decrease_steps_count(recipe)

        recipe_step = RecipeStepService.get(recipe_step_id)

        recipe.recipe_steps.remove(recipe_step)
        return recipe
