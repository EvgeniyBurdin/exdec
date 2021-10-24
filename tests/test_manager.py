import asyncio
from typing import Any, Callable

from exdec.data_classes import DecData, FuncInfo
from exdec.manager import Manager, execute_wrapper
from exdec.utils import (check_exception_class, check_handler,
                         default_exc_handler, try_reraise)


class FakeManager:

    is_try_reraise_called = False

    def try_reraise(self, func_info: FuncInfo):
        self.is_try_reraise_called = True

    def execute_handler(self, handler: Callable, dec_data: DecData):
        return handler(dec_data.func_info)

    async def async_execute_handler(
        self, handler: Callable, dec_data: DecData
    ):
        return handler(dec_data.func_info)


def test_execute_wrapper(
    handler: Callable[[FuncInfo], Any], dec_data: DecData
):
    fm = FakeManager()

    _execute = execute_wrapper(FakeManager.execute_handler)
    result = _execute(fm, handler, dec_data)
    assert not fm.is_try_reraise_called
    assert result is None

    dec_data.func_info.exception = Exception()
    _execute = execute_wrapper(FakeManager.async_execute_handler)
    result = asyncio.run(_execute(fm, handler, dec_data))
    assert fm.is_try_reraise_called
    assert result is None


def test_init(manager: Manager):

    assert manager.exc_handler == default_exc_handler
    assert manager.check_exception_class == check_exception_class
    assert manager.check_handler == check_handler
    assert manager.try_reraise == try_reraise
    assert manager.default_exception_classes == (Exception, )


def test_make_handlers(manager: Manager, handler: Callable[[FuncInfo], Any]):

    before_handler, after_handler, exc_handler = manager.make_handlers(
        handler, handler, handler
    )
    for h in (before_handler, after_handler, exc_handler):
        assert h == handler

    before_handler, after_handler, exc_handler = manager.make_handlers(
        None, None, None
    )
    assert before_handler is None
    assert after_handler is None
    assert exc_handler == manager.exc_handler


class AnyException_1(Exception):
    pass


class AnyException_2(Exception):
    pass


def test_make_exceptions(manager: Manager, func: Callable):

    exceptions = manager.make_exceptions(dec_args=tuple())
    assert exceptions == manager.default_exception_classes

    # @catch
    # def any_func():
    #     ...
    # This decorator will make dec_args==(any_func, )
    exceptions = manager.make_exceptions(dec_args=(func, ))
    assert exceptions == manager.default_exception_classes

    exceptions = manager.make_exceptions(
        dec_args=(AnyException_1, AnyException_2, )
    )
    assert exceptions == (AnyException_1, AnyException_2, )
