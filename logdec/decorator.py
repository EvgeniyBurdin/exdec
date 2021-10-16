import asyncio
import functools
from typing import Any, Tuple, Union

from .utils import FuncInfo, Settings

settings = Settings()


def logex(
    *names_or_func,
    reraise: Union[Tuple[Exception, ...], Exception] = (),
    return_value: Any = None,
    exc_info: bool = False,
    settings: Settings = settings,
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
                        return settings.handling_exception(func_info, exc)
                return async_func()
            else:
                try:
                    return func(*args, **kwargs)
                except Exception as exc:
                    return settings.handling_exception(func_info, exc)

        return wrapper

    if names_or_func and callable(names_or_func[0]):
        return _decor(names_or_func[0])
    else:
        return _decor
