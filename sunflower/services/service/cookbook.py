""" This module provides a class CookBookService for working with
    cookbook data at a higher level (with error handling)

    Classes:
    ----------------
        CookBookService
            working with cookbook data in database at a higher level
            (with logical error handling)
"""
from typing import List

from sunflower.models import CustomUser
from sunflower.models.cookbook import CookBook
from sunflower.models.recipe import Recipe
from sunflower.services.logger import LogAllMethods
from sunflower.services.service.base_service import BaseService
from sunflower.storage.cookbook import CookBookQuery


class CookBookService(metaclass=LogAllMethods):

    @staticmethod
    def add(cookbook: CookBook) -> CookBook:
        return BaseService.add(cookbook)

    @staticmethod
    def get(cookbook_id: int) -> CookBook:
        return BaseService.get(CookBook, cookbook_id)

    @staticmethod
    def update(user_id: int, cookbook_id: int, kwargs):
        return BaseService.update(CookBook, user_id, cookbook_id, kwargs)

    @staticmethod
    def delete(user_id: int, cookbook_id: int):
        return BaseService.delete(CookBook, user_id, cookbook_id)

    @staticmethod
    def get_all_by_user_id(user_id: int) -> List[CookBook]:
        BaseService.is_object_exist(CustomUser, user_id)
        return CookBookQuery.get_all_by_user_id(user_id)

    @staticmethod
    def add_recipe(user_id: int, cookbook_id: int, recipe: Recipe
                   ) -> CookBook:
        BaseService.is_object_exist(CookBook, cookbook_id)
        BaseService.is_has_rights(CookBook, user_id, cookbook_id)

        cookbook = BaseService.get(CookBook, cookbook_id)
        cookbook.recipes.add(recipe)
        return cookbook

    @staticmethod
    def remove_recipe(user_id: int, cookbook_id: int, recipe: Recipe
                      ) -> CookBook:
        BaseService.is_object_exist(CookBook, cookbook_id)
        BaseService.is_has_rights(CookBook, user_id, cookbook_id)

        cookbook = BaseService.get(CookBook, cookbook_id)
        cookbook.recipes.remove(recipe)
        return cookbook
