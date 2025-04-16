"""Conftest."""

from unittest.mock import patch

from kat_bulgaria.errors import KatError, KatErrorSubtype, KatErrorType
import pytest

from pytest_homeassistant_custom_component.common import MockConfigEntry

from custom_components.kat_bulgaria.config_flow import DOMAIN
from custom_components.kat_bulgaria.const import CONF_PERSON_TYPE

from . import (
    EGN_VALID,
    MOCK_DATA_BUSINESS_FULL,
    MOCK_DATA_INDIVIDUAL,
    MOCK_DATA_INDIVIDUAL_FULL,
    MOCK_DATA_V1,
)


# region coordinator setup

PATCH_GET_OBLIGATIONS = (
    "custom_components.kat_bulgaria.kat_client.KatClient.get_obligations"
)
TEST_ERROR_TEXT = "error text"


@pytest.fixture(autouse=True)
def auto_enable_custom_integrations(enable_custom_integrations):
    """Automatically enable loading custom integrations in all tests."""
    # This fixture enables loading custom integrations in all tests.
    # Remove to enable selective use of this fixture
    yield


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
        data=MOCK_DATA_INDIVIDUAL_FULL,
        unique_id=EGN_VALID,
        version=2,
    )


@pytest.fixture(name="config_entry_v2_business")
def mock_config_entry_v2_business() -> MockConfigEntry:
    """Fixture for a config entry."""
    return MockConfigEntry(
        domain=DOMAIN,
        data=MOCK_DATA_BUSINESS_FULL,
        unique_id=EGN_VALID,
        version=2,
    )


@pytest.fixture(name="config_entry_v2_invalid_person_type")
def mock_config_entry_v2_invalid_person_type() -> MockConfigEntry:
    """Fixture for a config entry."""
    mock_data = {
        CONF_PERSON_TYPE: "something invalid",
        **MOCK_DATA_INDIVIDUAL
    }

    return MockConfigEntry(
        domain=DOMAIN,
        data=mock_data,
        unique_id=EGN_VALID,
        version=2,
    )


@pytest.fixture(name="mock_get_obligations_ok_nodata")
def mock_get_obligations_ok_nodata():
    """Mock get obligations."""

    with patch(PATCH_GET_OBLIGATIONS) as mock_get_obligations:
        mock_get_obligations.return_value = []
        yield


@pytest.fixture(name="mock_get_obligations_err_usernotfound")
def mock_get_obligations_err_usernotfound():
    """Mock get obligations."""

    with patch(PATCH_GET_OBLIGATIONS) as mock_get_obligations:
        mock_get_obligations.side_effect = KatError(
            KatErrorType.API_ERROR,
            KatErrorSubtype.VALIDATION_USER_NOT_FOUND_ONLINE,
            TEST_ERROR_TEXT,
        )
        yield


@pytest.fixture(name="mock_get_obligations_err_driving_license_invalid")
def mock_get_obligations_err_driving_license_invalid():
    """Mock get obligations."""

    with patch(PATCH_GET_OBLIGATIONS) as mock_get_obligations:
        mock_get_obligations.side_effect = KatError(
            KatErrorType.VALIDATION_ERROR,
            KatErrorSubtype.VALIDATION_DRIVING_LICENSE_INVALID,
            TEST_ERROR_TEXT,
        )
        yield


@pytest.fixture(name="mock_get_obligations_err_gov_id_number_invalid")
def mock_get_obligations_err_gov_id_number_invalid():
    """Mock get obligations."""

    with patch(PATCH_GET_OBLIGATIONS) as mock_get_obligations:
        mock_get_obligations.side_effect = KatError(
            KatErrorType.VALIDATION_ERROR,
            KatErrorSubtype.VALIDATION_GOV_ID_NUMBER_INVALID,
            TEST_ERROR_TEXT,
        )
        yield


@pytest.fixture(name="mock_get_obligations_err_bulstat_invalid")
def mock_get_obligations_err_bulstat_invalid():
    """Mock get obligations."""

    with patch(PATCH_GET_OBLIGATIONS) as mock_get_obligations:
        mock_get_obligations.side_effect = KatError(
            KatErrorType.VALIDATION_ERROR,
            KatErrorSubtype.VALIDATION_GOV_ID_NUMBER_INVALID,
            TEST_ERROR_TEXT,
        )
        yield


@pytest.fixture(name="mock_get_obligations_err_api_timeout")
def mock_get_obligations_err_api_timeout():
    """Mock get obligations."""

    with patch(PATCH_GET_OBLIGATIONS) as mock_get_obligations:
        mock_get_obligations.side_effect = KatError(
            KatErrorType.API_ERROR, KatErrorSubtype.API_TIMEOUT, TEST_ERROR_TEXT
        )
        yield


@pytest.fixture(name="mock_get_obligations_err_api_toomanyrequests")
def mock_get_obligations_err_api_toomanyrequests():
    """Mock get obligations."""

    with patch(PATCH_GET_OBLIGATIONS) as mock_get_obligations:
        mock_get_obligations.side_effect = KatError(
            KatErrorType.API_ERROR,
            KatErrorSubtype.API_TOO_MANY_REQUESTS,
            TEST_ERROR_TEXT,
        )
        yield


@pytest.fixture(name="mock_get_obligations_err_api_errorreadingdata")
def mock_get_obligations_err_api_errorreadingdata():
    """Mock get obligations."""

    with patch(PATCH_GET_OBLIGATIONS) as mock_get_obligations:
        mock_get_obligations.side_effect = KatError(
            KatErrorType.API_ERROR,
            KatErrorSubtype.API_ERROR_READING_DATA,
            TEST_ERROR_TEXT,
        )
        yield


@pytest.fixture(name="mock_get_obligations_err_api_invalidschema")
def mock_get_obligations_err_api_invalidschema():
    """Mock get obligations."""

    with patch(PATCH_GET_OBLIGATIONS) as mock_get_obligations:
        mock_get_obligations.side_effect = KatError(
            KatErrorType.API_ERROR, KatErrorSubtype.API_INVALID_SCHEMA, TEST_ERROR_TEXT
        )
        yield


@pytest.fixture(name="mock_get_obligations_err_api_unknown")
def mock_get_obligations_err_api_unknown():
    """Mock get obligations."""

    with patch(PATCH_GET_OBLIGATIONS) as mock_get_obligations:
        mock_get_obligations.side_effect = KatError(
            KatErrorType.API_ERROR, KatErrorSubtype.API_UNKNOWN_ERROR, TEST_ERROR_TEXT
        )
        yield
