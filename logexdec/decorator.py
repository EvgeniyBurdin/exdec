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
    exclude: Union[Tuple[Exception, ...], Exception] = (),
    is_log_exclude: bool = True,
    find_logger: Callable = _find_logger,
    log_error: Callable = _log_error,
    is_exc_info: bool = False,
):
    def _decor(func):

        @functools.wraps(func)
        def wrapper(*args, **kwargs):

            logger = find_logger(
                func, args, kwargs,
                class_logger_attr_name,
                func_logger_kwarg_name,
                app_logger_name,
            )
            log_kwargs = {
                "logger": logger,
                "func": func, "func_args": args, "func_kwargs": kwargs,
                "main_message": main_message, "is_exc_info": is_exc_info,
            }
            if asyncio.iscoroutinefunction(func):
                async def async_func():
                    try:
                        return await func(*args, **kwargs)
                    except exclude as exc_info:
                        if is_log_exclude:
                            log_error(**log_kwargs, exc_info=exc_info)
                        raise
                    except Exception as exc_info:
                        log_error(**log_kwargs, exc_info=exc_info)
                        return copy(return_value)
                return async_func()
            else:
                try:
                    return func(*args, **kwargs)
                except exclude as exc_info:
                    if is_log_exclude:
                        log_error(**log_kwargs, exc_info=exc_info)
                    raise
                except Exception as exc_info:
                    log_error(**log_kwargs, exc_info=exc_info)
                    return copy(return_value)

        return wrapper

    if names_or_func and callable(names_or_func[0]):
        return _decor(names_or_func[0])
    else:
        return _decor
