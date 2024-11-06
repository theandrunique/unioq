from abc import ABC, abstractmethod

from unioq import ServiceProviderBuilder, ServiceScope


class IApiService(ABC):
    @abstractmethod
    def do_its_thing(self) -> str: ...


class ApiService(IApiService):
    def do_its_thing(self) -> str:
        return "response from api"


def test_singlton():
    service_provider_builder = ServiceProviderBuilder()

    service_provider_builder.register(IApiService, ApiService, ServiceScope.singleton)

    service_provider = service_provider_builder.build()

    api_service1 = service_provider.resolve(IApiService)
    api_service2 = service_provider.resolve(IApiService)

    assert id(api_service1) == id(api_service2)


def test_transient():
    service_provider_builder = ServiceProviderBuilder()

    service_provider_builder.register(IApiService, ApiService, ServiceScope.transient)

    service_provider = service_provider_builder.build()

    api_service1 = service_provider.resolve(IApiService)
    api_service2 = service_provider.resolve(IApiService)

    assert id(api_service1) != id(api_service2)
