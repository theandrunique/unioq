from abc import ABC, abstractmethod

import pytest

from unioq import MissingDependencies, ServiceProviderBuilder, ServiceScope


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


def test_exception_missing_dependencies():
    service_provider_builder = ServiceProviderBuilder()

    service_provider_builder.register(IApiService, ApiService, ServiceScope.singleton)

    with pytest.raises(MissingDependencies):
        service_provider = service_provider_builder.build()
