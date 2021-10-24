from exdec.utils import (check_exception_class, check_handler,
                         default_exc_handler, try_reraise)

from exdec.data_classes import FuncInfo
from exdec.manager import Manager


def any_handler(FuncInfo: FuncInfo):
    pass


def any_func():
    pass


def test_init(manager: Manager):

    assert manager.exc_handler == default_exc_handler
    assert manager.check_exception_class == check_exception_class
    assert manager.check_handler == check_handler
    assert manager.try_reraise == try_reraise
    assert manager.default_exception_classes == (Exception, )


def test_make_handlers(manager: Manager):

    before_handler, after_handler, exc_handler = manager.make_handlers(
        any_handler, any_handler, any_handler
    )
    for handler in (before_handler, after_handler, exc_handler):
        assert handler == any_handler

    before_handler, after_handler, exc_handler = manager.make_handlers(
        None, None, None
    )
    assert before_handler is None
    assert after_handler is None
    assert exc_handler == manager.exc_handler


def test_make_exceptions(manager: Manager):

    exceptions = manager.make_exceptions(dec_args=tuple())
    assert exceptions == manager.default_exception_classes

    # @catch
    # def any_func():
    #     ...
    # This decorator will make dec_args=(any_func, )
    exceptions = manager.make_exceptions(dec_args=(any_func, ))
    assert exceptions == manager.default_exception_classes
