"""KAT Bulgaria Client Wrapper."""

from kat_bulgaria.data_models import KatObligation
from kat_bulgaria.kat_api_client import KatApiClient

from homeassistant.core import HomeAssistant

from .const import PersonType


class KatClient:
    """KAT Client Manager."""

    api: KatApiClient
    hass: HomeAssistant

    person_type: str
    person_egn: str
    person_document_number: str
    bulstat: str | None

    def __init__(
        self,
        hass: HomeAssistant,
        person_type: str,
        egn: str,
        document_number: str,
        bulstat: str | None,
    ) -> None:
        """Initialize client."""
        super().__init__()

        self.hass = hass
        self.api = KatApiClient()

        self.person_type = person_type
        self.person_egn = egn
        self.person_document_number = document_number
        self.bulstat = None

        if self.person_type == PersonType.BUSINESS:
            if bulstat is None:
                raise ValueError("Bulstat is required for business type")

            self.bulstat = bulstat

    async def validate_credentials(self) -> bool:
        """Validate EGN/License Number."""
        if self.person_type == PersonType.BUSINESS:
            return await self.api.validate_credentials_business(
                self.person_egn, self.person_document_number, self.bulstat
            )

        return await self.api.validate_credentials_individual(
            self.person_egn, self.person_document_number
        )

    async def get_obligations(self) -> list[KatObligation]:
        """Get obligations."""
        if self.person_type == PersonType.BUSINESS:
            return await self.api.get_obligations_business(
                self.person_egn, self.person_document_number, self.bulstat
            )

        return await self.api.get_obligations_individual(
            self.person_egn, self.person_document_number
        )
