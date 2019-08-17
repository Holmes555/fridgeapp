""" This module contains exceptions, that can rise within this package.

    SunflowerException - base exception for other class of exceptions;
    DuplicationError - raises, when user tries to add the same date (duplicate)
                       to the database;
    DependencyError - raises, when user tries to do illegal relation operation;
    LogicalError - raises, when user tries to perform an illogical operation;
    NotFoundError - raises, when user trying to get an object that
                    is not in the database;
    RightError - raises, when user trying to do something,
                 he doesn't have a right to do;
"""


class ServiceException(Exception):
    """ Base exception for other class of exceptions."""

    def __init__(self, message: str):
        """
        Parameters
        ----------
        message: str
            Exception text, which describes mistake;
        """
        super().__init__(message)


class DuplicationException(ServiceException):
    """
        Raises, when user tries to add the same date (duplicate)
        to the database.

        Examples:
        ----------
            * User trying to add duplicate cookbook relation.
            * User trying to add duplicate tag.

    """
    def __init__(self, message: str):
        """
        Parameters
        ----------
        message: str
            Exception text, which describes mistake;
        """
        super().__init__(message)


class LogicalException(ServiceException):
    """
        Raises, when user tries to perform an illogical operation.

        Examples:
        ----------
            * User trying to add a loop relation between two cookbooks

    """
    def __init__(self, message: str):
        """
        Parameters
        ----------
        message: str
            Exception text, which describes mistake;
        """
        super().__init__(message)


class NotFoundException(ServiceException):
    """
         Raises, when user trying to get an object that is not in the database.

         Examples:
         ----------
            * User trying to get a recipe, before the creation.
            * User trying to get a remote cookbook.
    """
    def __init__(self, object_id: int, object_class: str):
        """
        Parameters
        ----------
        object_id: int
            Id of of object, that user trying to found.
        object_class: str
            Class of object (recipe, cookbook, ...), that user trying to found.
        """
        super().__init__("Couldn't find {object_class} with id {object_id}"
                         .format(object_class=object_class,
                                 object_id=object_id))


class RightException(ServiceException):
    """
        Raises, when user trying to do something, he doesn't have a right to do.

        Examples:
        ----------
            * User trying to update another user's recipe.
            * User trying to delete another user's cookbook.
            * User trying to add his recipe to another user's cookbook.

    """

    def __init__(self, message: str):
        """
        Parameters
        ----------
        message: str
            Exception text, which describes mistake;
        """
        super().__init__(message)
