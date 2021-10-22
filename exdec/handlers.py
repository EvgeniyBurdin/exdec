""" Module with default handlers.

You can create your own handlers. And use them directly in the decorator call,
or by passing them when creating an instance of the manager class.

Synchronous handlers can be used with both synchronous and asynchronous
functions.

Asynchronous handlers will work only with asynchronous functions.
"""
from typing import Any

from .data_classes import FuncInfo
from .logger import logger


def before_handler(func_info: FuncInfo) -> None:
    """ Called before the operation of the function from `func_info.func`.

    Attention!
    Can change `func_info.args` and `func_info.kwargs`, changed values will
    be used when calling `func_info.func`.
    """
    logger.debug(f"before_handler: {func_info}")


def after_handler(func_info: FuncInfo) -> None:
    """ Called after successful execution of `func_info.func`.

    Attention!
    Can change the value of `func_info.result`, and it will be used as a
    result of the `func_info.func`.
    """
    logger.debug(f"after_handler: {func_info}")


def exc_handler(func_info: FuncInfo) -> Any:
    """ Called if an exception occurs during the execution of `func_info.func`
    and must be handled.

    Returns the value to be used as a result of `func_info.func`.
    """
    logger.error(f"exc_handler: {func_info}")
