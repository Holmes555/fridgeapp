""" This module provides a class IngredientService for working
    with ingredient data at a higher level (with error handling)

    Classes:
    ----------------
        IngredientService
            working with ingredient data in database at a higher level
            (with logical error handling)
"""
from typing import List

from sunflower.models.ingredient import Ingredient
from sunflower.models.recipe import Recipe
from sunflower.services.logger import LogAllMethods
from sunflower.services.service.base_service import BaseService
from sunflower.services.service.product import ProductService
from sunflower.storage.ingredient import IngredientQuery


class IngredientService(metaclass=LogAllMethods):
    
    @staticmethod
    def add(ingredient: Ingredient) -> Ingredient:
        return BaseService.add(ingredient)

    @staticmethod
    def get_or_create(kwargs) -> Ingredient:
        return BaseService.get_or_create(Ingredient, kwargs)

    @staticmethod
    def get(ingredient_id: int) -> Ingredient:
        return BaseService.get(Ingredient, ingredient_id)

    @staticmethod
    def get_all() -> List[Ingredient]:
        return BaseService.get_all(Ingredient)

    @staticmethod
    def get_by_name(name: str):
        return IngredientQuery.get_by_name(name)

    @staticmethod
    def get_all_by_recipe_id(recipe_id):
        BaseService.is_object_exist(Recipe, recipe_id)
        return IngredientQuery.get_all_by_recipe_id(recipe_id)
