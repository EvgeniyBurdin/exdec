from dataclasses import dataclass
from typing import Any, Callable, Dict, Optional, Tuple, Type, Union


@dataclass
class FuncInfo:
    func: Callable
    args: Tuple[Any, ...]
    kwargs: Dict[str, Any]
    exception: Exception
    owner: Optional[str] = None


@dataclass
class DecData:
    exceptions: Union[Tuple[Type[Exception], ...], Type[Exception]]
    exclude: bool
    handler: Optional[Callable[[FuncInfo], Any]]
    func_info: FuncInfo
