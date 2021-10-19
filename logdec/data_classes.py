from dataclasses import dataclass
from typing import Callable, Optional, Tuple, Union


@dataclass
class FuncInfo:
    func: Callable
    args: tuple
    kwargs: dict
    owner_instance: Optional[object] = None


@dataclass
class DecData:
    exception: Exception
    no_reraise: Union[Tuple[Exception, ...], Exception]
    callback: Optional[Callable]
    func_info: FuncInfo
