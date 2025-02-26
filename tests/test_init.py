"""Testing __init__.py"""

from unittest.mock import patch

from custom_components.kat_bulgaria.const import DOMAIN

from homeassistant.components.sensor import DOMAIN as SENSOR_DOMAIN
from homeassistant.components.weather import DOMAIN as WEATHER_DOMAIN
from homeassistant.config_entries import SOURCE_IMPORT, ConfigEntry, ConfigEntryState
from homeassistant.core import HomeAssistant
from homeassistant.setup import async_setup_component

from .const import TEST_PERSON_NAME, TEST_PERSON_EGN, TEST_CONFIG

async def async_init_integration(
    hass: HomeAssistant,
    config_entry: ConfigEntry | None = None,
) -> ConfigEntry:
    """Set up the Gismeteo integration in Home Assistant."""
    if config_entry is None:
        config_entry = ConfigEntry(
            domain=DOMAIN,
            title=TEST_PERSON_NAME,
            unique_id=TEST_PERSON_EGN,
            data=TEST_CONFIG
        )

    config_entry.add_to_hass(hass)

    await hass.config_entries.async_setup(config_entry.entry_id)
    await hass.async_block_till_done()

    return config_entry


async def test_async_setup(hass: HomeAssistant):
    """Test a successful setup component."""
    await async_setup_component(hass, DOMAIN, {})
    await hass.async_block_till_done()
    
    
async def test_async_setup_entry(hass: HomeAssistant):
    """Test a successful setup entry."""
    await async_init_integration(hass)

    state = hass.states.get(f"{SENSOR_DOMAIN}.kat_nikola_count_total")
    assert state is not None