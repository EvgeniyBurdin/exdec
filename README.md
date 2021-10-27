# exdec

[![PyPI](https://img.shields.io/pypi/v/exdec)](https://pypi.org/project/exdec) [![build](https://github.com/EvgeniyBurdin/exdec/actions/workflows/python-app.yml/badge.svg?branch=main)](https://github.com/EvgeniyBurdin/exdec/actions/workflows/python-app.yml) [![codecov](https://codecov.io/gh/EvgeniyBurdin/exdec/branch/main/graph/badge.svg?token=YIJG8TN4DD)](https://codecov.io/gh/EvgeniyBurdin/exdec) [![Total alerts](https://img.shields.io/lgtm/alerts/g/EvgeniyBurdin/exdec.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/EvgeniyBurdin/exdec/alerts/) [![Language grade: Python](https://img.shields.io/lgtm/grade/python/g/EvgeniyBurdin/exdec.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/EvgeniyBurdin/exdec/context:python)

Decorator for catching exceptions in functions and methods. And also with the possibility of preliminary processing of incoming data, and post-processing of the function result.

- Works with both synchronous and asynchronous functions and methods;
- Catches exceptions of the required types;
- Three types of handlers are available: before the start of the function, after its end, and the exception handler;
- Handlers can be both synchronous and asynchronous;
- All current information about the function is available in any handler;
- Ability to change the incoming data and the result of the function in the handlers;
- Several ways to fine-tune and pre-configure the decorator;

## Decorator arguments

| name                                     | annotation                              | default                            |
|----------------------------------------- |---------------------------------------- |----------------------------------- |
| All positional arguments (i.e. `*args`)  | `Type[Exception]`                       | `Exception`                        |
| `exclude`                                | `bool`                                  | `False`                            |
| `before_handler`                         | `Optional[Callable[[FuncInfo],None]]`   | `None`                             |
| `after_handler`                          | `Optional[Callable[[FuncInfo],None]]`   | `None`                             |
| `exc_handler`                            | `Callable[[FuncInfo],Any]`              | `exdec.utils.default_exc_handler`  |
| `extra`                                  | `Any`                                   | `None`                             |
| `manager`                                | `exdec.manager.Manager`                 | `Manager()`                        |

If `exclude` set to `False`, then `exc_handler` will handle exceptions from `*args`.  If set to `True`, then `exc_handler` will handle all exceptions except those specified in `*args`.

In the `extra` argument you can specify arbitrary data to be passed to the handlers.

All handlers have an `FuncInfo` argument:

```python
# exdec/data_classes.py

@dataclass
class FuncInfo:
    """ Decorated function information.

    `result` will be available in the handler after calling the function if
    no exception occurs.

    If an exception occurs during the execution of the function, it will be
    stored in `exception`. This information will be available in the exception
    handler.
    """
    func: Callable
    args: Tuple[Any, ...]
    kwargs: Dict[str, Any]
    result: Any = None
    exception: Optional[Exception] = None
    extra: Any = None
    
...
```

## Installation

```bash
pip install exdec
```

## Quick start

More examples in the [examples folder](https://github.com/EvgeniyBurdin/exdec/tree/main/examples).

```python
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
    msg = f"Caught an exception! func_info={func_info}."
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

    # Catching only ZeroDivisionError
    @catch(ZeroDivisionError)
    def safe_div_5(self, x: int, y: int) -> Optional[float]:
        return x / y


math_functions = MathFunctions()
assert math_functions.safe_div_5(3, 0) is None


# 6 --------------------------------------------------------------------------

def exc_handler_reraise(func_info: FuncInfo) -> float:
    print(f"Caught an exception! func_info={func_info}. \n RERAISE!")
    raise func_info.exception


# Catching only (MyException_1, ZeroDivisionError) and reraise
@catch(MyException_1, ZeroDivisionError, exc_handler=exc_handler_reraise)
def div_6(x: int, y: int) -> float:
    return x / y


div_6(3, 0)  # ZeroDivisionError
```
