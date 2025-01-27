## unioq

This lib was made by me and for me, but you still free to use it.

Type-safe Dependency Injection lib for Python.

## Example

```python
from abc import ABC, abstractmethod

from unioq import ServiceCollection, ServiceProvider


class IApiService(ABC):
    @abstractmethod
    def get_data(self) -> int: ...


class MyApiService(IApiService):
    def get_data(self) -> int:
        return 10


def build_service_provider() -> ServiceProvider:
    service_collection = ServiceCollection()

    service_collection.add_transient(IApiService, MyApiService)

    return service_collection.build_service_provider()


service_provider = build_service_provider()

api_service = service_provider.resolve(IApiService)

print(api_service.get_data())
```

