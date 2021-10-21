from .data_classes import FuncInfo


def before_handler(func_info: FuncInfo):

    print("log before:", func_info)


def after_handler(func_info: FuncInfo):

    print("log after:", func_info)


def exc_handler(func_info: FuncInfo):

    print("log exc:", func_info)
