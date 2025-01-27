from unittest.mock import Mock

from unioq import ServiceProviderBuilder


class ApiService:
    def do_its_thing(self) -> str:
        return "response from api"


def test_factory():
    service_provider_builder = ServiceProviderBuilder()

    mock = Mock(return_value=ApiService())

    def some_factory() -> ApiService:
        return mock()

    service_provider_builder.add_transient(ApiService, some_factory)

    service_provider = service_provider_builder.build()

    resolved_service = service_provider.resolve(ApiService)

    assert isinstance(resolved_service, ApiService)

    mock.assert_called_once()
