from typing import Optional

from exdec.data_classes import FuncInfo
from exdec.decorator import catch


# 1 --------------------------------------------------------------------------

# Catching all exceptions
@catch
def safe_div_1(x: int, y: int) -> Optional[float]:
    return x / y


assert safe_div_1(3, 3) == 1.0
assert safe_div_1(3, 0) is None


# 2 --------------------------------------------------------------------------

# Catching only ZeroDivisionError
@catch(ZeroDivisionError)
def safe_div_2(x: int, y: int) -> Optional[float]:
    return x / y


assert safe_div_2(3, 0) is None


# 3 --------------------------------------------------------------------------

HANDLER_RESULT = 0.0


def exc_handler(func_info: FuncInfo) -> float:
    msg = f"Caught an exception, func_info={func_info}."
    print(f"{msg} Result changed to {HANDLER_RESULT}")
    return HANDLER_RESULT


# Catching only ZeroDivisionError
@catch(ZeroDivisionError, exc_handler=exc_handler)
def safe_div_3(x: int, y: int) -> float:
    return x / y


assert safe_div_3(3, 0) == HANDLER_RESULT


# 4 --------------------------------------------------------------------------

class MyException_1(Exception):
    pass


class MyException_2(Exception):
    pass


# Catching all exceptions, except for (MyException_1, MyException_2)
@catch(MyException_1, MyException_2, exclude=True, exc_handler=exc_handler)
def safe_div_4(x: int, y: int) -> float:
    return x / y


assert safe_div_4(3, 0) == HANDLER_RESULT


# 5 --------------------------------------------------------------------------

# For methods everything works the same
class MathFunctions:

    # Catching only MyException_1
    @catch(MyException_1)
    def safe_div_5(self, x: int, y: int) -> Optional[float]:
        return x / y


math_functions = MathFunctions()
assert math_functions.safe_div_5(3, 0) is None


# 6 --------------------------------------------------------------------------

def exc_handler_reraise(func_info: FuncInfo) -> float:
    exc = func_info.exception
    print(f"Caught an exception, func_info={func_info}. \n RERAISE!")
    raise exc


# Catching only (MyException_1, ZeroDivisionError) and reraise
@catch(MyException_1, ZeroDivisionError, exc_handler=exc_handler_reraise)
def div_6(x: int, y: int) -> float:
    return x / y


div_6(3, 0)  # ZeroDivisionError
