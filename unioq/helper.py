import inspect
from typing import Any, Callable, List, Type, TypeVar, get_origin, get_type_hints

T = TypeVar("T")


def get_type_name(t: Type[Any]) -> str:
    return t.__name__


def get_dependencies_types(service: Callable[..., Any]) -> List[type]:
    if inspect.isclass(service):
        type_hints = get_type_hints(service.__init__)
    else:
        type_hints = get_type_hints(service)

    constructor = inspect.signature(service)
    dependencies = []

    for name, param in constructor.parameters.items():
        if name == "self":
            continue

        dependency_cls = type_hints.get(name, param.annotation)

        if dependency_cls is inspect.Signature.empty or dependency_cls is Any:
            raise ValueError(f"Parameter '{name}' in '{service}' is missing a specific type annotation.")

        dependencies.append(dependency_cls)

    return dependencies


def check_service_return_type(interface: Type[T], service: Callable[..., T]) -> None:
    service_name = getattr(service, "__name__", str(service))

    if inspect.isclass(service):
        if not issubclass(service, interface):
            raise TypeError(f"The class '{service_name}' does not match the given interface '{interface.__name__}'.")
    elif callable(service):
        signature = inspect.signature(service)

        return_annotation = signature.return_annotation

        if return_annotation is inspect.Signature.empty:
            raise TypeError(f"The factory function '{service_name}' must have a return type annotation.")

        origin_type = get_origin(return_annotation) or return_annotation
        if not (issubclass(origin_type, interface) or origin_type == interface):
            raise TypeError(
                f"The factory function '{service_name}' return type '{return_annotation}' "
                f"does not match the given interface '{interface.__name__}'."
            )
    else:
        raise TypeError("Expecting a callable object in a service field.")
