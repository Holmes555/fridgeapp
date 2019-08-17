from sunflower.models.cookbook import CookBook
from sunflower.storage.base_query import BaseQuery


class CookBookQuery(BaseQuery):

    @staticmethod
    def get_all_by_user_id(user_id: int):
        return CookBook.objects.filter(author__pk=user_id)
