from logging import getLogger, Logger
from typing import Any, Callable, Dict


def find_logger(
    func: Callable, func_args: tuple, func_kwargs: Dict[str, Any],
    class_logger_attr_name: str,
    func_logger_kwarg_name: str,
    app_logger_name: str,
) -> Logger:
    """ Searches for an instance of the logger in class attributes, in named
        function arguments, and in the application.

        Returns the found logger.
    """
    logger = None

    # A logger can be an "attribute" of a method class.
    # The name of the "attribute" in class_logger_attr_name.
    if func_args and hasattr(func_args[0], func.__name__) \
       and func.__qualname__.startswith(func_args[0].__class__.__name__):
        _logger = getattr(func_args[0], class_logger_attr_name, None)
        if isinstance(_logger, Logger):
            logger = _logger

    # The logger can be passed to a function as a "named argument".
    # The name of the "named argument" in func_logger_kwarg_name.
    _logger = func_kwargs.get(func_logger_kwarg_name)
    if isinstance(_logger, Logger):
        logger = _logger

    # If the logger is not already defined, we will take "application logger".
    # The name of the "application logger" in app_logger_name.
    if logger is None:
        logger = getLogger(app_logger_name)

    return logger


def log_error(
    logger: Logger,
    func: Callable, func_args: tuple, func_kwargs: Dict[str, Any],
    main_message: str, is_exc_info: bool,
    exc_info: Exception,
):
    extra = {
        "func": func,
        "func_args": func_args,
        "func_kwargs": func_kwargs,
        "error": exc_info,
    }
    msg = main_message

    if not is_exc_info:
        msg = f"{msg}{exc_info}"
        exc_info = None

    logger.error(msg=msg, exc_info=exc_info, extra=extra)
