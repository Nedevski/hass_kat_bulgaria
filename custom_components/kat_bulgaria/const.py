"""Constants for the KAT Bulgaria integration."""

from datetime import timedelta

DOMAIN = "kat_bulgaria"

CONF_PERSON_TYPE = "person_type"

# Old
CONF_DRIVING_LICENSE = "driving_license_number"

CONF_PERSON_NAME = "person_name"
CONF_PERSON_EGN = "egn"
CONF_DOCUMENT_NUMBER = "document_number"

CONF_BULSTAT = "business_bulstat"

COORD_DATA_KEY = "obligations"

DEFAULT_POLL_INTERVAL = timedelta(minutes=30)


class PersonType:
    """Person Type."""

    INDIVIDUAL = "individual"
    BUSINESS = "business"
