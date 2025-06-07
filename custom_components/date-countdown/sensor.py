"""Sensor platform for Date Countdown."""
import logging
from datetime import date
from typing import Any, Dict, Optional

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.util import dt as dt_util

from .const import DOMAIN, EVENT_TYPES, WEDDING_ANNIVERSARIES

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities) -> None:
    """Set up Date Countdown sensors from a config entry."""
    sensors = []

    # Ensure hass.data[DOMAIN] is initialized
    if DOMAIN not in hass.data:
        hass.data[DOMAIN] = {}

    # Add event sensors
    events = entry.options.get("events", [])
    if not events:
        _LOGGER.warning("No events configured for Date Countdown integration. No event sensors will be created.")
    for event in events:
        # Validate event data
        if not all(key in event for key in ["name", "date", "type"]):
            _LOGGER.error("Invalid event configuration, missing required fields: %s", event)
            continue
        if event["type"] not in EVENT_TYPES:
            _LOGGER.error("Invalid event type '%s' for event: %s", event["type"], event)
            continue

        try:
            # Validate date format (DD/MM/YYYY)
            day, month, year = map(int, event["date"].split('/'))
            date(year, month, day)  # This will raise ValueError if the date is invalid
        except (ValueError, TypeError) as e:
            _LOGGER.error("Invalid date format for event %s: %s. Expected DD/MM/YYYY.", event, e)
            continue

        event_sensor = DateCountdownSensor(
            event["name"],
            event.get("first_name", ""),
            event["type"],
            event["date"]
        )
        sensors.append(event_sensor)
        _LOGGER.info("Created DateCountdownSensor with unique_id: %s, name: %s", event_sensor.unique_id, event_sensor.name)

    if not sensors:
        _LOGGER.warning("No sensors were created for Date Countdown integration. Check configuration and events.")
    else:
        hass.data[DOMAIN][entry.entry_id] = {"sensors": sensors}
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
        _LOGGER.debug("Initialized DateCountdownSensor: unique_id=%s, name=%s, date=%s", self._attr_unique_id, self._attr_name, self._event_date)

    def _get_friendly_name(self) -> str:
        """Return the friendly name in the format 'Name - Event Type'."""
        prefix = f"{self._first_name} {self._name}".strip() if self._first_name else self._name
        # Define translated event types
        event_type_labels = {
            "birthday": "Anniversaire",
            "anniversary": "Anniversaire de mariage",
            "memorial": "Mémorial",
            "promotion": "Promotion",
            "special_event": "Événement spécial"
        }
        event_type_name = event_type_labels.get(self._event_type, self._event_type)
        friendly_name = f"{prefix} - {event_type_name}"
        _LOGGER.debug("Generated friendly name for sensor %s: %s", self._attr_unique_id, friendly_name)
        return friendly_name

    @property
    def state(self) -> Optional[int]:
        """Return the state of the sensor (days until event)."""
        return self._state

    @property
    def extra_state_attributes(self) -> Dict[str, Any]:
        """Return the state attributes."""
        attributes = {
            "event_date": self._event_date,
            "event_type": self._event_type,
            "first_name": self._first_name,
            "friendly_name": self._attr_name
        }
        if self._years is not None:
            attributes["years"] = self._years
        if self._event_type == "anniversary" and self._wedding_type is not None:
            attributes["wedding_type"] = self._wedding_type
        _LOGGER.debug("Returning attributes for sensor %s: %s", self._attr_unique_id, attributes)
        return attributes

    async def async_update(self) -> None:
        """Update the sensor."""
        try:
            # Parse and validate date
            day, month, year = map(int, self._event_date.split('/'))
            date(year, month, day)
        except (ValueError, TypeError) as e:
            _LOGGER.error("Failed to parse event date %s for sensor %s: %s", self._event_date, self._attr_unique_id, e)
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
        _LOGGER.debug("Updated sensor %s: %s days until %s", self._attr_unique_id, self._state, next_event)

        # Calculate years
        self._years = next_event.year - year

        # Set wedding type for anniversaries
        if self._event_type == "anniversary" and self._years in WEDDING_ANNIVERSARIES:
            self._wedding_type = WEDDING_ANNIVERSARIES[self._years]
        else:
            self._wedding_type = None
