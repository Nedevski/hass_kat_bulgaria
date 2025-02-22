"""Support for KAT Bulgaria sensors."""

from kat_bulgaria.obligations import KatObligation

from homeassistant.components.sensor import SensorEntity
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback

from .const import COORD_DATA_KEY
from .coordinator import KatBulgariaConfigEntry, KatBulgariaUpdateCoordinator
from .entity import KatBulgariaEntity


async def async_setup_entry(
    hass: HomeAssistant,
    entry: KatBulgariaConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Set up KAT Bulgaria sensors based on a config entry."""

    coordinator = entry.runtime_data

    async_add_entities(
        [
            KatBulgariaTotalTicketCountSensor(coordinator),
            KatBulgariaNotServedTicketCountSensor(coordinator),
            KatBulgariaTotalTicketAmountSensor(coordinator),
        ],
    )


class KatBulgariaTotalTicketCountSensor(KatBulgariaEntity, SensorEntity):
    """Defines a Total Ticket Count sensor."""

    _attr_name = "Count Total"
    _attr_unique_id = "total_ticket_count"

    _obligations: list[KatObligation]

    def __init__(self, coordinator: KatBulgariaUpdateCoordinator) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._obligations = coordinator.data[COORD_DATA_KEY]

    @property
    def native_value(self) -> int:
        """Return the state of the entity."""
        return len(self._obligations)

    @property
    def extra_state_attributes(self) -> dict[str, str]:
        """Return the extra state attributes."""
        return {
            "total_amount": str(
                sum([obligation.discount_amount for obligation in self._obligations])
            )
        }


class KatBulgariaNotServedTicketCountSensor(KatBulgariaEntity, SensorEntity):
    """Defines a Total Ticket Count sensor."""

    _attr_name = "Count Non-Served"
    _attr_unique_id = "non_served_ticket_count"
        
    _obligations: list[KatObligation]

    def __init__(self, coordinator: KatBulgariaUpdateCoordinator) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._obligations = coordinator.data[COORD_DATA_KEY]

    @property
    def native_value(self) -> int:
        """Return the state of the entity."""
        return sum([obligation.is_served for obligation in self._obligations])


class KatBulgariaTotalTicketAmountSensor(KatBulgariaEntity, SensorEntity):
    """Defines a Total Ticket Amount sensor."""

    _attr_name = "Total BGN Owed"
    _attr_unique_id = "total_ticket_amount_owed"

    _obligations: list[KatObligation]

    def __init__(self, coordinator: KatBulgariaUpdateCoordinator) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._obligations = coordinator.data[COORD_DATA_KEY]

    @property
    def native_value(self) -> int:
        """Return the state of the entity."""
        return sum([obligation.discount_amount for obligation in self._obligations])

    @property
    def icon(self) -> str | None:
        """Return the icon to use in the frontend."""
        return "mdi:cash-multiple" if self.native_value != 0 else "mdi:cash-off"
