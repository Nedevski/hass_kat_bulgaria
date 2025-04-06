"""Conftest."""

from unittest.mock import patch

from kat_bulgaria.errors import KatError, KatErrorSubtype, KatErrorType
import pytest

from homeassistant.components.kat_bulgaria.config_flow import DOMAIN

from . import (
    EGN_VALID,
    MOCK_DATA_BUSINESS,
    MOCK_DATA_INDIVIDUAL,
    MOCK_DATA_PERSON_TYPE_BUSINESS,
    MOCK_DATA_PERSON_TYPE_INDIVIDUAL,
    MOCK_DATA_V1,
)

from tests.common import MockConfigEntry

# region coordinator setup


@pytest.fixture(name="config_entry_v1")
def mock_config_entry_v1() -> MockConfigEntry:
    """Fixture for a config entry."""
    return MockConfigEntry(
        domain=DOMAIN, data=MOCK_DATA_V1, unique_id=EGN_VALID, version=1
    )


@pytest.fixture(name="config_entry_v2_individual")
def mock_config_entry_v2_individual() -> MockConfigEntry:
    """Fixture for a config entry."""
    return MockConfigEntry(
        domain=DOMAIN,
        data={**MOCK_DATA_PERSON_TYPE_INDIVIDUAL, **MOCK_DATA_INDIVIDUAL},
        unique_id=EGN_VALID,
        version=2,
    )


@pytest.fixture(name="config_entry_v2_business")
def mock_config_entry_v2__business() -> MockConfigEntry:
    """Fixture for a config entry."""
    return MockConfigEntry(
        domain=DOMAIN,
        data={**MOCK_DATA_PERSON_TYPE_BUSINESS, **MOCK_DATA_BUSINESS},
        unique_id=EGN_VALID,
        version=2,
    )


@pytest.fixture(name="mock_get_obligations_ok_nodata")
def mock_get_obligations_ok_nodata():
    """Mock get obligations."""

    with patch(
        "homeassistant.components.kat_bulgaria.kat_client.KatClient.get_obligations"
    ) as mock_get_obligations:
        mock_get_obligations.return_value = []
        yield


@pytest.fixture(name="mock_get_obligations_err_usernotfound")
def mock_get_obligations_err_usernotfound():
    """Mock get obligations."""

    with patch(
        "homeassistant.components.kat_bulgaria.kat_client.KatClient.get_obligations"
    ) as mock_get_obligations:
        mock_get_obligations.side_effect = KatError(
            KatErrorType.API_ERROR,
            KatErrorSubtype.VALIDATION_USER_NOT_FOUND_ONLINE,
            "error text",
        )
        yield


@pytest.fixture(name="mock_get_obligations_err_driving_license_invalid")
def mock_get_obligations_err_driving_license_invalid():
    """Mock get obligations."""

    with patch(
        "homeassistant.components.kat_bulgaria.kat_client.KatClient.get_obligations"
    ) as mock_get_obligations:
        mock_get_obligations.side_effect = KatError(
            KatErrorType.VALIDATION_ERROR,
            KatErrorSubtype.VALIDATION_DRIVING_LICENSE_INVALID,
            "error text",
        )
        yield


@pytest.fixture(name="mock_get_obligations_err_gov_id_number_invalid")
def mock_get_obligations_err_gov_id_number_invalid():
    """Mock get obligations."""

    with patch(
        "homeassistant.components.kat_bulgaria.kat_client.KatClient.get_obligations"
    ) as mock_get_obligations:
        mock_get_obligations.side_effect = KatError(
            KatErrorType.VALIDATION_ERROR,
            KatErrorSubtype.VALIDATION_GOV_ID_NUMBER_INVALID,
            "error text",
        )
        yield


@pytest.fixture(name="mock_get_obligations_err_bulstat_invalid")
def mock_get_obligations_err_bulstat_invalid():
    """Mock get obligations."""

    with patch(
        "homeassistant.components.kat_bulgaria.kat_client.KatClient.get_obligations"
    ) as mock_get_obligations:
        mock_get_obligations.side_effect = KatError(
            KatErrorType.VALIDATION_ERROR,
            KatErrorSubtype.VALIDATION_GOV_ID_NUMBER_INVALID,
            "error text",
        )
        yield


@pytest.fixture(name="mock_get_obligations_err_api_timeout")
def mock_get_obligations_err_api_timeout():
    """Mock get obligations."""

    with patch(
        "homeassistant.components.kat_bulgaria.kat_client.KatClient.get_obligations"
    ) as mock_get_obligations:
        mock_get_obligations.side_effect = KatError(
            KatErrorType.API_ERROR, KatErrorSubtype.API_TIMEOUT, "error text"
        )
        yield


@pytest.fixture(name="mock_get_obligations_err_api_toomanyrequests")
def mock_get_obligations_err_api_toomanyrequests():
    """Mock get obligations."""

    with patch(
        "homeassistant.components.kat_bulgaria.kat_client.KatClient.get_obligations"
    ) as mock_get_obligations:
        mock_get_obligations.side_effect = KatError(
            KatErrorType.API_ERROR, KatErrorSubtype.API_TOO_MANY_REQUESTS, "error text"
        )
        yield


@pytest.fixture(name="mock_get_obligations_err_api_errorreadingdata")
def mock_get_obligations_err_api_errorreadingdata():
    """Mock get obligations."""

    with patch(
        "homeassistant.components.kat_bulgaria.kat_client.KatClient.get_obligations"
    ) as mock_get_obligations:
        mock_get_obligations.side_effect = KatError(
            KatErrorType.API_ERROR, KatErrorSubtype.API_ERROR_READING_DATA, "error text"
        )
        yield


@pytest.fixture(name="mock_get_obligations_err_api_invalidschema")
def mock_get_obligations_err_api_invalidschema():
    """Mock get obligations."""

    with patch(
        "homeassistant.components.kat_bulgaria.kat_client.KatClient.get_obligations"
    ) as mock_get_obligations:
        mock_get_obligations.side_effect = KatError(
            KatErrorType.API_ERROR, KatErrorSubtype.API_INVALID_SCHEMA, "error text"
        )
        yield


@pytest.fixture(name="mock_get_obligations_err_api_unknown")
def mock_get_obligations_err_api_unknown():
    """Mock get obligations."""

    with patch(
        "homeassistant.components.kat_bulgaria.kat_client.KatClient.get_obligations"
    ) as mock_get_obligations:
        mock_get_obligations.side_effect = KatError(
            KatErrorType.API_ERROR, KatErrorSubtype.API_UNKNOWN_ERROR, "error text"
        )
        yield
