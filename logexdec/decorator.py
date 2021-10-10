import asyncio
import functools
from copy import copy
from typing import Any, Callable, Tuple, Union

from logexdec.defaults import (APP_LOGGER_NAME, CLASS_LOGGER_ATTR_NAME,
                               FUNC_LOGGER_KWARG_NAME, MAIN_MESSAGE)
from logexdec.utils import find_logger as _find_logger
from logexdec.utils import log_error as _log_error


def logex(
    *names_or_func,
    class_logger_attr_name: str = CLASS_LOGGER_ATTR_NAME,
    func_logger_kwarg_name: str = FUNC_LOGGER_KWARG_NAME,
    app_logger_name: str = APP_LOGGER_NAME,
    main_message: str = MAIN_MESSAGE,
    return_value: Any = None,
    raise_exceptions: Union[Tuple[Exception, ...], Exception] = (),
    is_log_raised: bool = True,
    find_logger_func: Callable = _find_logger,
    log_error_func: Callable = _log_error,
    exc_info: bool = False,
):
    def _decor(func):

        @functools.wraps(func)
        def wrapper(*args, **kwargs):

            logger = find_logger_func(
                func, args, kwargs,
                class_logger_attr_name,
                func_logger_kwarg_name,
                app_logger_name,
            )
            log_kwargs = {
                "logger": logger,
                "func": func, "func_args": args, "func_kwargs": kwargs,
                "main_message": main_message, "exc_info": exc_info,
            }
            if asyncio.iscoroutinefunction(func):
                async def async_func():
                    try:
                        return await func(*args, **kwargs)
                    except raise_exceptions as error:
                        if is_log_raised:
                            log_error_func(**log_kwargs, error=error)
                        raise
                    except Exception as error:
                        log_error_func(**log_kwargs, error=error)
                        return copy(return_value)
                return async_func()
            else:
                try:
                    return func(*args, **kwargs)
                except raise_exceptions as error:
                    if is_log_raised:
                        log_error_func(**log_kwargs, error=error)
                    raise
                except Exception as error:
                    log_error_func(**log_kwargs, error=error)
                    return copy(return_value)

        return wrapper

    if names_or_func and callable(names_or_func[0]):
        return _decor(names_or_func[0])
    else:
        return _decor
