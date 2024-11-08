from collections.abc import Callable
from dataclasses import dataclass
from enum import Enum
from typing import Any

from .exceptions import MissingDependencies, MissingService
from .helper import get_service_name_by_interface, resolve_dependencies


class ServiceScope(Enum):
    transient = "transient"
    singleton = "singleton"
    scoped = "scoped"


@dataclass
class ServiceRegistration[T]:
    name: str
    service: Callable[..., T]
    lifetime: ServiceScope
    args: list[Any]
    instance: T | None = None


class ServiceProvider:
    def __init__[T](self, services: dict[type[T], ServiceRegistration[T]]) -> None:
        self._services = services

    def resolve[T](self, interface: type[T]) -> T:
        service_registration = self._services.get(interface)
        if not service_registration:
            raise MissingService(interface)

        if service_registration.lifetime == ServiceScope.singleton:
            if not service_registration.instance:
                service_registration.instance = service_registration.service(
                    *self.resolve_dependencies(service_registration)
                )

            return service_registration.instance

        return service_registration.service(*self.resolve_dependencies(service_registration))

    def resolve_dependencies(self, service_registration: ServiceRegistration) -> list[Any]:
        dependency_instances = []

        for dependency_type in service_registration.args:
            dependency_instance = self.resolve(dependency_type)
            dependency_instances.append(dependency_instance)

        return dependency_instances


class ServiceProviderBuilder:
    def __init__(self) -> None:
        self.services: dict[type, ServiceRegistration] = {}

    def register_transient[T](self, interface: type[T], service: Callable[..., T]) -> None:
        return self.register(interface, service, ServiceScope.transient)

    def register_singleton[T](self, interface: type[T], service: Callable[..., T]) -> None:
        return self.register(interface, service, ServiceScope.singleton)

    def register[T](self, interface: type[T], service: Callable[..., T], scope: ServiceScope) -> None:
        service_name = get_service_name_by_interface(interface)
        dependencies = resolve_dependencies(service)

        registration = ServiceRegistration(service_name, service, scope, dependencies)

        self.services[interface] = registration

    def build(self) -> ServiceProvider:
        missing_dependencies = []

        for service in self.services.values():
            for service_dependencies in service.args:
                if service_dependencies not in self.services:
                    missing_dependencies.append(service_dependencies)

            if missing_dependencies:
                raise MissingDependencies(service.name, missing_dependencies)

        return ServiceProvider(self.services)
