from unioq import ServiceCollection


class ApiService:
    def do_its_thing(self) -> str:
        return "response from api"


def test_singlton():
    service_collection = ServiceCollection()

    service_collection.add_singleton(ApiService)

    service_provider = service_collection.build_service_provider()

    api_service1 = service_provider.resolve(ApiService)
    api_service2 = service_provider.resolve(ApiService)

    assert id(api_service1) == id(api_service2)


def test_transient():
    service_collection = ServiceCollection()

    service_collection.add_transient(ApiService)

    service_provider = service_collection.build_service_provider()

    api_service1 = service_provider.resolve(ApiService)
    api_service2 = service_provider.resolve(ApiService)

    assert id(api_service1) != id(api_service2)
