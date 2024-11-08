import inspect


def get_service_name_by_interface(interface: type) -> str:
    return interface.__name__


def resolve_dependencies(service):
    constructor = inspect.signature(service)

    dependencies = []

    for name, param in constructor.parameters.items():
        if name == "self":
            continue

        dependency_cls = param.annotation

        dependencies.append(dependency_cls)

    return dependencies
