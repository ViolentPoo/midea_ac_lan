from __future__ import annotations

from homeassistant.components.select import SelectEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .entity import MideaEntity
from .const import DOMAIN
from midea_ac_lan.codes import ACAttributes


FAN_LOW = 20
FAN_HIGH = 60


FAN_MAP = {
    "Low": FAN_LOW,
    "High": FAN_HIGH,
}

REVERSE_MAP = {
    FAN_LOW: "Low",
    FAN_HIGH: "High",
}


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:

    device = hass.data[DOMAIN][entry.entry_id]

    async_add_entities([
        MideaFanSpeedSelect(device, entry)
    ])


class MideaFanSpeedSelect(MideaEntity, SelectEntity):
    """Fan speed selector for Midea dehumidifiers."""

    _attr_name = "Fan Speed"
    _attr_icon = "mdi:fan"

    @property
    def options(self):
        return ["Low", "High"]

    @property
    def current_option(self):
        raw = self._device.get_attribute(ACAttributes.fan_speed)

        if raw is None:
            return "Low"

        # Normalize closest match
        if raw >= 50:
            return "High"
        return "Low"

    def select_option(self, option: str) -> None:
        value = FAN_MAP.get(option, FAN_LOW)

        self._device.set_attribute(
            attr=ACAttributes.fan_speed,
            value=value,
        )

        self.async_write_ha_state()
