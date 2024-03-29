from fridgeapp.services import exceptions
from fridgeapp.storage.base_query import BaseQuery


class BaseService:
    @staticmethod
    def get_name(model):
        return model.__name__

    @staticmethod
    def is_duplicated(model, param: str, param_val):
        kwargs = {param: param_val}
        if BaseQuery.is_duplication(model, kwargs):
            model = BaseService.get_name(model)
            raise exceptions.DuplicationException(
                f"{model} with {param} {param_val} is already exists!"
            )
        return False

    @staticmethod
    def _object_not_found(object_id: int, object_name: str):
        """ Checks if such an object exists in the database. """
        raise exceptions.NotFoundException(object_id, object_name)

    @staticmethod
    def is_object_exist(model, object_id: int):
        try:
            BaseQuery.get(model, object_id)
        except model.DoesNotExist:
            model = BaseService.get_name(model)
            BaseService._object_not_found(object_id, model)

    @staticmethod
    def is_has_rights(model, user_id: int, object_id: int):
        object_ = BaseQuery.get(model, object_id)
        if object_.author.pk == user_id:
            return True
        model = BaseService.get_name(model)
        raise exceptions.RightException(
            f"User doesn't have rights to modify this {model} (id {object_id})"
        )

    @staticmethod
    def add(model_object):
        return BaseQuery.add(model_object)

    @staticmethod
    def get(model, object_id: int):
        BaseService.is_object_exist(model, object_id)
        return BaseQuery.get(model, object_id)

    @staticmethod
    def get_or_create(model, kwargs):
        return BaseQuery.get_or_create(model, kwargs)

    @staticmethod
    def get_all(model):
        return BaseQuery.get_all(model)

    @staticmethod
    def update(model, user_id: int, object_id: int, kwargs):
        BaseService.is_object_exist(model, object_id)
        BaseService.is_has_rights(model, user_id, object_id)

        return BaseQuery.update(model, object_id, kwargs)

    @staticmethod
    def delete(model, user_id: int, object_id: int):
        BaseService.is_object_exist(model, object_id)
        BaseService.is_has_rights(model, user_id, object_id)

        return BaseQuery.delete(model, object_id)
