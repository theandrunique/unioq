from typing import Any, Dict, List, Type, TypeVar

from .exceptions import MissingService
from .models import ServiceRegistration, ServiceScope

T = TypeVar("T")


class ServiceProvider:
    def __init__(self, services: Dict[Type[T], ServiceRegistration[T]]) -> None:
        self._service_registrations = services

    def resolve(self, interface: Type[T]) -> T:
        service_registration = self._service_registrations.get(interface)  # type: ignore
        if not service_registration:
            raise MissingService(interface)

        if service_registration.lifetime == ServiceScope.singleton:
            if not service_registration.instance:
                service_registration.instance = service_registration.service(
                    *self._resolve_dependencies(service_registration)
                )

            return service_registration.instance  # type: ignore

        return service_registration.service(*self._resolve_dependencies(service_registration))  # type: ignore

    def _resolve_dependencies(self, service_registration: ServiceRegistration[T]) -> List[Any]:
        dependency_instances = []

        for dependency_type in service_registration.args:
            dependency_instance = self.resolve(dependency_type)
            dependency_instances.append(dependency_instance)

        return dependency_instances
