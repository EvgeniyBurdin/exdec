import inspect

from exdec.data_classes import FuncInfo
from exdec.handlers import after_handler, before_handler, exc_handler


def test_default_handlers(func_info: FuncInfo):

    for handler in (after_handler, before_handler, exc_handler):

        parameters = inspect.signature(handler).parameters
        assert len(parameters) == 1

        func_info_arg = parameters.get("func_info")
        assert func_info_arg is not None
        assert func_info_arg.annotation is FuncInfo

        assert handler(func_info) is None

    some_func_result = 1
    func_info.result = some_func_result
    assert exc_handler(func_info) == some_func_result
