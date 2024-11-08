# uniq-ioq

## Example

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


def build_service_provider() -> ServiceProvider:
    service_provider_builder = ServiceProviderBuilder()

    service_provider_builder.add_transient(IApiService, MyApiService)

    service_provider = service_provider_builder.build()



service_provider = build_service_provider()


api_service = service_provider.resolve(IApiService)

print(api_service.get_data())
```

