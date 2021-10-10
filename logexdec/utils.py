from logging import getLogger
from typing import Any, Callable, Dict


def find_or_create_logger(
    func: Callable, func_args: tuple, func_kwargs: Dict[str, Any],
    class_logger_attr_name: str, func_logger_kwarg_name: str,
    app_logger_name: str,
):

    logger = None
    if func_args and hasattr(func_args[0], func.__name__) \
       and func.__qualname__.startswith(func_args[0].__class__.__name__):
        logger = getattr(func_args[0], class_logger_attr_name, None)

    if logger is None:
        logger = func_kwargs.get(func_logger_kwarg_name)

    if logger is None:
        logger = getLogger(app_logger_name)

    return logger


def log(
    logger: Callable,
    func: Callable, func_args: tuple, func_kwargs: Dict[str, Any],
    error: Exception
):
    logger.error(error)
