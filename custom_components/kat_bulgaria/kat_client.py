"""KAT Bulgaria Client Wrapper."""

from kat_bulgaria.kat_api_client import KatApiClient

from homeassistant.core import HomeAssistant
from homeassistant.helpers.httpx_client import get_async_client


class KatClient:
    """KAT Client Manager."""

    person_name: str
    person_egn: str
    person_license_number: str

    api: KatApiClient
    hass: HomeAssistant

    def __init__(
        self, hass: HomeAssistant, name: str, egn: str, license_number: str
    ) -> None:
        """Initialize client."""
        super().__init__()

        self.person_name = name
        self.person_egn = egn
        self.person_license_number = license_number

        self.api = KatApiClient()
        self.hass = hass

    async def validate_credentials(self):
        """Validate EGN/License Number."""
        async with get_async_client(self.hass) as client:
            return await self.api.validate_credentials(
                self.person_egn, self.person_license_number, client
            )

    async def get_obligations(self):
        """Get obligations."""
        async with get_async_client(self.hass) as client:
            return await self.api.get_obligations(
                self.person_egn, self.person_license_number, client
            )
