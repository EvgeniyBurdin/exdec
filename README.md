# exdec

[![PyPI](https://img.shields.io/pypi/v/exdec)](https://pypi.org/project/exdec) [![Total alerts](https://img.shields.io/lgtm/alerts/g/EvgeniyBurdin/exdec.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/EvgeniyBurdin/exdec/alerts/) [![Language grade: Python](https://img.shields.io/lgtm/grade/python/g/EvgeniyBurdin/exdec.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/EvgeniyBurdin/exdec/context:python)

Decorator for catching exceptions in functions and methods.

## Installation

```bash
pip install exdec
```

## Quick start

```python
from typing import Optional

from exdec.data_classes import FuncInfo
from exdec.decorator import catch


# 1 --------------------------------------------------------------------------

# Catching all exceptions
@catch
def safe_div_1(x: int, y: int) -> Optional[float]:
    result = x / y
    return result


z = safe_div_1(3, 3)
assert z == 1.0
z = safe_div_1(3, 0)
assert z is None


# 2 --------------------------------------------------------------------------

# Catching only ZeroDivisionError
@catch(ZeroDivisionError)
def safe_div_2(x: int, y: int) -> Optional[float]:
    result = x / y
    return result


z = safe_div_2(3, 0)
assert z is None


# 3 --------------------------------------------------------------------------

HANDLER_RESULT = 0.0


def exc_handler(func_info: FuncInfo) -> float:
    exc = func_info.exception
    print(f"Caught an exception {type(exc)}: {exc}.")
    fname = func_info.func.__name__
    args = func_info.args
    print(f"Result {fname}{args} changed to {HANDLER_RESULT}")
    return HANDLER_RESULT


# Catching only ZeroDivisionError
@catch(ZeroDivisionError, exc_handler=exc_handler)
def safe_div_3(x: int, y: int) -> float:
    result = x / y
    return result


z = safe_div_3(3, 0)
assert z == HANDLER_RESULT


# 4 --------------------------------------------------------------------------

class MyException_1(Exception):
    pass


class MyException_2(Exception):
    pass


# Catching all exceptions, except for (MyException_1, MyException_2)
@catch(MyException_1, MyException_2, exclude=True, exc_handler=exc_handler)
def safe_div_4(x: int, y: int) -> float:
    result = x / y
    return result


z = safe_div_4(3, 0)
assert z == HANDLER_RESULT


# 5 --------------------------------------------------------------------------

def exc_handler_reraise(func_info: FuncInfo) -> float:
    exc = func_info.exception
    print(f">>> Caught an exception {type(exc)}: {exc}. \nRERAISE!")
    raise exc


# Catching only (MyException_1, ZeroDivisionError) and reraise
@catch(MyException_1, ZeroDivisionError, exc_handler=exc_handler_reraise)
def div(x: int, y: int) -> float:
    result = x / y
    return result


z = div(3, 0)
```
