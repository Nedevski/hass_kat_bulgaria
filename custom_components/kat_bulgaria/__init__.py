"""The KAT Bulgaria integration."""

from __future__ import annotations

from homeassistant.const import Platform
from homeassistant.core import HomeAssistant

from .const import CONF_DRIVING_LICENSE, CONF_PERSON_EGN, CONF_PERSON_NAME
from .coordinator import KatBulgariaConfigEntry, KatBulgariaUpdateCoordinator
from .kat_client import KatClient

PLATFORMS: list[Platform] = [
    Platform.BINARY_SENSOR,
    Platform.SENSOR,
]


async def async_setup_entry(hass: HomeAssistant, entry: KatBulgariaConfigEntry) -> bool:
    """Set up KAT Bulgaria from a config entry."""

    person_name: str = entry.data[CONF_PERSON_NAME]
    person_egn: str = entry.data[CONF_PERSON_EGN]
    license_number: str = entry.data[CONF_DRIVING_LICENSE]

    client = KatClient(person_name, person_egn, license_number)

    coordinator = KatBulgariaUpdateCoordinator(hass, entry, client)

    await coordinator.async_config_entry_first_refresh()

    entry.runtime_data = coordinator

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True


async def async_unload_entry(
    hass: HomeAssistant, entry: KatBulgariaConfigEntry
) -> bool:
    """Unload a config entry."""
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
