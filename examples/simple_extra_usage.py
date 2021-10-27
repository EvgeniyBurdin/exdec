from exdec.data_classes import FuncInfo
from exdec.decorator import catch


_EXTRA_RU = "ru"


def exc_handler(func_info: FuncInfo) -> float:

    if func_info.extra == _EXTRA_RU:
        message = "Поймано исключение!"
    else:
        message = "Caught an exception!"

    print(message, f"func_info={func_info}. \n RERAISE!")

    raise func_info.exception


# Catching only ZeroDivisionError and reraise
@catch(ZeroDivisionError, exc_handler=exc_handler, extra=_EXTRA_RU)
def div(x: int, y: int) -> float:
    return x / y


div(3, 0)  # ZeroDivisionError
