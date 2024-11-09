from abc import ABC, abstractmethod

from unioq import ServiceProviderBuilder
from unioq.service_provider import ServiceProvider


class SomeExternalService: ...


class IApiService(ABC):
    @abstractmethod
    def do_its_thing(self) -> str: ...


class ApiService(IApiService):
    def __init__(self, service_provider: ServiceProvider) -> None:
        self.external_service = service_provider.resolve(SomeExternalService)

    def do_its_thing(self) -> str:
        return "response from api"


def test_service_provider_factory():
    service_provider_builder = ServiceProviderBuilder()

    service_provider_builder.add_transient(SomeExternalService, SomeExternalService)

    service_provider_builder.add_transient(IApiService, ApiService)

    service_provider = service_provider_builder.build()

    service_provider.resolve(IApiService)
