from unittest.mock import Mock

from unioq import ServiceCollection


class ApiService:
    def do_its_thing(self) -> str:
        return "response from api"


def test_factory():
    service_collection = ServiceCollection()

    mock = Mock(return_value=ApiService())

    def some_factory() -> ApiService:
        return mock()

    service_collection.add_transient(ApiService, some_factory)

    service_provider = service_collection.build_service_provider()

    resolved_service = service_provider.resolve(ApiService)

    assert isinstance(resolved_service, ApiService)

    mock.assert_called_once()
