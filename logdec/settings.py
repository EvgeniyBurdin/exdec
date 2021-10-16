from copy import copy
from dataclasses import dataclass
from logging import Logger, getLogger
from typing import Any, Callable, Optional, Tuple, Union

from .defaults import (APP_NAME, LOGGER_ATTR_NAME, LOGGER_KWARG_NAME,
                       MAIN_LOG_MESSAGE)


@dataclass
class FuncInfo:
    func: Callable
    args: tuple
    kwargs: dict
    reraise: Union[Tuple[Exception, ...], Exception]
    return_value: Any
    exc_info: bool
    owner_instance: Optional[object] = None


class LogDec:
    def __init__(
        self,
        logger_attr_name: str = LOGGER_ATTR_NAME,
        logger_kwarg_name: str = LOGGER_KWARG_NAME,
        app_name: str = APP_NAME,
        main_log_message: str = MAIN_LOG_MESSAGE,
        is_log_reraise: bool = False,
    ):
        self.logger_attr_name = logger_attr_name
        self.logger_kwarg_name = logger_kwarg_name
        self.app_name = app_name
        self.main_log_message = main_log_message
        self.is_log_reraise = is_log_reraise

    @staticmethod
    def get_owner_instance(
        func: Callable, func_args: tuple
    ) -> Optional[object]:

        if func_args and hasattr(func_args[0], func.__name__):
            class_name = func_args[0].__class__.__name__
            method_name = f"{class_name}.{func.__name__}"
            if func.__qualname__ == method_name:
                return func_args[0]

    @staticmethod
    def get_logger_from_instance(
        instance: object, logger_attr_name: str
    ) -> Optional[Logger]:

        logger = getattr(instance, logger_attr_name, None)
        if isinstance(logger, Logger):
            return logger

    def find_logger_func(self, func_info: FuncInfo) -> Logger:
        """ Searches for an instance of the logger in class attributes, in named
            function arguments, and in the application.

            Returns the found logger.
        """
        func_info.owner_instance = self.get_owner_instance(
            func_info.func, func_info.args
        )

        # A logger can be an "attribute" of a method class
        logger = self.get_logger_from_instance(
            func_info.owner_instance, self.logger_attr_name
        )

        # The logger can be passed to a function as a "named argument"
        _logger = func_info.kwargs.get(self.logger_kwarg_name)
        logger = _logger if isinstance(_logger, Logger) else logger

        return getLogger(self.app_name) if logger is None else logger

    def log_exception(self, func_info: FuncInfo, exc: Exception):

        logger = self.find_logger_func(func_info)

        extra = {
            "func": func_info.func,
            "func_args": func_info.args,
            "func_kwargs": func_info.kwargs,
            "exc": exc,
        }

        msg = self.main_log_message
        if not func_info.exc_info:
            msg = f"{msg} {exc}"

        logger.error(msg=msg, exc_info=func_info.exc_info, extra=extra)

    def handling_exception(self, func_info: FuncInfo, exc: Exception) -> Any:

        if isinstance(exc, func_info.reraise):
            if self.is_log_reraise:
                self.log_exception(func_info, exc)
            raise
        self.log_exception(func_info, exc)

        return copy(func_info.return_value)
