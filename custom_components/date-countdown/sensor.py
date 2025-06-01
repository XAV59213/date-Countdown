"""Sensor platform for Date Countdown."""
import logging
from datetime import date
from typing import Any, Dict, Optional

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.util import dt as dt_util
from homeassistant.helpers.device_registry import DeviceEntryType, DeviceRegistry, async_get as async_get_device_registry
from homeassistant.helpers.entity_registry import async_get as async_get_entity_registry, RegistryEntry

from .const import DOMAIN, EVENT_TYPES, WEDDING_ANNIVERSARIES, SAINTS_BY_DATE, PUBLIC_HOLIDAYS_2025

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities) -> None:
    """Set up Date Countdown sensors from a config entry."""
    sensors = []

    # Ensure hass.data[DOMAIN] is initialized
    if DOMAIN not in hass.data:
        hass.data[DOMAIN] = {}

    # Get device and entity registries
    device_registry: DeviceRegistry = async_get_device_registry(hass)
    entity_registry = async_get_entity_registry(hass)

    # Add event sensors (these can be re-created as events change)
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

    # Create global static sensors (SaintOfTheDaySensor and PublicHolidaySensor) only if they don't exist
    # Check if SaintOfTheDaySensor already exists
    saint_entity: Optional[RegistryEntry] = entity_registry.async_get_entity_id(
        "sensor", DOMAIN, "global_saint_of_the_day"
    )
    if saint_entity is None:
        # Create a device for SaintOfTheDaySensor
        saint_device = device_registry.async_get_or_create(
            config_entry_id=entry.entry_id,
            identifiers={(DOMAIN, "saint_of_the_day_device")},
            name="Saint du Jour",
            manufacturer="@XAV59213",
            model="Date Countdown",
            entry_type=DeviceEntryType.SERVICE,
        )
        saint_sensor = SaintOfTheDaySensor(saint_device.id)
        sensors.append(saint_sensor)
        _LOGGER.info("Created global SaintOfTheDaySensor with unique_id: %s, device_id: %s", saint_sensor.unique_id, saint_device.id)
    else:
        _LOGGER.debug("SaintOfTheDaySensor with unique_id global_saint_of_the_day already exists")

    # Check if PublicHolidaySensor already exists
    holiday_entity: Optional[RegistryEntry] = entity_registry.async_get_entity_id(
        "sensor", DOMAIN, "global_public_holiday"
    )
    if holiday_entity is None:
        # Create a device for PublicHolidaySensor
        holiday_device = device_registry.async_get_or_create(
            config_entry_id=entry.entry_id,
            identifiers={(DOMAIN, "public_holiday_device")},
            name="Jour Férié",
            manufacturer="@XAV59213",
            model="Date Countdown",
            entry_type=DeviceEntryType.SERVICE,
        )
        holiday_sensor = PublicHolidaySensor(holiday_device.id)
        sensors.append(holiday_sensor)
        _LOGGER.info("Created global PublicHolidaySensor with unique_id: %s, device_id: %s", holiday_sensor.unique_id, holiday_device.id)
    else:
        _LOGGER.debug("PublicHolidaySensor with unique_id global_public_holiday already exists")

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
        self._is_public_holiday = None
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
        # Always include event_date, even if async_update fails
        attributes = {
            "event_date": self._event_date,  # Ensure event_date is always present
            "event_type": self._event_type,
            "first_name": self._first_name,
            "friendly_name": self._attr_name
        }
        # Add computed attributes if they are available
        if self._years is not None:
            attributes["years"] = self._years
        if self._is_public_holiday is not None:
            attributes["is_public_holiday"] = self._is_public_holiday
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
            self._is_public_holiday = None
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

        # Check if the event date is a public holiday
        date_key = f"{day:02d}:{month:02d}"
        self._is_public_holiday = PUBLIC_HOLIDAYS_2025.get(date_key)

class SaintOfTheDaySensor(SensorEntity):
    """Representation of a Saint of the Day sensor."""

    def __init__(self, device_id: str) -> None:
        """Initialize the sensor."""
        self._state = None
        self._saint = None
        self._attr_unique_id = "global_saint_of_the_day"
        self._attr_name = "Saint du jour"
        self._attr_icon = "mdi:church"
        self._attr_device_id = device_id

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
        _LOGGER.debug("Updating SaintOfTheDaySensor with date_key: %s", date_key)
        self._saint = SAINTS_BY_DATE.get(date_key, "Aucun saint aujourd'hui")
        self._state = self._saint

class PublicHolidaySensor(SensorEntity):
    """Representation of a Public Holiday sensor."""

    def __init__(self, device_id: str) -> None:
        """Initialize the sensor."""
        self._state = None
        self._next_holiday = None
        self._next_date = None
        self._attr_unique_id = "global_public_holiday"
        self._attr_name = "Jour férié"
        self._attr_icon = "mdi:calendar-star"
        self._attr_device_id = device_id

    @property
    def state(self) -> Optional[str]:
        """Return the state of the sensor."""
        return self._state

    @property
    def extra_state_attributes(self) -> Dict[str, Any]:
        """Return the state attributes."""
        return {
            "next_holiday": self._next_holiday,
            "next_date": self._next_date,
            "friendly_name": self._attr_name
        }

    async def async_update(self) -> None:
        """Update the sensor with holiday for the current date."""
        today = dt_util.now().date()
        date_key = f"{today.day:02d}:{today.month:02d}"
        _LOGGER.debug("Updating PublicHolidaySensor with date_key: %s", date_key)
        self._state = PUBLIC_HOLIDAYS_2025.get(date_key, "Aucun jour férié")

        # Find the next holiday
        current_year = today.year
        for day_month, name in sorted(PUBLIC_HOLIDAYS_2025.items(), key=lambda x: (x[0].split(":")[1], x[0].split(":")[0])):
            day, month = map(int, day_month.split(":"))
            try:
                holiday_date = date(current_year, month, day)
                if holiday_date >= today:
                    self._next_holiday = name
                    self._next_date = holiday_date.strftime("%d/%m/%Y")
                    return
            except ValueError:
                # Skip invalid dates (e.g., 29/02 in non-leap years)
                continue
        # If no holiday found this year, use the first one next year
        first_key = next(iter(PUBLIC_HOLIDAYS_2025))
        day, month = map(int, first_key.split(":"))
        self._next_holiday = PUBLIC_HOLIDAYS_2025[first_key]
        self._next_date = date(current_year + 1, month, day).strftime("%d/%m/%Y")
