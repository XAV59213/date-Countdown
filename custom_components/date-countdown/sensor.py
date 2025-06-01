"""Sensor platform for Date Countdown."""

import logging
from datetime import date
from typing import Any, Dict, Optional

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.util import dt as dt_util

from .const import DOMAIN, EVENT_TYPES, WEDDING_ANNIVERSARIES, SAINTS_BY_DATE

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities) -> None:
    """Set up Date Countdown sensors from a config entry."""
    sensors = []

    # Add event sensors
    for event in entry.options.get("events", []):
        sensors.append(DateCountdownSensor(
            event["name"],
            event.get("first_name", ""),
            event["type"],
            event["date"]
        ))

    # Always add saint of the day sensor
    saint_sensor = SaintOfTheDaySensor()
    sensors.append(saint_sensor)
    _LOGGER.info("Created SaintOfTheDaySensor with unique_id: %s", saint_sensor.unique_id)

    hass.data[DOMAIN][entry.entry_id] = sensors
    async_add_entities(sensors)

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    hass.data[DOMAIN].pop(entry.entry_id, None)
    return True

class DateCountdownSensor(SensorEntity):
    """Representation of a Date Countdown sensor."""

    def __init__(self, name: str, first_name: str, event_type: str, event_date: str) -> None:
        """Initialize the sensor."""
        self._name = name
        self._first_name = first_name
        self._event_type = event_type
        self._event_date = event_date
        self._state = None
        self._years = None
        self._wedding_type = None
        self._attr_unique_id = f"{event_type}_{name.lower().replace(' ', '_')}_{event_date.replace('/', '')}"
        self._attr_name = self._get_friendly_name()
        self._attr_unit_of_measurement = "days"
        self._attr_icon = {
            "birthday": "mdi:cake",
            "anniversary": "mdi:ring",
            "memorial": "mdi:candle",
            "promotion": "mdi:briefcase",
            "special_event": "mdi:star"
        }.get(event_type, "mdi:calendar")

    def _get_friendly_name(self) -> str:
        """Return the friendly name based on event type."""
        prefix = f"{self._first_name} {self._name}".strip() if self._first_name else self._name
        if self._event_type == "birthday":
            return f"{prefix}'s birthday"
        elif self._event_type == "anniversary":
            return f"{prefix}'s anniversary"
        elif self._event_type == "memorial":
            return f"In memory of {prefix}"
        elif self._event_type == "promotion":
            return f"{prefix}'s promotion"
        elif self._event_type == "special_event":
            return f"{prefix}'s special event"
        return f"{prefix}'s {self._event_type}"

    @property
    def state(self) -> Optional[int]:
        """Return the state of the sensor (days until event)."""
        return self._state

    @property
    def extra_state_attributes(self) -> Dict[str, Any]:
        """Return the state attributes."""
        attributes = {
            "years": self._years,
            "friendly_name": self._attr_name,
            "event_type": self._event_type,
            "first_name": self._first_name
        }
        if self._event_type == "anniversary" and self._wedding_type:
            attributes["wedding_type"] = self._wedding_type
        return attributes

    async def async_update(self) -> None:
        """Update the sensor."""
        try:
            # Parse and validate date
            day, month, year = map(int, self._event_date.split('/'))
            date(year, month, day)
        except (ValueError, TypeError):
            self._state = None
            self._years = None
            self._wedding_type = None
            return

        today = dt_util.now().date()
        next_event = date(today.year, month, day)

        # If event already passed this year, use next year
        if next_event < today:
            next_event = date(today.year + 1, month, day)

        # Calculate days until event
        self._state = (next_event - today).days

        # Calculate years
        self._years = next_event.year - year

        # Set wedding type for anniversaries
        if self._event_type == "anniversary" and self._years in WEDDING_ANNIVERSARIES:
            self._wedding_type = WEDDING_ANNIVERSARIES[self._years]
        else:
            self._wedding_type = None

class SaintOfTheDaySensor(SensorEntity):
    """Representation of a Saint of the Day sensor."""

    def __init__(self) -> None:
        """Initialize the sensor."""
        self._state = None
        self._saint = None
        self._attr_unique_id = "saint_of_the_day"
        self._attr_name = "Saint du jour"
        self._attr_icon = "mdi:church"

    @property
    def state(self) -> Optional[str]:
        """Return the state of the sensor (saint name)."""
        return self._state

    @property
    def extra_state_attributes(self) -> Dict[str, Any]:
        """Return the state attributes."""
        return {
            "saint": self._saint,
            "friendly_name": self._attr_name
        }

    async def async_update(self) -> None:
        """Update the sensor with saint for the current date."""
        today = dt_util.now().date()
        date_key = f"{today.day:02d}:{today.month:02d}"

        # Get saint from the list
        self._saint = SAINTS_BY_DATE.get(date_key, "Aucun saint aujourd'hui")
        self._state = self._saint
