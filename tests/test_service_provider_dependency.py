from unioq import ServiceCollection
from unioq.service_provider import ServiceProvider


class SomeExternalService: ...


class ApiService:
    def __init__(self, service_provider: ServiceProvider) -> None:
        self.external_service = service_provider.resolve(SomeExternalService)

    def do_its_thing(self) -> str:
        return "response from api"


def test_service_provider_factory():
    service_collection = ServiceCollection()

    service_collection.add_transient(SomeExternalService)

    service_collection.add_transient(ApiService)

    service_provider = service_collection.build_service_provider()

    service_provider.resolve(ApiService)
