from unioq import ServiceCollection


class HttpClient:
    def get(self) -> str:
        return "response_from_http_client"


class ApiService:
    def __init__(self, client: "HttpClient") -> None:
        self.client = client

    def do_its_thing(self) -> str:
        return f"response from api {self.client.get()}"


def test_string_annotations():
    service_collection = ServiceCollection()

    service_collection.add_transient(HttpClient)
    service_collection.add_transient(ApiService)

    service_provider = service_collection.build_service_provider()
    service_provider.resolve(ApiService)
