from unioq import ServiceProviderBuilder


class HttpClient:
    def get(self) -> str:
        return "response_from_http_client"


class ApiService:
    def __init__(self, client: "HttpClient") -> None:
        self.client = client

    def do_its_thing(self) -> str:
        return f"response from api {self.client.get()}"


def test_string_annotations():
    service_provider_builder = ServiceProviderBuilder()

    service_provider_builder.add_transient(HttpClient)
    service_provider_builder.add_transient(ApiService)

    service_provider = service_provider_builder.build()
    service_provider.resolve(ApiService)
