import asyncio
import functools
from copy import copy
from typing import Any, Tuple, Union

from logexdec.settings import (APP_LOGGER_NAME, CLASS_LOGGER_ATTR_NAME,
                               FUNC_LOGGER_KWARG_NAME)
from logexdec.utils import find_or_create_logger, log


def logex(
    *names_or_func,
    class_logger_attr_name: str = CLASS_LOGGER_ATTR_NAME,
    func_logger_kwarg_name: str = FUNC_LOGGER_KWARG_NAME,
    app_logger_name: str = APP_LOGGER_NAME,
    return_value: Any = None,
    exclude: Union[Tuple[Exception, ...], Exception] = (),
    log_exclude: bool = True
):
    def _decor(func):

        @functools.wraps(func)
        def wrapper(*args, **kwargs):

            logger = find_or_create_logger(
                func, args, kwargs,
                class_logger_attr_name, func_logger_kwarg_name,
                app_logger_name,
            )
            log_kwargs = {
                "logger": logger,
                "func": func, "func_args": args, "func_kwargs": kwargs,

            }
            if asyncio.iscoroutinefunction(func):
                async def async_func():
                    try:
                        return await func(*args, **kwargs)
                    except exclude as error:
                        if log_exclude:
                            log(**log_kwargs, error=error)
                        raise
                    except Exception as error:
                        log(**log_kwargs, error=error)
                        return copy(return_value)
                return async_func()
            else:
                try:
                    return func(*args, **kwargs)
                except exclude as error:
                    if log_exclude:
                        log(**log_kwargs, error=error)
                    raise
                except Exception as error:
                    log(**log_kwargs, error=error)
                    return copy(return_value)

        return wrapper

    if names_or_func and callable(names_or_func[0]):
        return _decor(names_or_func[0])
    else:
        return _decor
