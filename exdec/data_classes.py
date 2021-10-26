""" Module with used data classes.
"""
from dataclasses import dataclass
from typing import Any, Callable, Dict, Optional, Tuple, Type


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


@dataclass
class DecData:
    """ Data available inside the decorator.

    If `exclude` set to `True`, then the decorator will not catch `exceptions`.
    If in `False`, then the decorator will catch only `exceptions`.
    """
    exceptions: Tuple[Type[Exception], ...]
    exclude: bool
    func_info: FuncInfo
