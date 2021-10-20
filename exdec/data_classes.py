from dataclasses import dataclass
from typing import Callable, Optional, Tuple, Type, Union


@dataclass
class FuncInfo:
    func: Callable
    args: tuple
    kwargs: dict
    exception: Exception
    owner_instance: Optional[object] = None


@dataclass
class DecData:
    exceptions: Union[Tuple[Type[Exception], ...], Type[Exception]]
    exclude: bool
    handler: Optional[Callable]
    func_info: FuncInfo
