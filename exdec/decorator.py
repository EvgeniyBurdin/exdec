import asyncio
import functools
from typing import Any, Callable, Optional

from .data_classes import DecData, FuncInfo
from .manager import Manager

manager = Manager()


def catch(
    *dec_args,
    exclude: bool = False,
    before_handler: Optional[Callable[[FuncInfo], Any]] = None,
    after_handler: Optional[Callable[[FuncInfo], Any]] = None,
    exc_handler: Optional[Callable[[FuncInfo], Any]] = None,
    manager: Manager = manager,
):
    exceptions = manager.make_exceptions(dec_args)
    before_handler, after_handler, exc_handler = manager.make_handlers(
        before_handler, after_handler, exc_handler
    )

    def decor(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):

            dec_data = DecData(
                exceptions=exceptions,
                exclude=exclude,
                func_info=FuncInfo(func=func, args=args, kwargs=kwargs),
            )

            if asyncio.iscoroutinefunction(func):
                async def async_func():
                    try:
                        await manager.aio_execute_handler(
                            before_handler, dec_data
                        )
                        result = await func(*args, **kwargs)
                        await manager.aio_execute_handler(
                            after_handler, dec_data
                        )
                    except Exception as exception:
                        dec_data.func_info.exception = exception
                        result = await manager.aio_execute_handler(
                            exc_handler, dec_data
                        )
                    return result
                wrapper_result = async_func()
            else:
                try:
                    manager.execute_handler(before_handler, dec_data)
                    wrapper_result = func(*args, **kwargs)
                    manager.execute_handler(after_handler, dec_data)
                except Exception as exception:
                    dec_data.func_info.exception = exception
                    wrapper_result = manager.execute_handler(
                        exc_handler, dec_data
                    )

            return wrapper_result

        return wrapper

    if dec_args and callable(dec_args[0]) and not type(dec_args[0]) is type:
        return decor(dec_args[0])
    else:
        return decor
