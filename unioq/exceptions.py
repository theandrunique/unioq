from collections.abc import Callable
from typing import Any, List, Type


class UnioqException(Exception):
    "Base unioq exception"


class MissingDependencies(UnioqException):
    def __init__(self, service_name: str, missing: List[Any]) -> None:
        super().__init__(
            f"It is impossible to instantiate a service instance '{service_name}', missing dependencies: {missing}."
        )


class MissingService(UnioqException):
    def __init__(self, interface: Type[Any]) -> None:
        super().__init__(f"Service '{interface}' was not registred.")


class ServiceAlreadyRegistred(UnioqException):
    def __init__(self, service_name: str, i: Callable[..., Any]) -> None:
        super().__init__(f"'{service_name}' has already been registred with '{i}'.")
