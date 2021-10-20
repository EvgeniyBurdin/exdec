import asyncio
import functools
from typing import Callable, Optional, Tuple, Type, Union

from .data_classes import DecData, FuncInfo
from .catcher import Catcher

catcher = Catcher()


def catch(
    *names_or_func,
    exceptions: Union[
        Tuple[Type[Exception], ...], Type[Exception]
    ] = Exception,
    exclude: bool = False,
    handler: Optional[Callable] = None,
    catcher: Catcher = catcher,
):
    def _decor(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):

            def make_dec_data(catched: Exception) -> DecData:
                return DecData(
                    exceptions=exceptions, exclude=exclude, handler=handler,
                    func_info=FuncInfo(
                        func=func, args=args, kwargs=kwargs, exception=catched,
                    ),
                )

            if asyncio.iscoroutinefunction(func):
                async def async_func():
                    try:
                        return await func(*args, **kwargs)
                    except Exception as exception:
                        return await catcher.aio_handle_exception(
                            make_dec_data(exception)
                        )
                return async_func()
            else:
                try:
                    return func(*args, **kwargs)
                except Exception as exception:
                    return catcher.handle_exception(make_dec_data(exception))

        return wrapper

    if names_or_func and callable(names_or_func[0]):
        return _decor(names_or_func[0])
    else:
        return _decor
