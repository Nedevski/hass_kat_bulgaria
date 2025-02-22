"""DateUpdateCoordinator for Kat Bulgaria integration."""

from datetime import timedelta
import logging
from typing import Any

from kat_bulgaria.obligations import KatError

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import DOMAIN
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
        client: KatClient,
    ) -> None:
        """Initialize coordinator."""
        super().__init__(
            hass,
            logger=_LOGGER,
            config_entry=config_entry,
            name=f"KAT - {client.person_name}",
            update_interval=timedelta(minutes=1),
        )
        self.client = client
        assert self.config_entry.unique_id
        self.serial_number = self.config_entry.unique_id

    async def _async_update_data(self) -> dict[str, Any]:
        try:
            obligations = await self.client.get_obligations()

        except KatError as error:
            raise UpdateFailed(
                translation_domain=DOMAIN,
                translation_key="update_error",
                translation_placeholders={"error": str(error)},
            ) from error

        return {"obligations": obligations}
