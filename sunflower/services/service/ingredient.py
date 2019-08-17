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
    def delete(user_id: int, ingredient_id: int):
        return BaseService.delete(Ingredient, user_id, ingredient_id)

    @staticmethod
    def get_by_name(name: str):
        return IngredientQuery.get_by_name(name)

    @staticmethod
    def get_all_by_recipe_id(recipe_id):
        BaseService.is_object_exist(Recipe, recipe_id)
        return IngredientQuery.get_all_by_recipe_id(recipe_id)

    @staticmethod
    def update(user_id: int, ingredient_id, kwargs: dict) -> Ingredient:

        if 'product' in kwargs:
            kwargs_ = {'name': kwargs['product']}
            product, _ = ProductService.get_or_create(kwargs_)
            kwargs['product'] = product

        return BaseService.update(Ingredient, user_id, ingredient_id, kwargs)
