""" This module provides a class RecipeRatingService for working with recipe
    rating data at a higher level (with error handling)

    Classes:
    ----------------
        RecipeRatingService
            working with recipe rating data in database at a higher level
            (with logical error handling)
"""

from sunflower.models.recipe import Recipe
from sunflower.models.recipe_rating import RecipeRating
from sunflower.services.logger import LogAllMethods
from sunflower.services.service.base_service import BaseService
from sunflower.services.service.recipe import RecipeService
from sunflower.storage.base_query import BaseQuery
from sunflower.storage.recipe_rating import RecipeRatingQuery


class RecipeRatingService(metaclass=LogAllMethods):

    @staticmethod
    def add(recipe_rating: RecipeRating) -> RecipeRating:
        return BaseService.add(recipe_rating)

    @staticmethod
    def get(recipe_rating_id: int) -> RecipeRating:
        return BaseService.get(RecipeRating, recipe_rating_id)

    @staticmethod
    def get_by_recipe_id(recipe_id: int) -> RecipeRating:
        BaseService.is_object_exist(Recipe, recipe_id)
        return RecipeRatingQuery.get_by_recipe_id(recipe_id)

    @staticmethod
    def _calculate_new_rating(mark_sum: float, mark_count: int) -> float:
        return mark_sum / mark_count

    @staticmethod
    def update(recipe_id: int, kwargs) -> RecipeRating:
        BaseService.is_object_exist(Recipe, recipe_id)

        recipe = RecipeService.get(recipe_id)
        rating = RecipeRatingService.get_by_recipe_id(recipe.rating.pk)

        mark = kwargs['rating']

        mark_sum = rating.mark_sum + mark
        mark_count = rating.mark_count + 1

        rating = RecipeRatingService._calculate_new_rating(mark_sum, mark_count)

        kwargs['rating'] = rating
        kwargs['mark_sum'] = mark_sum
        kwargs['mark_count'] = mark_count

        return BaseQuery.update(RecipeRating, recipe.rating.pk, kwargs)

