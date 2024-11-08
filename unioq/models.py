from collections.abc import Callable
from dataclasses import dataclass
from enum import Enum
from typing import Any, Generic, List, Optional, TypeVar

T = TypeVar("T")


class ServiceScope(Enum):
    transient = "transient"
    singleton = "singleton"
    scoped = "scoped"


@dataclass
class ServiceRegistration(Generic[T]):
    name: str
    service: Callable[..., T]
    lifetime: ServiceScope
    args: List[Any]
    instance: Optional[T] = None
