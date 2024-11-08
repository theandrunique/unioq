from abc import ABC, abstractmethod

import pytest

from unioq import ServiceProviderBuilder
from unioq.exceptions import MissingDependencies, MissingService, ServiceAlreadyRegistred


class IHttpClient(ABC):
    @abstractmethod
    def get(self) -> str: ...


class HttpClient(IHttpClient):
    def get(self) -> str:
        return "response_from_http_client"


class IApiService(ABC):
    @abstractmethod
    def do_its_thing(self) -> str: ...


class ApiService(IApiService):
    def __init__(self, client: IHttpClient) -> None:
        self.client = client

    def do_its_thing(self) -> str:
        return "response from api"


def test_missing_dependencies_exception():
    service_provider_builder = ServiceProviderBuilder()

    service_provider_builder.add_singleton(IApiService, ApiService)

    with pytest.raises(MissingDependencies):
        service_provider_builder.build()


def test_missing_service_exception():
    service_provider_builder = ServiceProviderBuilder()
    service_provider = service_provider_builder.build()

    with pytest.raises(MissingService):
        service_provider.resolve(IApiService)


def test_already_registred_exception():
    service_provider_builder = ServiceProviderBuilder()
    service_provider_builder.add_transient(IApiService, ApiService)
    with pytest.raises(ServiceAlreadyRegistred):
        service_provider_builder.add_transient(IApiService, ApiService)


def test_type_error_with_factory():
    service_provider_builder = ServiceProviderBuilder()

    def some_factory() -> IHttpClient:
        return HttpClient()

    with pytest.raises(TypeError):
        service_provider_builder.add_transient(IApiService, some_factory)


def test_type_error_with_service():
    service_provider_builder = ServiceProviderBuilder()

    with pytest.raises(TypeError):
        service_provider_builder.add_transient(IApiService, HttpClient)
