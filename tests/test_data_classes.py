from exdec.data_classes import FuncInfo


def test_func_info_default_None_fields(func_info: FuncInfo):

    assert func_info.result is None
    assert func_info.exception is None
