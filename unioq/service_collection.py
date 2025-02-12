import inspect
from collections.abc import Callable
from typing import Any, Type, TypeVar

from .exceptions import MissingDependencies, ServiceAlreadyRegistred
from .helper import check_service_return_type, get_dependencies_types, get_type_name
from .models import ServiceRegistration, ServiceScope
from .service_provider import ServiceProvider

T = TypeVar("T")


class ServiceCollection:
    def __init__(self) -> None:
        self._service_registrations: dict[Type[Any], ServiceRegistration[Any]] = {}

    def add_transient(self, interface: Type[T], service: Callable[..., T] | None = None) -> None:
        return self.add_service(interface, service, ServiceScope.transient)

    def add_singleton(self, interface: Type[T], service: Callable[..., T] | None = None) -> None:
        return self.add_service(interface, service, ServiceScope.singleton)

    def add_service(
        self,
        interface: Type[T],
        service: Callable[..., T] | None = None,
        scope: ServiceScope = ServiceScope.transient,
    ) -> None:
        if service is None:
            service = interface

        if interface is None or not inspect.isclass(interface):
            raise TypeError(f"Expected 'interface' to be a class type, but got {type(interface).__name__}")

        if not callable(service):
            raise TypeError(f"Expected 'service' to be a callable, but got {type(service).__name__}")

        if not isinstance(scope, ServiceScope):
            raise TypeError(f"Expected 'scope' to be ServiceScope, but got {type(scope).__name__}")

        try:
            check_service_return_type(interface, service)
        except TypeError as e:
            raise e

        if registred_service := self._service_registrations.get(interface):
            raise ServiceAlreadyRegistred(registred_service.name, registred_service.service)

        service_name = get_type_name(interface)

        dependencies = get_dependencies_types(service)

        registration = ServiceRegistration(service_name, service, scope, dependencies)

        self._service_registrations[interface] = registration

    def build_service_provider(self) -> ServiceProvider:
        missing_dependencies = []
        service_provider = ServiceProvider(self._service_registrations)
        self._service_registrations[ServiceProvider] = ServiceRegistration(
            ServiceProvider.__name__, ServiceProvider, ServiceScope.singleton, [], instance=service_provider
        )

        for service in self._service_registrations.values():
            for service_dependency in service.args:
                if service_dependency not in self._service_registrations:
                    missing_dependencies.append(service_dependency)

            if missing_dependencies:
                raise MissingDependencies(service.name, missing_dependencies)

        return service_provider
