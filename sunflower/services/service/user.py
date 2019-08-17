""" This module provides a class UserService for working with user data
    at a higher level (with error handling)

    Classes:
    ----------------
        UserService
            working with user data in database at a higher level
            (with logical error handling)
"""
from sunflower.models import CustomUser
from sunflower.services import exceptions
from sunflower.services.logger import LogAllMethods
from sunflower.services.service.base_service import BaseService
from sunflower.storage.user import UserQuery


class UserService(metaclass=LogAllMethods):

    @staticmethod
    def is_username_unique(username: str):
        try:
            UserService.get_by_name(username)
        except CustomUser.DoesNotExist:
            return True
        raise exceptions.LogicalException(f"Can't update to username "
                                          f"{username}, because user with such "
                                          f"username is already exists!")

    @staticmethod
    def add(user: CustomUser) -> CustomUser:
        return BaseService.add(user)

    @staticmethod
    def get(user_id: int) -> CustomUser:
        return BaseService.get(CustomUser, user_id)

    @staticmethod
    def update(user_id: int, kwargs) -> CustomUser:
        return UserQuery.update(CustomUser, user_id, kwargs)

    @staticmethod
    def delete(user_id):
        return UserQuery.delete(CustomUser, user_id)

    @staticmethod
    def get_by_name(username: str):
        return UserQuery.get_by_name(username)
