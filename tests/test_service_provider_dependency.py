from unioq import ServiceProviderBuilder
from unioq.service_provider import ServiceProvider


class SomeExternalService: ...


class ApiService:
    def __init__(self, service_provider: ServiceProvider) -> None:
        self.external_service = service_provider.resolve(SomeExternalService)

    def do_its_thing(self) -> str:
        return "response from api"


def test_service_provider_factory():
    service_provider_builder = ServiceProviderBuilder()

    service_provider_builder.add_transient(SomeExternalService)

    service_provider_builder.add_transient(ApiService)

    service_provider = service_provider_builder.build()

    service_provider.resolve(ApiService)
