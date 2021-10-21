from dataclasses import dataclass
from typing import Any, Callable, Dict, Optional, Tuple, Type, Union


@dataclass
class FuncInfo:
    func: Callable
    args: Tuple[Any, ...]
    kwargs: Dict[str, Any]
    exception: Optional[Exception] = None


@dataclass
class DecData:
    exceptions: Union[Tuple[Type[Exception], ...], Type[Exception]]
    exclude: bool
    before_handler: Callable[[FuncInfo], Any]
    after_handler: Callable[[FuncInfo], Any]
    exc_handler: Callable[[FuncInfo], Any]
    func_info: FuncInfo