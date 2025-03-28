"""Tests for KAT Bulgaria."""

from homeassistant.components.kat_bulgaria.const import (
    CONF_DRIVING_LICENSE,
    CONF_PERSON_EGN,
    CONF_PERSON_NAME,
)

EGN_VALID = "0011223344"
LICENSE_VALID = "123456789"

EGN_INVALID = "9988776655"
LICENSE_INVALID = "123"

MOCK_NAME = "KAT - test"
MOCK_DATA = {
    CONF_PERSON_NAME: "test",
    CONF_PERSON_EGN: EGN_VALID,
    CONF_DRIVING_LICENSE: LICENSE_VALID,
}
