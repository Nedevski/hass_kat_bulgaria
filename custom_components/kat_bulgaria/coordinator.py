"""DateUpdateCoordinator for Kat Bulgaria integration."""

from datetime import timedelta
import logging
from typing import Any

from kat_bulgaria.errors import KatError

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import (
    CONF_DRIVING_LICENSE,
    CONF_PERSON_EGN,
    CONF_PERSON_NAME,
    COORD_DATA_KEY,
    DOMAIN,
)
from .kat_client import KatClient

type KatBulgariaConfigEntry = ConfigEntry[KatBulgariaUpdateCoordinator]

_LOGGER = logging.getLogger(__name__)


class KatBulgariaUpdateCoordinator(DataUpdateCoordinator):
    """My custom coordinator."""

    config_entry: KatBulgariaConfigEntry
    client: KatClient

    def __init__(
        self,
        hass: HomeAssistant,
        config_entry: KatBulgariaConfigEntry,
    ) -> None:
        """Initialize coordinator."""

        person_name: str = config_entry.data[CONF_PERSON_NAME]
        person_egn: str = config_entry.data[CONF_PERSON_EGN]
        license_number: str = config_entry.data[CONF_DRIVING_LICENSE]

        super().__init__(
            hass,
            logger=_LOGGER,
            config_entry=config_entry,
            name=f"KAT - {person_name}",
            update_interval=timedelta(minutes=30),
        )

        assert self.config_entry.unique_id
        self.serial_number = self.config_entry.unique_id
        self.client = KatClient(hass, person_name, person_egn, license_number)

    async def _async_update_data(self) -> dict[str, Any]:
        try:
            obligations = await self.client.get_obligations()

        except KatError as error:
            raise UpdateFailed(
                translation_domain=DOMAIN,
                translation_key="update_error",
                translation_placeholders={"error": str(error)},
            ) from error

        return {COORD_DATA_KEY: obligations}
