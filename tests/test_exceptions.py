from abc import ABC, abstractmethod
from typing import Any

import pytest

from unioq import ServiceCollection
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
        response = self.client.get()
        return f"response from api: {response}"


def test_missing_dependencies_exception():
    service_collection = ServiceCollection()

    service_collection.add_singleton(IApiService, ApiService)

    with pytest.raises(MissingDependencies):
        service_collection.build_service_provider()


def test_missing_service_exception():
    service_collection = ServiceCollection()
    service_provider = service_collection.build_service_provider()

    with pytest.raises(MissingService):
        service_provider.resolve(IApiService)


def test_already_registred_exception():
    service_collection = ServiceCollection()
    service_collection.add_transient(IApiService, ApiService)
    with pytest.raises(ServiceAlreadyRegistred):
        service_collection.add_transient(IApiService, ApiService)


def test_type_error_with_factory():
    service_collection = ServiceCollection()

    def some_factory() -> IHttpClient:
        return HttpClient()

    with pytest.raises(TypeError):
        service_collection.add_transient(IApiService, some_factory)


def test_type_error_with_service():
    service_collection = ServiceCollection()

    with pytest.raises(TypeError):
        service_collection.add_transient(IApiService, HttpClient)


def test_missing_annotations_error():
    service_collection = ServiceCollection()

    def factory(some_arg) -> IHttpClient:
        return HttpClient()

    with pytest.raises(ValueError):
        service_collection.add_transient(IHttpClient, factory)


def test_any_annotations_error():
    service_collection = ServiceCollection()

    def factory(some_arg: Any) -> IHttpClient:
        return HttpClient()

    with pytest.raises(ValueError):
        service_collection.add_transient(IHttpClient, factory)
