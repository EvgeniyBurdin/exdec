import asyncio
import functools
from typing import Any, Tuple, Union

from .settings import FuncInfo, LogDec

log_dec = LogDec()


def logex(
    *names_or_func,
    reraise: Union[Tuple[Exception, ...], Exception] = (),
    return_value: Any = None,  # return value for no reraise
    exc_info: bool = False,    # whether to include traceback in the log
    log_dec: LogDec = log_dec,
):
    def _decor(func):

        @functools.wraps(func)
        def wrapper(*args, **kwargs):

            func_info = FuncInfo(
                func=func, args=args, kwargs=kwargs,
                reraise=reraise, return_value=return_value, exc_info=exc_info,
            )

            if asyncio.iscoroutinefunction(func):
                async def async_func():
                    try:
                        return await func(*args, **kwargs)
                    except Exception as exc:
                        return log_dec.handling_exception(func_info, exc)
                return async_func()
            else:
                try:
                    return func(*args, **kwargs)
                except Exception as exc:
                    return log_dec.handling_exception(func_info, exc)

        return wrapper

    if names_or_func and callable(names_or_func[0]):
        return _decor(names_or_func[0])
    else:
        return _decor
