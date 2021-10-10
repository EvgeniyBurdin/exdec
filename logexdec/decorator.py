import asyncio
import functools
from copy import copy
from typing import Any, Tuple, Union

from logexdec.utils import find_or_create_logger, log


def logex(
    *names_or_func,
    class_logger_attr_name: str = "logger",
    func_logger_kwarg_name: str = "logger",
    app_logger_name: str = "log_exception",
    return_on_exception: Any = None,
    exclude: Union[Tuple[Exception, ...], Exception] = (),
    is_log_for_exclude: bool = True
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
                        if is_log_for_exclude:
                            log(**log_kwargs, error=error)
                        raise
                    except Exception as error:
                        log(**log_kwargs, error=error)
                        return copy(return_on_exception)
                return async_func()
            else:
                try:
                    return func(*args, **kwargs)
                except exclude as error:
                    if is_log_for_exclude:
                        log(**log_kwargs, error=error)
                    raise
                except Exception as error:
                    log(**log_kwargs, error=error)
                    return copy(return_on_exception)

        return wrapper

    if names_or_func and callable(names_or_func[0]):
        return _decor(names_or_func[0])
    else:
        return _decor
