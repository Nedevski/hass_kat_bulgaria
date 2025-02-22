"""Base class for KAТ Bulgaria entities."""

from kat_bulgaria.obligations import KatObligation

from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .coordinator import KatBulgariaUpdateCoordinator


class KatBulgariaEntity(CoordinatorEntity[KatBulgariaUpdateCoordinator]):
    """Defines a base AirGradient entity."""

    _attr_has_entity_name = True

    obligations: list[KatObligation]

    def __init__(self, coordinator: KatBulgariaUpdateCoordinator) -> None:
        """Initialize airgradient entity."""

        super().__init__(coordinator)
        self.obligations = coordinator.data["obligations"]
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, coordinator.serial_number)},
            manufacturer="KAT Bulgaria",
            serial_number=coordinator.client.person_egn,
        )
