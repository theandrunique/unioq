# uniq-ioq

## Interface

```python
from unioq import ServiceProviderBuilder, ServiceProvider, ServiceScope
from abc import ABC, abstractmethod


class IApiService(ABC):
    @abstractmethod
    def get_data(self) -> int:
        ...


class MyApiService(IApiService):
    def get_data(self) -> int:
        return 10


def build_ioq_container() -> ServiceProvider:
    service_provider_builder = ServiceProviderBuilder()

    service_provider_builder.register(IApiService, MyApiService, ServiceScope.TRANSIENT)

    service_provider = service_provider_builder.build()



service_provider = build_ioq_container()


api_service = service_provider.resolve(IApiService)

print(api_service.get_data())
```

