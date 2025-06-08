"""Sensor platform for Date Countdown."""
import logging
from datetime import date, datetime
from typing import Any, Dict, Optional

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.util import dt as dt_util

from .const import DOMAIN, EVENT_TYPES, WEDDING_ANNIVERSARIES, AGE_CATEGORIES, AGE_CATEGORY_ICONS, WORK_MEDAL_LEVELS, WORK_MEDAL_PENIBLE_LEVELS

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities) -> None:
    """Set up Date Countdown sensors from a config entry."""
    sensors = []

    if DOMAIN not in hass.data:
        hass.data[DOMAIN] = {}

    events = entry.options.get("events", [])
    if not events:
        _LOGGER.warning("No events configured for Date Countdown integration. No event sensors will be created.")
    for event in events:
        if not all(key in event for key in ["name", "type"]):
            _LOGGER.error("Invalid event configuration, missing required fields: %s", event)
            continue
        if event["type"] not in EVENT_TYPES:
            _LOGGER.error("Invalid event type '%s' for event: %s", event["type"], event)
            continue

        if event["type"] == "retirement":
            required_key = "start_date"
        else:
            required_key = "date"

        if required_key not in event:
            _LOGGER.error("Missing required field '%s' for event: %s", required_key, event)
            continue

        try:
            day, month, year = map(int, event[required_key].split('/'))
            date(year, month, day)
            if event.get("birth_date"):
                day, month, year = map(int, event["birth_date"].split('/'))
                date(year, month, day)
            if event.get("death_date"):
                day, month, year = map(int, event["death_date"].split('/'))
                date(year, month, day)
        except (ValueError, TypeError) as e:
            _LOGGER.error("Invalid date format for event %s: %s. Expected DD/MM/YYYY.", event, e)
            continue

        event_sensor = DateCountdownSensor(
            event["name"],
            event.get("first_name", ""),
            event["type"],
            event.get("date"),
            event.get("death_date"),
            event.get("start_date"),
            event.get("birth_date"),
            event.get("is_penible", False)
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

    def __init__(
        self,
        name: str,
        first_name: str,
        event_type: str,
        event_date: Optional[str] = None,
        death_date: Optional[str] = None,
        start_date: Optional[str] = None,
        birth_date: Optional[str] = None,
        is_penible: bool = False
    ) -> None:
        """Initialize the sensor."""
        self._name = name
        self._first_name = first_name
        self._event_type = event_type
        self._event_date = event_date
        self._death_date = death_date
        self._start_date = start_date
        self._birth_date = birth_date
        self._is_penible = is_penible
        self._state = None
        self._years = None
        self._wedding_type = None
        self._age_if_alive = None
        self._years_since_death = None
        self._age_category = None
        self._years_remaining = None
        self._years_worked = None
        self._work_medal = None
        unique_id_base = f"{event_type}_{name.lower().replace(' ', '_')}"
        unique_id_date = (start_date or event_date or "").replace('/', '')
        self._attr_unique_id = f"{unique_id_base}_{unique_id_date}"
        self._attr_name = self._get_friendly_name()
        self._attr_unit_of_measurement = "days"
        self._attr_icon = {
            "birthday": "mdi:cake",
            "anniversary": "mdi:ring",
            "memorial": "mdi:candle",
            "promotion": "mdi:briefcase",
            "special_event": "mdi:star",
            "retirement": "mdi:beach"
        }.get(event_type, "mdi:calendar")
        _LOGGER.debug("Initialized DateCountdownSensor: unique_id=%s, name=%s, date=%s, start_date=%s, birth_date=%s, is_penible=%s", 
                      self._attr_unique_id, self._attr_name, self._event_date, self._start_date, self._birth_date, self._is_penible)

    def _get_friendly_name(self) -> str:
        """Return the friendly name in the format 'Name - Event Type'."""
        prefix = f"{self._first_name} {self._name}".strip() if self._first_name else self._name
        event_type_labels = {
            "birthday": "Anniversaire",
            "anniversary": "Anniversaire de mariage",
            "memorial": "Mémorial",
            "promotion": "Promotion",
            "special_event": "Événement spécial",
            "retirement": "Retraite"
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
        if self._event_type == "retirement":
            attributes["start_date"] = self._start_date
            attributes["birth_date"] = self._birth_date
            attributes["is_penible"] = self._is_penible
            if self._years_worked is not None:
                attributes["years_worked"] = self._years_worked
            if self._years_remaining is not None:
                attributes["years_remaining"] = self._years_remaining
            if self._work_medal:
                attributes["work_medal"] = self._work_medal
        else:
            if self._years is not None:
                attributes["years"] = self._years
            if self._event_type == "birthday" and self._age_category:
                attributes["age_category"] = self._age_category
            if self._event_type == "anniversary" and self._wedding_type:
                attributes["wedding_type"] = self._wedding_type
            if self._event_type == "memorial":
                if self._death_date:
                    attributes["death_date"] = self._death_date
                if self._age_if_alive is not None:
                    attributes["age_if_alive"] = self._age_if_alive
                if self._years_since_death is not None:
                    attributes["years_since_death"] = self._years_since_death
        _LOGGER.debug("Returning attributes for sensor %s: %s", self._attr_unique_id, attributes)
        return attributes

    async def async_update(self) -> None:
        """Update the sensor."""
        today = dt_util.now().date()

        if self._event_type == "retirement":
            try:
                day, month, year = map(int, self._start_date.split('/'))
                start_date = date(year, month, day)
            except (ValueError, TypeError) as e:
                _LOGGER.error("Failed to parse start date %s for sensor %s: %s", self._start_date, self._attr_unique_id, e)
                self._state = None
                self._years_worked = None
                self._years_remaining = None
                self._work_medal = None
                return

            # Calculer les années travaillées
            self._years_worked = today.year - start_date.year
            if (today.month, today.day) < (start_date.month, start_date.day):
                self._years_worked -= 1

            # Calculer la date de retraite
            retirement_age = 64  # Âge par défaut si pas de date de naissance
            if self._birth_date:
                try:
                    day, month, year = map(int, self._birth_date.split('/'))
                    birth_date = date(year, month, day)
                    birth_year = birth_date.year
                    if birth_year < 1961:
                        retirement_age = 62
                    elif birth_year >= 1968:
                        retirement_age = 64
                    else:
                        # Interpolation linéaire entre 62 et 64 ans
                        retirement_age = 62 + (birth_year - 1961) * (64 - 62) / (1968 - 1961)
                except (ValueError, TypeError) as e:
                    _LOGGER.error("Failed to parse birth date %s for sensor %s: %s", self._birth_date, self._attr_unique_id, e)

            if self._birth_date:
                try:
                    birth_date = date(*map(int, self._birth_date.split('/')))
                    retirement_year = birth_date.year + int(retirement_age)
                    retirement_date = date(retirement_year, birth_date.month, birth_date.day)
                    if retirement_date < today:
                        retirement_date = date(today.year + 1, birth_date.month, birth_date.day)
                except (ValueError, TypeError) as e:
                    _LOGGER.error("Failed to calculate retirement date for sensor %s: %s", self._attr_unique_id, e)
                    retirement_date = date(today.year + 1, start_date.month, start_date.day)
            else:
                retirement_date = date(today.year + 10, start_date.month, start_date.day)  # Estimation arbitraire si pas de birth_date

            self._state = (retirement_date - today).days
            self._years_remaining = retirement_date.year - today.year
            if (today.month, today.day) > (retirement_date.month, retirement_date.day):
                self._years_remaining -= 1

            # Déterminer la médaille du travail
            medal_levels = WORK_MEDAL_PENIBLE_LEVELS if self._is_penible else WORK_MEDAL_LEVELS
            self._work_medal = None
            for years_required, level in sorted(medal_levels.items(), reverse=True):
                if self._years_worked >= years_required:
                    self._work_medal = level
                    break

        else:
            try:
                day, month, year = map(int, self._event_date.split('/'))
                event_date = date(year, month, day)
            except (ValueError, TypeError) as e:
                _LOGGER.error("Failed to parse event date %s for sensor %s: %s", self._event_date, self._attr_unique_id, e)
                self._state = None
                self._years = None
                self._wedding_type = None
                self._age_if_alive = None
                self._years_since_death = None
                self._age_category = None
                return

            next_event = date(today.year, event_date.month, event_date.day)
            if next_event < today:
                next_event = date(today.year + 1, event_date.month, event_date.day)

            self._state = (next_event - today).days
            self._years = next_event.year - event_date.year

            if self._event_type == "anniversary" and self._years in WEDDING_ANNIVERSARIES:
                self._wedding_type = WEDDING_ANNIVERSARIES[self._years]
            else:
                self._wedding_type = None

            if self._event_type == "memorial":
                self._age_if_alive = today.year - event_date.year
                if (today.month, today.day) < (event_date.month, event_date.day):
                    self._age_if_alive -= 1
                if self._death_date:
                    try:
                        day, month, year = map(int, self._death_date.split('/'))
                        death_date = date(year, month, year)
                        self._years_since_death = today.year - death_date.year
                        if (today.month, today.day) < (death_date.month, death_date.day):
                            self._years_since_death -= 1
                    except (ValueError, TypeError) as e:
                        _LOGGER.error("Failed to parse death date %s for sensor %s: %s", self._death_date, self._attr_unique_id, e)
                        self._years_since_death = None
                else:
                    self._years_since_death = None
            else:
                self._age_if_alive = None
                self._years_since_death = None

            if self._event_type == "birthday":
                self._age_category = None
                for (min_age, max_age), category in AGE_CATEGORIES.items():
                    if min_age <= self._years <= max_age:
                        self._age_category = category
                        self._attr_icon = AGE_CATEGORY_ICONS.get(category, "mdi:cake")
                        break
