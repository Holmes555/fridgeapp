from fridgeapp.models.tag import Tag
from fridgeapp.storage.base_query import BaseQuery


class TagQuery(BaseQuery):
    @staticmethod
    def get_by_title(title: str):
        try:
            return Tag.objects.get(title=title)
        except Tag.DoesNotExist:
            return None

    @staticmethod
    def get_all_by_recipe_id(recipe_id: int):
        return Tag.objects.filter(recipe__pk=recipe_id)
