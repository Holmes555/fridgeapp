class FridgeAppException(Exception):
    """ Base exception for other class of exceptions."""

    def __init__(self, message: str):
        super().__init__(message)


class DuplicationException(FridgeAppException):
    def __init__(self, message: str):
        super().__init__(message)


class LogicalException(FridgeAppException):
    def __init__(self, message: str):
        super().__init__(message)


class NotFoundException(FridgeAppException):
    def __init__(self, object_id: int, object_class: str):
        super().__init__(
            "Couldn't find {object_class} with id {object_id}".format(
                object_class=object_class, object_id=object_id
            )
        )


class RightException(FridgeAppException):
    def __init__(self, message: str):
        super().__init__(message)
