from sunflower.models.user import CustomUser
from sunflower.storage.base_query import BaseQuery


class UserQuery(BaseQuery):

    @staticmethod
    def update(model, object_id: int, kwargs):
        return BaseQuery.update(model, object_id, kwargs)

    @staticmethod
    def delete(model, object_id: int):
        return BaseQuery.delete(model, object_id)

    @staticmethod
    def get_by_name(username: str):
        return CustomUser.objects.get(username=username)
