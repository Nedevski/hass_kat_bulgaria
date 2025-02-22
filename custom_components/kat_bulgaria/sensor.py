"""Support for KAT Bulgaria sensors."""

from kat_bulgaria.obligations import KatObligation

from homeassistant.components.sensor import SensorEntity
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback

from .coordinator import KatBulgariaConfigEntry, KatBulgariaUpdateCoordinator
from .entity import KatBulgariaEntity


async def async_setup_entry(
    hass: HomeAssistant,
    entry: KatBulgariaConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Set up KAT Bulgaria sensors based on a config entry."""

    coordinator = entry.runtime_data

    async_add_entities([KatBulgariaTicketCountSensor(coordinator)])


class KatBulgariaTicketCountSensor(KatBulgariaEntity, SensorEntity):
    """Defines a Total Ticket Count sensor."""

    _attr_name = "Ticket Count"
    _attr_unique_id = "ticket_count"
    _attr_icon = "mdi:cash-multiple"
    # _attr_icon = "mdi:cash-fast"
    # _attr_unit_of_measurement = "BGN"

    _obligations: list[KatObligation]

    def __init__(self, coordinator: KatBulgariaUpdateCoordinator) -> None:
        """Initialize the sensor."""

        super().__init__(coordinator)
        self._attr_entity_registry_enabled_default = True

        self._obligations = coordinator.data["obligations"]

    @property
    def native_value(self) -> int:
        """Return the state of the entity."""
        return len(self._obligations)

    @property
    def extra_state_attributes(self) -> dict[str, str]:
        """Return the extra state attributes."""
        return {
            "total_amount": str(
                sum([obligation.amount for obligation in self._obligations])
            )
        }
