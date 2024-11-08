class UnioqException(Exception):
    "Base unioq exception"


class MissingDependencies(UnioqException):
    "it is impossible to instantiate a class of type D, missing dependencies"

    def __init__(self, service_name: str, missing: list) -> None:
        super().__init__(
            f"It is impossible to instantiate a class of type {service_name}, missing dependencies: {missing}"
        )


class MissingService(UnioqException):
    def __init__(self, interface) -> None:
        super().__init__(f"Service {interface}, was not registred")
