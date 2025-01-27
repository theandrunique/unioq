import pytest

from unioq import ServiceCollection


def test_arguments_with_none():
    service_collection = ServiceCollection()

    with pytest.raises(TypeError):
        service_collection.add_transient(None, None)


def test_arguments_with_some():
    service_collection = ServiceCollection()

    with pytest.raises(TypeError):
        service_collection.add_transient(1, "sdf")
