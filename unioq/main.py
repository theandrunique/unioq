import inspect
from dataclasses import dataclass
from enum import Enum
from typing import Any

from .exceptions import MissingDependencies, MissingDependency


class Helper:
    @staticmethod
    def get_service_name_by_interface(interface: type) -> str:
        return type(interface).__name__

    @staticmethod
    def resolve_dependencies(service):
        constructor = inspect.signature(service)

        dependencies = []

        for name, param in constructor.parameters.items():
            if name == "self":
                continue

            dependency_cls = param.annotation

            dependencies.append(dependency_cls)

        return dependencies


class ServiceScope(Enum):
    transient = "transient"
    singleton = "singleton"
    scoped = "scoped"


@dataclass
class ServiceRegistration:
    name: str
    service: type
    lifetime: ServiceScope
    args: list[Any]
    instance: Any = None


class ServiceProvider:
    def __init__(self, services: dict[type, ServiceRegistration]) -> None:
        self._services = services

    def resolve[T](self, interface: type[T]) -> T:
        service_registration = self._services.get(interface)
        if not service_registration:
            raise MissingDependency(interface)

        if service_registration.instance:
            return service_registration.instance

        dependency_instances = []

        for dependency_type in service_registration.args:
            dependency_instance = self.resolve(dependency_type)
            dependency_instances.append(dependency_instance)

        if service_registration.lifetime == ServiceScope.singleton:
            service_registration.instance = service_registration.service(*dependency_instances)
            return service_registration.instance

        return service_registration.service(*dependency_instances)


class ServiceProviderBuilder:
    def __init__(self) -> None:
        self.services: dict[type, ServiceRegistration] = {}

    def register(self, interface, service, scope: ServiceScope) -> None:
        service_name = Helper.get_service_name_by_interface(interface)
        dependencies = Helper.resolve_dependencies(service)

        registration = ServiceRegistration(service_name, service, scope, dependencies)

        self.services[interface] = registration

    def build(self) -> ServiceProvider:
        missing_dependencies = []

        for service in self.services.values():
            for service_dependencies in service.args:
                if service_dependencies not in self.services:
                    missing_dependencies.append(service_dependencies)

            if missing_dependencies:
                raise MissingDependencies(missing_dependencies)

        return ServiceProvider(self.services)
