""" This module provides a class TagService for working with tag data
    at a higher level (with error handling)

    Classes:
    ----------------
        TagService
            working with tag data in database at a higher level
            (with logical error handling)
"""
from typing import List

from fridgeapp.models.recipe import Recipe
from fridgeapp.models.tag import Tag
from fridgeapp.services.service.base_service import BaseService
from fridgeapp.services.service.recipe import RecipeService
from fridgeapp.storage.tag import TagQuery


class TagService:
    @staticmethod
    def add(tag: Tag) -> Tag:
        return BaseService.add(tag)

    @staticmethod
    def get_or_create(kwargs):
        return BaseService.get_or_create(Tag, kwargs)

    @staticmethod
    def get(tag_id: int) -> Tag:
        return BaseService.get(Tag, tag_id)

    @staticmethod
    def get_all() -> List[Tag]:
        return BaseService.get_all(Tag)

    @staticmethod
    def get_by_title(title: str) -> Tag:
        return TagQuery.get_by_title(title)

    @staticmethod
    def get_all_by_recipe_id(recipe_id: int) -> List[Tag]:
        BaseService.is_object_exist(Recipe, recipe_id)
        return TagQuery.get_all_by_recipe_id(recipe_id)

    @staticmethod
    def _increase_tag_popularity(tag_id: int) -> Tag:
        tag = TagService.get(tag_id)
        tag.popularity += 1
        tag.save()
        return tag

    @staticmethod
    def _decrease_tag_popularity(tag_id: int) -> Tag:
        tag = TagService.get(tag_id)
        if tag.popularity > 0:
            tag.popularity -= 1
            tag.save()
        return tag

    @staticmethod
    def add_to_recipe(user_id: int, recipe_id: int, tag: Tag) -> Tag:
        BaseService.is_object_exist(Recipe, recipe_id)
        BaseService.is_has_rights(Recipe, user_id, recipe_id)

        recipe = RecipeService.get(recipe_id)
        recipe.tags.add(tag)
        TagService._increase_tag_popularity(tag.pk)

        return tag

    @staticmethod
    def remove_from_recipe(user_id: int, recipe_id: int, tag: Tag) -> Tag:
        BaseService.is_object_exist(Recipe, recipe_id)
        BaseService.is_has_rights(Recipe, user_id, recipe_id)

        recipe = RecipeService.get(recipe_id)
        recipe.tags.remove(tag)
        TagService._decrease_tag_popularity(tag.pk)

        return tag
