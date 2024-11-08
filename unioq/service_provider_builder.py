from collections.abc import Callable
from typing import Any, Type, TypeVar

from .exceptions import MissingDependencies, ServiceAlreadyRegistred
from .helper import check_service_return_type, get_dependencies_types, get_type_name
from .models import ServiceRegistration, ServiceScope
from .service_provider import ServiceProvider

T = TypeVar("T")


class ServiceProviderBuilder:
    def __init__(self) -> None:
        self._service_registrations: dict[Type[Any], ServiceRegistration[Any]] = {}

    def register_transient(self, interface: Type[T], service: Callable[..., T]) -> None:
        return self.register(interface, service, ServiceScope.transient)

    def register_singleton(self, interface: Type[T], service: Callable[..., T]) -> None:
        return self.register(interface, service, ServiceScope.singleton)

    def register(self, interface: Type[T], service: Callable[..., T], scope: ServiceScope) -> None:
        check_service_return_type(interface, service)

        if registred_service := self._service_registrations.get(interface):
            raise ServiceAlreadyRegistred(registred_service.name, registred_service.service)

        service_name = get_type_name(interface)

        dependencies = get_dependencies_types(service)

        registration = ServiceRegistration(service_name, service, scope, dependencies)

        self._service_registrations[interface] = registration

    def build(self) -> ServiceProvider:
        missing_dependencies = []

        for service in self._service_registrations.values():
            for service_dependencies in service.args:
                if service_dependencies not in self._service_registrations:
                    missing_dependencies.append(service_dependencies)

            if missing_dependencies:
                raise MissingDependencies(service.name, missing_dependencies)

        return ServiceProvider(self._service_registrations)
