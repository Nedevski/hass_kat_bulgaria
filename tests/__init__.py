"""Tests for KAT Bulgaria."""

from homeassistant.components.kat_bulgaria.const import (
    CONF_BULSTAT,
    CONF_DOCUMENT_NUMBER,
    CONF_DRIVING_LICENSE,
    CONF_PERSON_EGN,
    CONF_PERSON_NAME,
    CONF_PERSON_TYPE,
    PersonType,
)

EGN_VALID = "0011223344"
LICENSE_VALID = "123456789"
BULSTAT_VALID = "000000000"

EGN_INVALID = "9988776655"
LICENSE_INVALID = "123"
BULSTAT_INVALID = "321"

MOCK_NAME = "KAT - test"

MOCK_DATA_PERSON_TYPE_INDIVIDUAL = {CONF_PERSON_TYPE: PersonType.INDIVIDUAL}
MOCK_DATA_PERSON_TYPE_BUSINESS = {CONF_PERSON_TYPE: PersonType.BUSINESS}

MOCK_DATA_INDIVIDUAL = {
    CONF_PERSON_NAME: "test",
    CONF_PERSON_EGN: EGN_VALID,
    CONF_DOCUMENT_NUMBER: LICENSE_VALID,
}

MOCK_DATA_BUSINESS = {
    CONF_PERSON_NAME: "test",
    CONF_PERSON_EGN: EGN_VALID,
    CONF_DOCUMENT_NUMBER: LICENSE_VALID,
    CONF_BULSTAT: BULSTAT_VALID,
}

MOCK_DATA_V1 = {
    CONF_PERSON_NAME: "test",
    CONF_PERSON_EGN: EGN_VALID,
    CONF_DRIVING_LICENSE: LICENSE_VALID,
}

PATCH_VALIDATE_CREDS_INDIVIDUAL = (
    "kat_bulgaria.kat_api_client.KatApiClient.validate_credentials_individual"
)
PATCH_VALIDATE_CREDS_BUSINESS = (
    "kat_bulgaria.kat_api_client.KatApiClient.validate_credentials_business"
)
