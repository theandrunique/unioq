from unioq import ServiceProviderBuilder


class ApiService:
    def do_its_thing(self) -> str:
        return "response from api"


def test_singlton():
    service_provider_builder = ServiceProviderBuilder()

    service_provider_builder.add_singleton(ApiService)

    service_provider = service_provider_builder.build()

    api_service1 = service_provider.resolve(ApiService)
    api_service2 = service_provider.resolve(ApiService)

    assert id(api_service1) == id(api_service2)


def test_transient():
    service_provider_builder = ServiceProviderBuilder()

    service_provider_builder.add_transient(ApiService)

    service_provider = service_provider_builder.build()

    api_service1 = service_provider.resolve(ApiService)
    api_service2 = service_provider.resolve(ApiService)

    assert id(api_service1) != id(api_service2)
