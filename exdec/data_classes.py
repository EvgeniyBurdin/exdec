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
    before_handler: Optional[Callable[[FuncInfo], Any]]
    after_handler: Optional[Callable[[FuncInfo], Any]]
    exc_handler: Optional[Callable[[FuncInfo], Any]]
    func_info: FuncInfo
