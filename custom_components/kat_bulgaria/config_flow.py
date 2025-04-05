"""Config flow for KAT Bulgaria integration."""

from __future__ import annotations

import logging
from typing import Any

from kat_bulgaria.errors import KatError, KatErrorType
import voluptuous as vol

from homeassistant.config_entries import ConfigFlow, ConfigFlowResult
from homeassistant.helpers.selector import SelectSelector, SelectSelectorConfig

from .const import (
    CONF_BULSTAT,
    CONF_DOCUMENT_NUMBER,
    CONF_PERSON_EGN,
    CONF_PERSON_NAME,
    CONF_PERSON_TYPE,
    DOMAIN,
    PersonType,
)
from .kat_client import KatClient

_LOGGER = logging.getLogger(__name__)

SCHEMA_START = vol.Schema(
    {
        vol.Required(CONF_PERSON_TYPE, default=PersonType.INDIVIDUAL): SelectSelector(
            SelectSelectorConfig(
                options=[PersonType.INDIVIDUAL, PersonType.BUSINESS],
                translation_key=CONF_PERSON_TYPE,
            )
        )
    }
)

SCHEMA_PERSON = vol.Schema(
    {
        vol.Required(CONF_PERSON_NAME): str,
        vol.Required(CONF_PERSON_EGN): str,
        vol.Required(CONF_DOCUMENT_NUMBER): str,
    }
)

SCHEMA_BUSINESS = vol.Schema(
    {
        vol.Required(CONF_PERSON_NAME): str,
        vol.Required(CONF_PERSON_EGN): str,
        vol.Required(CONF_DOCUMENT_NUMBER): str,
        vol.Required(CONF_BULSTAT): str,
    }
)


class ConfigFlowHandler(ConfigFlow, domain=DOMAIN):
    """Handle a config flow for kat_bulgaria."""

    VERSION = 2

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Handle the initial step."""

        # If no input, show default form
        if user_input is None:
            return self.async_show_form(step_id="user", data_schema=SCHEMA_START)

        person_type = user_input[CONF_PERSON_TYPE]

        if person_type == PersonType.INDIVIDUAL:
            return await self.async_step_individual(user_input)
        if person_type == PersonType.BUSINESS:
            return await self.async_step_business(user_input)

        # If we reach here, something went wrong.
        _LOGGER.error("Invalid person type: %s", person_type)

        # Show the form again with an error
        return self.async_show_form(
            step_id="user",
            data_schema=SCHEMA_START,
            errors={"base": "invalid_type"},
        )

    async def async_step_individual(
        self, user_input: dict[str, Any]
    ) -> ConfigFlowResult:
        """Handle the initial step."""

        if len(user_input) == 1:
            return self.async_show_form(step_id="individual", data_schema=SCHEMA_PERSON)

        # Init user input values & init KatClient
        # user_input[CONF_PERSON_TYPE] = PersonType.INDIVIDUAL

        user_name = user_input[CONF_PERSON_NAME]
        user_egn = user_input[CONF_PERSON_EGN]
        user_license_number = user_input[CONF_DOCUMENT_NUMBER]

        kat_client = KatClient(
            self.hass,
            PersonType.INDIVIDUAL,
            user_name,
            user_egn,
            user_license_number,
            None,
        )

        errors = await self._validate_user_credentials(kat_client)

        if errors:
            return self.async_show_form(
                step_id="user", data_schema=SCHEMA_PERSON, errors=errors
            )

        # If this person (EGN) is already configured, abort
        await self.async_set_unique_id(user_egn)
        self._abort_if_unique_id_configured()

        return self.async_create_entry(title=f"KAT - {user_name}", data=user_input)

    async def async_step_business(self, user_input: dict[str, Any]) -> ConfigFlowResult:
        """Handle the initial step."""

        if len(user_input) == 1:
            return self.async_show_form(step_id="business", data_schema=SCHEMA_BUSINESS)

        # Init user input values & init KatClient
        # user_input[CONF_PERSON_TYPE] = PersonType.BUSINESS

        user_name = user_input[CONF_PERSON_NAME]
        user_egn = user_input[CONF_PERSON_EGN]
        user_gov_id_number = user_input[CONF_DOCUMENT_NUMBER]
        user_bulstat = user_input[CONF_BULSTAT]

        kat_client = KatClient(
            self.hass,
            PersonType.BUSINESS,
            user_name,
            user_egn,
            user_gov_id_number,
            user_bulstat,
        )

        errors = await self._validate_user_credentials(kat_client)

        if errors:
            return self.async_show_form(
                step_id="user", data_schema=SCHEMA_BUSINESS, errors=errors
            )

        # If this person (EGN) is already configured, abort
        await self.async_set_unique_id(user_bulstat)
        self._abort_if_unique_id_configured()

        return self.async_create_entry(title=f"KAT - {user_name}", data=user_input)

    async def async_step_reconfigure(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Handle a reconfiguration flow initialized by the user."""

        reconfigure_entry = self._get_reconfigure_entry()

        reconfigure_data_schema = vol.Schema(
            {
                vol.Required(
                    CONF_DOCUMENT_NUMBER,
                    default=reconfigure_entry.data.get(CONF_DOCUMENT_NUMBER, ""),
                ): str
            }
        )

        if not user_input:
            return self.async_show_form(
                step_id="reconfigure",
                data_schema=reconfigure_data_schema,
            )

        person_type = reconfigure_entry.data[CONF_PERSON_TYPE]
        new_document_number = user_input[CONF_DOCUMENT_NUMBER]

        match person_type:
            case PersonType.INDIVIDUAL:
                errors = await self._validate_user_credentials(
                    KatClient(
                        self.hass,
                        PersonType.INDIVIDUAL,
                        reconfigure_entry.data[CONF_PERSON_NAME],
                        reconfigure_entry.data[CONF_PERSON_EGN],
                        new_document_number,
                        None,
                    )
                )

                if errors:
                    return self.async_show_form(
                        step_id="reconfigure",
                        data_schema=reconfigure_data_schema,
                        errors=errors,
                    )

            case PersonType.BUSINESS:
                errors = await self._validate_user_credentials(
                    KatClient(
                        self.hass,
                        PersonType.BUSINESS,
                        reconfigure_entry.data[CONF_PERSON_NAME],
                        reconfigure_entry.data[CONF_PERSON_EGN],
                        new_document_number,
                        reconfigure_entry.data[CONF_BULSTAT],
                    )
                )

                if errors:
                    return self.async_show_form(
                        step_id="reconfigure",
                        data_schema=reconfigure_data_schema,
                        errors=errors,
                    )
            case _:
                return self.async_show_form(
                    step_id="reconfigure",
                    data_schema=None,
                    errors={"base": "invalid_type"},
                )

        return self.async_update_reload_and_abort(
            reconfigure_entry, data_updates={**user_input}
        )

    async def _validate_user_credentials(self, kat_client: KatClient) -> dict[str, str]:
        """Validate user credentials."""

        errors = {}

        # Verify user input
        try:
            await kat_client.validate_credentials()
        except KatError as err:
            if err.error_type in (
                KatErrorType.VALIDATION_EGN_INVALID,
                KatErrorType.VALIDATION_ID_DOCUMENT_INVALID,
                KatErrorType.VALIDATION_USER_NOT_FOUND_ONLINE,
            ):
                _LOGGER.warning(
                    "Invalid credentials, unable to setup: %s", err.error_type
                )
                errors["base"] = "invalid_config"

            if err.error_type in (
                KatErrorType.API_TIMEOUT,
                KatErrorType.API_ERROR_READING_DATA,
                KatErrorType.API_INVALID_SCHEMA,
                KatErrorType.API_TOO_MANY_REQUESTS,
                KatErrorType.API_UNKNOWN_ERROR,
            ):
                _LOGGER.warning("KAT API down, unable to setup: %s", err.error_type)
                errors["base"] = "cannot_connect"

        return errors
