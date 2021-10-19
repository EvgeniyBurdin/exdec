import asyncio
import functools
from typing import Tuple, Union, Optional, Callable, Type

from .data_classes import FuncInfo, DecData
from .handlers import Handler

handler = Handler()


def logex(
    *names_or_func,
    no_reraise: Union[Tuple[Type, ...], Type] = Exception,
    callback: Optional[Callable] = None,
    handler: Handler = handler,
):
    def _decor(func):

        @functools.wraps(func)
        def wrapper(*args, **kwargs):

            def make_dec_data(exception: Exception) -> DecData:
                return DecData(
                    exception=exception,
                    no_reraise=no_reraise,
                    callback=callback,
                    func_info=FuncInfo(func=func, args=args, kwargs=kwargs),
                )

            if asyncio.iscoroutinefunction(func):
                async def async_func():
                    try:
                        return await func(*args, **kwargs)
                    except Exception as exception:
                        return await handler.aio_exception(
                            make_dec_data(exception)
                        )
                return async_func()
            else:
                try:
                    return func(*args, **kwargs)
                except Exception as exception:
                    return handler.exception(make_dec_data(exception))

        return wrapper

    if names_or_func and callable(names_or_func[0]):
        return _decor(names_or_func[0])
    else:
        return _decor
