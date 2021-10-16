import asyncio
import functools
from copy import copy
from typing import Any, Callable, Tuple, Union

from .defaults import (APP_NAME, LOGGER_ATTR_NAME, LOGGER_KWARG_NAME,
                       MAIN_LOG_MESSAGE)
from .utils import find_logger as _find_logger
from .utils import log_func as _log_func


def logex(
    *names_or_func,
    logger_attr_name: str = LOGGER_ATTR_NAME,
    logger_kwarg_name: str = LOGGER_KWARG_NAME,
    app_name: str = APP_NAME,
    main_log_message: str = MAIN_LOG_MESSAGE,
    reraise: Union[Tuple[Exception, ...], Exception] = (),
    return_value: Any = None,
    is_log_reraise: bool = False,
    find_logger_func: Callable = _find_logger,
    log_func: Callable = _log_func,
    exc_info: bool = False,
):
    def _decor(func):

        @functools.wraps(func)
        def wrapper(*args, **kwargs):

            log_kwargs = {
                "func": func, "func_args": args, "func_kwargs": kwargs,
                "main_log_message": main_log_message, "exc_info": exc_info,
                "find_logger_func": find_logger_func,
                "logger_attr_name": logger_attr_name,
                "logger_kwarg_name": logger_kwarg_name,
                "app_name": app_name,
            }

            if asyncio.iscoroutinefunction(func):
                async def async_func():
                    try:
                        return await func(*args, **kwargs)
                    except reraise as error:
                        if is_log_reraise:
                            log_func(**log_kwargs, error=error)
                        raise
                    except Exception as error:
                        log_func(**log_kwargs, error=error)
                        return copy(return_value)
                return async_func()
            else:
                try:
                    return func(*args, **kwargs)
                except reraise as error:
                    if is_log_reraise:
                        log_func(**log_kwargs, error=error)
                    raise
                except Exception as error:
                    log_func(**log_kwargs, error=error)
                    return copy(return_value)

        return wrapper

    if names_or_func and callable(names_or_func[0]):
        return _decor(names_or_func[0])
    else:
        return _decor
