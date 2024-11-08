from abc import ABC, abstractmethod

from unioq import ServiceProviderBuilder


class IApiService(ABC):
    @abstractmethod
    def do_its_thing(self) -> str: ...


class ApiService(IApiService):
    def do_its_thing(self) -> str:
        return "response from api"


def test_factory():
    service_provider_builder = ServiceProviderBuilder()

    def some_factory() -> ApiService:
        return ApiService()

    service_provider_builder.add_transient(IApiService, some_factory)

    service_provider = service_provider_builder.build()

    service_provider.resolve(IApiService)
