import logging.config
import types
from enum import Enum
from functools import wraps


class LogLevel(Enum):
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


logger = logging.getLogger(__name__)


class LogAllMethods(type):
    def __new__(mcs, name, bases, attrs):

        for attr_name, attr_value in attrs.items():
            if isinstance(attr_value, types.FunctionType):
                attrs[attr_name] = mcs.deco(attr_value)

        return super(LogAllMethods, mcs).__new__(mcs, name, bases, attrs)

    @classmethod
    def deco(mcs, func):
        def wrapper(*args, **kwargs):
            message = (f"{func.__name__} with args {args} "
                       f"and kwargs {kwargs} called")
            log_function_call(func, message)
            result = func(*args, **kwargs)
            message = f"{func.__name__} called with result {result}"
            log_function_call(func, message)
            return result

        return wrapper


def log_function_call(function_to_decorate, message, level=LogLevel.INFO):
    levels = {
        LogLevel.DEBUG: logger.debug,
        LogLevel.INFO: logger.info,
        LogLevel.WARNING: logger.warning,
        LogLevel.ERROR: logger.error,
        LogLevel.CRITICAL: logger.critical
    }

    @wraps(function_to_decorate)
    def wrapper_around_function(*args, **kwargs):
        levels[level](message)
        return function_to_decorate(*args, **kwargs)

    return wrapper_around_function
