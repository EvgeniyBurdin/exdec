import asyncio
import functools
from copy import copy
from typing import Any, Callable, Tuple, Union

from .defaults import (APP_NAME, LOGGER_ATTR_NAME, LOGGER_KWARG_NAME,
                       MAIN_LOG_MESSAGE)
from .utils import find_logger as _find_logger
from .utils import log_error as _log_error


def logex(
    *names_or_func,
    logger_attr_name: str = LOGGER_ATTR_NAME,
    logger_kwarg_name: str = LOGGER_KWARG_NAME,
    app_name: str = APP_NAME,
    main_log_message: str = MAIN_LOG_MESSAGE,
    not_reraise: Union[Tuple[Exception, ...], Exception] = (),
    return_value: Any = None,
    log_reraised: bool = True,
    find_logger_func: Callable = _find_logger,
    log_error_func: Callable = _log_error,
    exc_info: bool = False,
):
    def _decor(func):

        @functools.wraps(func)
        def wrapper(*args, **kwargs):

            logger = find_logger_func(
                func, args, kwargs,
                logger_attr_name, logger_kwarg_name, app_name,
            )
            log_kwargs = {
                "logger": logger,
                "func": func, "func_args": args, "func_kwargs": kwargs,
                "main_log_message": main_log_message, "exc_info": exc_info,
            }

            if asyncio.iscoroutinefunction(func):
                async def async_func():
                    try:
                        return await func(*args, **kwargs)
                    except not_reraise as error:
                        log_error_func(**log_kwargs, error=error)
                        return copy(return_value)
                    except Exception as error:
                        if log_reraised:
                            log_error_func(**log_kwargs, error=error)
                        raise
                return async_func()
            else:
                try:
                    return func(*args, **kwargs)
                except not_reraise as error:
                    log_error_func(**log_kwargs, error=error)
                    return copy(return_value)
                except Exception as error:
                    if log_reraised:
                        log_error_func(**log_kwargs, error=error)
                    raise

        return wrapper

    if names_or_func and callable(names_or_func[0]):
        return _decor(names_or_func[0])
    else:
        return _decor
