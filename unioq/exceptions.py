class UnioqException(Exception):
    "Base unioq exception"


class MissingDependencies(UnioqException):
    "it is impossible to instantiate a class of type D, missing dependencies"

    def __init__(self, missing: list) -> None:
        super().__init__(
            f"it is impossible to instantiate a class of type D, missing dependencies: {missing}"
        )


class MissingDependency(UnioqException):
    def __init__(self, interface) -> None:
        super().__init__(f"Service {interface}, was not registred")
