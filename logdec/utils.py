from logging import getLogger, Logger
from typing import Any, Callable, Dict, Tuple, Union
from dataclasses import dataclass
from copy import copy

from .defaults import (APP_NAME, LOGGER_ATTR_NAME, LOGGER_KWARG_NAME,
                       MAIN_LOG_MESSAGE)


@dataclass
class FuncInfo:
    func: Callable
    args: tuple
    kwargs: dict
    reraise: Union[Tuple[Exception, ...], Exception]
    return_value: Any


class Settings:
    def __init__(
        self,
        logger_attr_name: str = LOGGER_ATTR_NAME,
        logger_kwarg_name: str = LOGGER_KWARG_NAME,
        app_name: str = APP_NAME,
        main_log_message: str = MAIN_LOG_MESSAGE,
        is_log_reraise: bool = False,
        exc_info: bool = False,
    ):
        self.logger_attr_name = logger_attr_name
        self.logger_kwarg_name = logger_kwarg_name
        self.app_name = app_name
        self.main_log_message = main_log_message
        self.is_log_reraise = is_log_reraise
        self.exc_info = exc_info

    def find_logger_func(self):
        pass

    def log_func(self, func_info: FuncInfo, exc: Exception):

        logger = self.find_logger_func(func_info)

        extra = {
            "func": func_info.func,
            "func_args": func_info.args,
            "func_kwargs": func_info.kwargs,
            "exc": exc,
        }

        if not self.exc_info:
            msg = f"{self.main_log_message}{exc}"

        logger.error(msg=msg, exc_info=exc_info, extra=extra)

    def handling_exception(self, func_info: FuncInfo, exc: Exception) -> Any:

        if isinstance(exc, func_info.reraise):
            if self.is_log_reraise:
                self.log_func(func_info, exc)
            raise
        self.log_func(func_info, exc)

        return copy(func_info.return_value)


def find_logger(
    func: Callable, func_args: tuple, func_kwargs: Dict[str, Any],
    logger_attr_name: str, logger_kwarg_name: str, app_name: str,
) -> Logger:
    """ Searches for an instance of the logger in class attributes, in named
        function arguments, and in the application.

        Returns the found logger.
    """
    logger = None

    # A logger can be an "attribute" of a method class.
    # The name of the "attribute" in logger_attr_name.
    if func_args and hasattr(func_args[0], func.__name__) \
       and func.__qualname__.startswith(func_args[0].__class__.__name__):
        _logger = getattr(func_args[0], logger_attr_name, None)
        if isinstance(_logger, Logger):
            logger = _logger

    # The logger can be passed to a function as a "named argument".
    # The name of the "named argument" in logger_kwarg_name.
    _logger = func_kwargs.get(logger_kwarg_name)
    if isinstance(_logger, Logger):
        logger = _logger

    # If the logger is not already defined, we will take "application logger".
    # The name of the "application logger" in app_name.
    if logger is None:
        logger = getLogger(app_name)

    return logger


def log_func(
    func: Callable, func_args: tuple, func_kwargs: Dict[str, Any],
    main_log_message: str, exc_info: bool,
    find_logger_func: Callable,
    logger_attr_name: str,
    logger_kwarg_name: str,
    app_name: str,
    error: Exception,
):
    logger = find_logger_func(
        func, func_args, func_kwargs,
        logger_attr_name, logger_kwarg_name, app_name,
    )
    extra = {
        "func": func,
        "func_args": func_args,
        "func_kwargs": func_kwargs,
        "error": error,
    }
    msg = main_log_message

    if not exc_info:
        msg = f"{msg}{error}"

    logger.error(msg=msg, exc_info=exc_info, extra=extra)
