import pytest

from unioq import ServiceProviderBuilder


def test_arguments_with_none():
    service_provider_builder = ServiceProviderBuilder()

    with pytest.raises(TypeError):
        service_provider_builder.add_transient(None, None)


def test_arguments_with_some():
    service_provider_builder = ServiceProviderBuilder()

    with pytest.raises(TypeError):
        service_provider_builder.add_transient(1, "sdf")
