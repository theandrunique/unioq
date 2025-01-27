from abc import ABC, abstractmethod

from unioq import ServiceCollection


class ITransport(ABC):
    @abstractmethod
    def read_data(self) -> str: ...


class SocketTransport(ITransport):
    def read_data(self) -> str:
        return "transport response"


class IHttpClient(ABC):
    @abstractmethod
    def get(self) -> str: ...


class HttpClient(IHttpClient):
    def __init__(self, transport: ITransport) -> None:
        self.transport = transport

    def get(self) -> str:
        response_from_transport = self.transport.read_data()
        return f"response_from_http_client, transport said: {response_from_transport}"


class IApiService(ABC):
    @abstractmethod
    def do_its_thing(self) -> str: ...


class ApiService(IApiService):
    def __init__(self, client: IHttpClient) -> None:
        self.client = client

    def do_its_thing(self) -> str:
        response = self.client.get()

        return f"response from api {response}"


def test_chain_dependencies():
    service_collection = ServiceCollection()

    service_collection.add_singleton(ITransport, SocketTransport)
    service_collection.add_singleton(IHttpClient, HttpClient)
    service_collection.add_singleton(IApiService, ApiService)

    service_provider = service_collection.build_service_provider()

    api_service = service_provider.resolve(IApiService)

    response = api_service.do_its_thing()

    assert response == "response from api response_from_http_client, transport said: transport response"
