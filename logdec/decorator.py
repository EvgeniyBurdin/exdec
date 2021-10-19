import asyncio
import functools
from typing import Callable, Optional, Tuple, Union

from .data_classes import CallInfo, FuncInfo
from .handlers import Handler

handler = Handler()


def logex(
    *names_or_func,
    no_reraise: Union[Tuple[Exception, ...], Exception] = (),
    callback: Optional[Callable] = None,  # for no_reraise
    handler: Handler = handler,
):
    def _decor(func):

        @functools.wraps(func)
        def wrapper(*args, **kwargs):

            def make_call_info(exception: Exception) -> CallInfo:
                func_info = FuncInfo(func=func, args=args, kwargs=kwargs)
                return CallInfo(
                    func_info=func_info, no_reraise=no_reraise,
                    callback=callback
                )

            if asyncio.iscoroutinefunction(func):
                async def async_func():
                    try:
                        return await func(*args, **kwargs)
                    except Exception as exception:
                        return handler.exception(make_call_info(exception))
                return async_func()
            else:
                try:
                    return func(*args, **kwargs)
                except Exception as exception:
                    return handler.exception(make_call_info(exception))

        return wrapper

    if names_or_func and callable(names_or_func[0]):
        return _decor(names_or_func[0])
    else:
        return _decor
