"""Test KAT Bulgaria setup process."""

from unittest.mock import AsyncMock, patch

from kat_bulgaria.errors import KatError, KatErrorType
import pytest

from homeassistant.components.kat_bulgaria import const as kat_constants
from homeassistant.components.kat_bulgaria.config_flow import (
    STEP_ID_BUSINESS,
    STEP_ID_INDIVIDUAL,
    STEP_ID_USER,
)
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResultType

from . import (
    BULSTAT_VALID,
    EGN_VALID,
    MOCK_DATA_BUSINESS,
    MOCK_DATA_INDIVIDUAL,
    MOCK_DATA_PERSON_TYPE_BUSINESS,
    MOCK_DATA_PERSON_TYPE_INDIVIDUAL,
    MOCK_NAME,
    PATCH_VALIDATE_CREDS_BUSINESS,
    PATCH_VALIDATE_CREDS_INDIVIDUAL,
)

from tests.common import MockConfigEntry


@pytest.mark.asyncio
async def test_flow_init_nodata_opens_configflow(hass: HomeAssistant) -> None:
    """Test config flow."""

    config_flow_user = await hass.config_entries.flow.async_init(
        kat_constants.DOMAIN, context={"source": STEP_ID_USER}
    )
    assert config_flow_user["type"] is FlowResultType.FORM
    assert config_flow_user["step_id"] == STEP_ID_USER

    config_flow_individual = await hass.config_entries.flow.async_configure(
        config_flow_user["flow_id"],
    )
    await hass.async_block_till_done()

    assert config_flow_individual["type"] is FlowResultType.FORM
    assert config_flow_individual["step_id"] == STEP_ID_USER


@pytest.mark.asyncio
async def test_flow_init_individual(hass: HomeAssistant) -> None:
    """Test config flow."""

    config_flow_user = await hass.config_entries.flow.async_init(
        kat_constants.DOMAIN, context={"source": STEP_ID_USER}
    )
    assert config_flow_user["type"] is FlowResultType.FORM
    assert config_flow_user["step_id"] == STEP_ID_USER

    config_flow_individual = await hass.config_entries.flow.async_configure(
        config_flow_user["flow_id"],
        user_input=MOCK_DATA_PERSON_TYPE_INDIVIDUAL,
    )
    await hass.async_block_till_done()

    assert config_flow_individual["type"] is FlowResultType.FORM
    assert config_flow_individual["step_id"] == STEP_ID_INDIVIDUAL


@pytest.mark.asyncio
async def test_flow_init_business(hass: HomeAssistant) -> None:
    """Test config flow."""

    config_flow_user = await hass.config_entries.flow.async_init(
        kat_constants.DOMAIN, context={"source": STEP_ID_USER}
    )
    assert config_flow_user["type"] is FlowResultType.FORM
    assert config_flow_user["step_id"] == STEP_ID_USER

    config_flow_business = await hass.config_entries.flow.async_configure(
        config_flow_user["flow_id"],
        user_input=MOCK_DATA_PERSON_TYPE_BUSINESS,
    )
    await hass.async_block_till_done()

    assert config_flow_business["type"] is FlowResultType.FORM
    assert config_flow_business["step_id"] == STEP_ID_BUSINESS


@pytest.mark.asyncio
@patch(PATCH_VALIDATE_CREDS_INDIVIDUAL, AsyncMock(return_value=True))
async def test_flow_individual(hass: HomeAssistant) -> None:
    """Test config flow."""

    config_flow_individual = await hass.config_entries.flow.async_init(
        kat_constants.DOMAIN,
        context={"source": STEP_ID_INDIVIDUAL},
        data=MOCK_DATA_PERSON_TYPE_INDIVIDUAL,
    )

    config_result = await hass.config_entries.flow.async_configure(
        config_flow_individual["flow_id"],
        user_input=MOCK_DATA_INDIVIDUAL,
    )
    await hass.async_block_till_done()

    assert config_result["type"] is FlowResultType.CREATE_ENTRY
    assert config_result["title"] == MOCK_NAME
    assert config_result["data"] == MOCK_DATA_INDIVIDUAL


@pytest.mark.asyncio
@patch(PATCH_VALIDATE_CREDS_BUSINESS, AsyncMock(return_value=True))
async def test_flow_business(hass: HomeAssistant) -> None:
    """Test config flow."""

    config_flow_individual = await hass.config_entries.flow.async_init(
        kat_constants.DOMAIN,
        context={"source": STEP_ID_BUSINESS},
        data=MOCK_DATA_PERSON_TYPE_BUSINESS,
    )

    config_result = await hass.config_entries.flow.async_configure(
        config_flow_individual["flow_id"],
        user_input=MOCK_DATA_BUSINESS,
    )
    await hass.async_block_till_done()

    assert config_result["type"] is FlowResultType.CREATE_ENTRY
    assert config_result["title"] == MOCK_NAME
    assert config_result["data"] == MOCK_DATA_BUSINESS


@pytest.mark.asyncio
@patch(
    PATCH_VALIDATE_CREDS_INDIVIDUAL,
    AsyncMock(side_effect=KatError(KatErrorType.VALIDATION_EGN_INVALID, "error text")),
)
async def test_flow_error_egn_invalid_individual(hass: HomeAssistant) -> None:
    """Test config flow."""

    config_flow_individual = await hass.config_entries.flow.async_init(
        kat_constants.DOMAIN,
        context={"source": STEP_ID_INDIVIDUAL},
        data=MOCK_DATA_PERSON_TYPE_INDIVIDUAL,
    )

    config_result = await hass.config_entries.flow.async_configure(
        config_flow_individual["flow_id"],
        user_input=MOCK_DATA_INDIVIDUAL,
    )
    await hass.async_block_till_done()

    assert config_result["type"] is FlowResultType.FORM
    assert config_result["errors"] == {"base": "invalid_config"}


@pytest.mark.asyncio
@patch(
    PATCH_VALIDATE_CREDS_BUSINESS,
    AsyncMock(side_effect=KatError(KatErrorType.VALIDATION_EGN_INVALID, "error text")),
)
async def test_flow_error_egn_invalid_business(hass: HomeAssistant) -> None:
    """Test config flow."""

    config_flow_individual = await hass.config_entries.flow.async_init(
        kat_constants.DOMAIN,
        context={"source": STEP_ID_BUSINESS},
        data=MOCK_DATA_PERSON_TYPE_BUSINESS,
    )

    config_result = await hass.config_entries.flow.async_configure(
        config_flow_individual["flow_id"],
        user_input=MOCK_DATA_BUSINESS,
    )
    await hass.async_block_till_done()

    assert config_result["type"] is FlowResultType.FORM
    assert config_result["errors"] == {"base": "invalid_config"}


@pytest.mark.asyncio
@patch(
    PATCH_VALIDATE_CREDS_INDIVIDUAL,
    AsyncMock(
        side_effect=KatError(
            KatErrorType.VALIDATION_USER_NOT_FOUND_ONLINE, "error text"
        )
    ),
)
async def test_flow_error_notfoundonline_individual(hass: HomeAssistant) -> None:
    """Test config flow."""

    config_flow_individual = await hass.config_entries.flow.async_init(
        kat_constants.DOMAIN,
        context={"source": STEP_ID_INDIVIDUAL},
        data=MOCK_DATA_PERSON_TYPE_INDIVIDUAL,
    )

    config_result = await hass.config_entries.flow.async_configure(
        config_flow_individual["flow_id"],
        user_input=MOCK_DATA_INDIVIDUAL,
    )
    await hass.async_block_till_done()

    assert config_result["type"] is FlowResultType.FORM
    assert config_result["errors"] == {"base": "invalid_config"}


@pytest.mark.asyncio
@patch(
    PATCH_VALIDATE_CREDS_BUSINESS,
    AsyncMock(
        side_effect=KatError(
            KatErrorType.VALIDATION_USER_NOT_FOUND_ONLINE, "error text"
        )
    ),
)
async def test_flow_error_notfoundonline_business(hass: HomeAssistant) -> None:
    """Test config flow."""

    config_flow_individual = await hass.config_entries.flow.async_init(
        kat_constants.DOMAIN,
        context={"source": STEP_ID_BUSINESS},
        data=MOCK_DATA_PERSON_TYPE_BUSINESS,
    )

    config_result = await hass.config_entries.flow.async_configure(
        config_flow_individual["flow_id"],
        user_input=MOCK_DATA_BUSINESS,
    )
    await hass.async_block_till_done()

    assert config_result["type"] is FlowResultType.FORM
    assert config_result["errors"] == {"base": "invalid_config"}


@pytest.mark.asyncio
@patch(
    PATCH_VALIDATE_CREDS_INDIVIDUAL,
    AsyncMock(
        side_effect=KatError(KatErrorType.VALIDATION_ID_DOCUMENT_INVALID, "error text")
    ),
)
async def test_flow_error_invalid_document_individual(hass: HomeAssistant) -> None:
    """Test config flow."""

    config_flow_individual = await hass.config_entries.flow.async_init(
        kat_constants.DOMAIN,
        context={"source": STEP_ID_INDIVIDUAL},
        data=MOCK_DATA_PERSON_TYPE_INDIVIDUAL,
    )

    config_result = await hass.config_entries.flow.async_configure(
        config_flow_individual["flow_id"],
        user_input=MOCK_DATA_INDIVIDUAL,
    )
    await hass.async_block_till_done()

    assert config_result["type"] is FlowResultType.FORM
    assert config_result["errors"] == {"base": "invalid_config"}


@pytest.mark.asyncio
@patch(
    PATCH_VALIDATE_CREDS_BUSINESS,
    AsyncMock(
        side_effect=KatError(KatErrorType.VALIDATION_ID_DOCUMENT_INVALID, "error text")
    ),
)
async def test_flow_error_invalid_document_business(hass: HomeAssistant) -> None:
    """Test config flow."""

    config_flow_individual = await hass.config_entries.flow.async_init(
        kat_constants.DOMAIN,
        context={"source": STEP_ID_BUSINESS},
        data=MOCK_DATA_PERSON_TYPE_BUSINESS,
    )

    config_result = await hass.config_entries.flow.async_configure(
        config_flow_individual["flow_id"],
        user_input=MOCK_DATA_BUSINESS,
    )
    await hass.async_block_till_done()

    assert config_result["type"] is FlowResultType.FORM
    assert config_result["errors"] == {"base": "invalid_config"}


@pytest.mark.asyncio
@patch(
    PATCH_VALIDATE_CREDS_INDIVIDUAL,
    AsyncMock(side_effect=KatError(KatErrorType.API_TIMEOUT, "error text")),
)
async def test_flow_error_api_timeout_individual(hass: HomeAssistant) -> None:
    """Test config flow."""

    config_flow_individual = await hass.config_entries.flow.async_init(
        kat_constants.DOMAIN,
        context={"source": STEP_ID_INDIVIDUAL},
        data=MOCK_DATA_PERSON_TYPE_INDIVIDUAL,
    )

    config_result = await hass.config_entries.flow.async_configure(
        config_flow_individual["flow_id"],
        user_input=MOCK_DATA_INDIVIDUAL,
    )
    await hass.async_block_till_done()

    assert config_result["type"] is FlowResultType.FORM
    assert config_result["errors"] == {"base": "cannot_connect"}


@pytest.mark.asyncio
@patch(
    PATCH_VALIDATE_CREDS_BUSINESS,
    AsyncMock(side_effect=KatError(KatErrorType.API_TIMEOUT, "error text")),
)
async def test_flow_error_api_timeout_business(hass: HomeAssistant) -> None:
    """Test config flow."""

    config_flow_individual = await hass.config_entries.flow.async_init(
        kat_constants.DOMAIN,
        context={"source": STEP_ID_BUSINESS},
        data=MOCK_DATA_PERSON_TYPE_BUSINESS,
    )

    config_result = await hass.config_entries.flow.async_configure(
        config_flow_individual["flow_id"],
        user_input=MOCK_DATA_BUSINESS,
    )
    await hass.async_block_till_done()

    assert config_result["type"] is FlowResultType.FORM
    assert config_result["errors"] == {"base": "cannot_connect"}


@pytest.mark.asyncio
@patch(
    PATCH_VALIDATE_CREDS_INDIVIDUAL,
    AsyncMock(side_effect=KatError(KatErrorType.API_ERROR_READING_DATA, "error text")),
)
async def test_flow_error_api_error_reading_data_individual(
    hass: HomeAssistant,
) -> None:
    """Test config flow."""

    config_flow_individual = await hass.config_entries.flow.async_init(
        kat_constants.DOMAIN,
        context={"source": STEP_ID_INDIVIDUAL},
        data=MOCK_DATA_PERSON_TYPE_INDIVIDUAL,
    )

    config_result = await hass.config_entries.flow.async_configure(
        config_flow_individual["flow_id"],
        user_input=MOCK_DATA_INDIVIDUAL,
    )
    await hass.async_block_till_done()

    assert config_result["type"] is FlowResultType.FORM
    assert config_result["errors"] == {"base": "cannot_connect"}


@pytest.mark.asyncio
@patch(
    PATCH_VALIDATE_CREDS_BUSINESS,
    AsyncMock(side_effect=KatError(KatErrorType.API_ERROR_READING_DATA, "error text")),
)
async def test_flow_error_api_error_reading_data_business(hass: HomeAssistant) -> None:
    """Test config flow."""

    config_flow_individual = await hass.config_entries.flow.async_init(
        kat_constants.DOMAIN,
        context={"source": STEP_ID_BUSINESS},
        data=MOCK_DATA_PERSON_TYPE_BUSINESS,
    )

    config_result = await hass.config_entries.flow.async_configure(
        config_flow_individual["flow_id"],
        user_input=MOCK_DATA_BUSINESS,
    )
    await hass.async_block_till_done()

    assert config_result["type"] is FlowResultType.FORM
    assert config_result["errors"] == {"base": "cannot_connect"}


@pytest.mark.asyncio
@patch(
    PATCH_VALIDATE_CREDS_INDIVIDUAL,
    AsyncMock(side_effect=KatError(KatErrorType.API_INVALID_SCHEMA, "error text")),
)
async def test_flow_error_api_invalid_schema_individual(
    hass: HomeAssistant,
) -> None:
    """Test config flow."""

    config_flow_individual = await hass.config_entries.flow.async_init(
        kat_constants.DOMAIN,
        context={"source": STEP_ID_INDIVIDUAL},
        data=MOCK_DATA_PERSON_TYPE_INDIVIDUAL,
    )

    config_result = await hass.config_entries.flow.async_configure(
        config_flow_individual["flow_id"],
        user_input=MOCK_DATA_INDIVIDUAL,
    )
    await hass.async_block_till_done()

    assert config_result["type"] is FlowResultType.FORM
    assert config_result["errors"] == {"base": "cannot_connect"}


@pytest.mark.asyncio
@patch(
    PATCH_VALIDATE_CREDS_BUSINESS,
    AsyncMock(side_effect=KatError(KatErrorType.API_INVALID_SCHEMA, "error text")),
)
async def test_flow_error_api_invalid_schema_business(hass: HomeAssistant) -> None:
    """Test config flow."""

    config_flow_individual = await hass.config_entries.flow.async_init(
        kat_constants.DOMAIN,
        context={"source": STEP_ID_BUSINESS},
        data=MOCK_DATA_PERSON_TYPE_BUSINESS,
    )

    config_result = await hass.config_entries.flow.async_configure(
        config_flow_individual["flow_id"],
        user_input=MOCK_DATA_BUSINESS,
    )
    await hass.async_block_till_done()

    assert config_result["type"] is FlowResultType.FORM
    assert config_result["errors"] == {"base": "cannot_connect"}


@pytest.mark.asyncio
@patch(
    PATCH_VALIDATE_CREDS_INDIVIDUAL,
    AsyncMock(side_effect=KatError(KatErrorType.API_TOO_MANY_REQUESTS, "error text")),
)
async def test_flow_error_api_too_many_requests_individual(
    hass: HomeAssistant,
) -> None:
    """Test config flow."""

    config_flow_individual = await hass.config_entries.flow.async_init(
        kat_constants.DOMAIN,
        context={"source": STEP_ID_INDIVIDUAL},
        data=MOCK_DATA_PERSON_TYPE_INDIVIDUAL,
    )

    config_result = await hass.config_entries.flow.async_configure(
        config_flow_individual["flow_id"],
        user_input=MOCK_DATA_INDIVIDUAL,
    )
    await hass.async_block_till_done()

    assert config_result["type"] is FlowResultType.FORM
    assert config_result["errors"] == {"base": "cannot_connect"}


@pytest.mark.asyncio
@patch(
    PATCH_VALIDATE_CREDS_BUSINESS,
    AsyncMock(side_effect=KatError(KatErrorType.API_TOO_MANY_REQUESTS, "error text")),
)
async def test_flow_error_api_too_many_requests_business(hass: HomeAssistant) -> None:
    """Test config flow."""

    config_flow_individual = await hass.config_entries.flow.async_init(
        kat_constants.DOMAIN,
        context={"source": STEP_ID_BUSINESS},
        data=MOCK_DATA_PERSON_TYPE_BUSINESS,
    )

    config_result = await hass.config_entries.flow.async_configure(
        config_flow_individual["flow_id"],
        user_input=MOCK_DATA_BUSINESS,
    )
    await hass.async_block_till_done()

    assert config_result["type"] is FlowResultType.FORM
    assert config_result["errors"] == {"base": "cannot_connect"}


@pytest.mark.asyncio
@patch(
    PATCH_VALIDATE_CREDS_INDIVIDUAL,
    AsyncMock(side_effect=KatError(KatErrorType.API_UNKNOWN_ERROR, "error text")),
)
async def test_flow_error_api_unknown_error_individual(
    hass: HomeAssistant,
) -> None:
    """Test config flow."""

    config_flow_individual = await hass.config_entries.flow.async_init(
        kat_constants.DOMAIN,
        context={"source": STEP_ID_INDIVIDUAL},
        data=MOCK_DATA_PERSON_TYPE_INDIVIDUAL,
    )

    config_result = await hass.config_entries.flow.async_configure(
        config_flow_individual["flow_id"],
        user_input=MOCK_DATA_INDIVIDUAL,
    )
    await hass.async_block_till_done()

    assert config_result["type"] is FlowResultType.FORM
    assert config_result["errors"] == {"base": "cannot_connect"}


@pytest.mark.asyncio
@patch(
    PATCH_VALIDATE_CREDS_BUSINESS,
    AsyncMock(side_effect=KatError(KatErrorType.API_UNKNOWN_ERROR, "error text")),
)
async def test_flow_error_api_unknown_error_business(hass: HomeAssistant) -> None:
    """Test config flow."""

    config_flow_individual = await hass.config_entries.flow.async_init(
        kat_constants.DOMAIN,
        context={"source": STEP_ID_BUSINESS},
        data=MOCK_DATA_PERSON_TYPE_BUSINESS,
    )

    config_result = await hass.config_entries.flow.async_configure(
        config_flow_individual["flow_id"],
        user_input=MOCK_DATA_BUSINESS,
    )
    await hass.async_block_till_done()

    assert config_result["type"] is FlowResultType.FORM
    assert config_result["errors"] == {"base": "cannot_connect"}


@pytest.mark.asyncio
@patch(PATCH_VALIDATE_CREDS_INDIVIDUAL, AsyncMock(return_value=True))
async def test_flow_error_already_configured_individual(
    hass: HomeAssistant,
) -> None:
    """Test config flow."""

    entry = MockConfigEntry(
        domain=kat_constants.DOMAIN,
        data=MOCK_DATA_INDIVIDUAL,
        unique_id=EGN_VALID,
    )
    entry.add_to_hass(hass)

    config_flow_individual = await hass.config_entries.flow.async_init(
        kat_constants.DOMAIN,
        context={"source": STEP_ID_INDIVIDUAL},
        data=MOCK_DATA_PERSON_TYPE_INDIVIDUAL,
    )

    config_result = await hass.config_entries.flow.async_configure(
        config_flow_individual["flow_id"],
        user_input=MOCK_DATA_INDIVIDUAL,
    )
    await hass.async_block_till_done()

    assert config_result["type"] is FlowResultType.ABORT
    assert config_result["reason"] == "already_configured"


@pytest.mark.asyncio
@patch(PATCH_VALIDATE_CREDS_BUSINESS, AsyncMock(return_value=True))
async def test_flow_error_already_configured_business(
    hass: HomeAssistant,
) -> None:
    """Test config flow."""

    entry = MockConfigEntry(
        domain=kat_constants.DOMAIN,
        data=MOCK_DATA_BUSINESS,
        unique_id=BULSTAT_VALID,
    )
    entry.add_to_hass(hass)

    config_flow_individual = await hass.config_entries.flow.async_init(
        kat_constants.DOMAIN,
        context={"source": STEP_ID_BUSINESS},
        data=MOCK_DATA_PERSON_TYPE_BUSINESS,
    )

    config_result = await hass.config_entries.flow.async_configure(
        config_flow_individual["flow_id"],
        user_input=MOCK_DATA_BUSINESS,
    )
    await hass.async_block_till_done()

    assert config_result["type"] is FlowResultType.ABORT
    assert config_result["reason"] == "already_configured"
