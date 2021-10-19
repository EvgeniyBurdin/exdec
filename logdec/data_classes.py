from dataclasses import dataclass
from typing import Callable, Optional, Tuple, Type, Union


@dataclass
class FuncInfo:
    func: Callable
    args: tuple
    kwargs: dict
    owner_instance: Optional[object] = None


@dataclass
class DecData:
    exception: Exception
    no_reraise: Union[Tuple[Type[Exception], ...], Type[Exception]]
    callback: Optional[Callable]
    func_info: FuncInfo
