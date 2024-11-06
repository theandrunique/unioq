from abc import ABC, abstractmethod

import pytest

from unioq import MissingService, ServiceProviderBuilder


class IApiService(ABC):
    @abstractmethod
    def do_its_thing(self) -> str: ...


class ApiService(IApiService):
    def do_its_thing(self) -> str:
        return "response from api"


def test_exception_missing_dependencies():
    service_provider_builder = ServiceProviderBuilder()
    service_provider = service_provider_builder.build()

    with pytest.raises(MissingService):
        service_provider.resolve(IApiService)
