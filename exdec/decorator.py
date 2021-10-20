import asyncio
import functools
from typing import Any, Callable, Optional

from .catcher import Catcher
from .data_classes import DecData, FuncInfo

catcher = Catcher()


class ExDecCatchException(Exception):
    pass


EX_MSG = "The positional arguments of the 'cath' decorator must be subclasses "
EX_MSG += "of Exception. But received:"


def catch(
    *exceptions_or_func,
    exclude: bool = False,
    handler: Optional[Callable[[FuncInfo], Any]] = None,
    catcher: Catcher = catcher,
):
    exceptions = exceptions_or_func
    if not exceptions or not type(exceptions[0]) is type:
        exceptions = (Exception, )

    for exc in exceptions:
        if not type(exc) is type or not issubclass(exc, Exception):
            msg = "The positional arguments of the 'cath' decorator must be "
            msg += "subclasses of Exception. But received: "
            msg += f"{msg}{exc}, type={type(exc)}."
            raise ExDecCatchException(msg)

    def _decor(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):

            def make_dec_data(exception: Exception) -> DecData:
                return DecData(
                    exceptions=exceptions, exclude=exclude, handler=handler,
                    func_info=FuncInfo(
                        func=func, args=args, kwargs=kwargs,
                        exception=exception,
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

    if exceptions_or_func and callable(exceptions_or_func[0]) \
       and not type(exceptions_or_func[0]) is type:
        return _decor(exceptions_or_func[0])
    else:
        return _decor
