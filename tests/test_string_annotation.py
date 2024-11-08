from abc import ABC, abstractmethod

from unioq import ServiceProviderBuilder


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
    def __init__(self, client: "IHttpClient") -> None:
        self.client = client

    def do_its_thing(self) -> str:
        return "response from api"


def test_string_annotations():
    service_provider_builder = ServiceProviderBuilder()

    service_provider_builder.add_transient(IHttpClient, HttpClient)
    service_provider_builder.add_transient(IApiService, ApiService)

    service_provider = service_provider_builder.build()
    service_provider.resolve(IApiService)
