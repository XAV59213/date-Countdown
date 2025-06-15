"""Calendar platform for Date Countdown."""
import logging
from datetime import date, datetime, timedelta, time, timezone
from typing import Optional, Callable

from homeassistant.components.calendar import CalendarEntity, CalendarEvent
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.util import dt as dt_util

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities: Callable) -> None:
    """Set up Date Countdown calendars from a config entry."""
    calendars = []
    events = entry.options.get("events", [])
    for event in events:
        name = event.get("name")
        first_name = event.get("first_name", "")
        event_type = event.get("type")
        event_date = event.get("date") or event.get("start_date")

        if not name or not event_type or not event_date:
            continue

        calendars.append(DateCountdownCalendar(
            name=name,
            first_name=first_name,
            event_type=event_type,
            event_date=event_date,
            entry_id=entry.entry_id
        ))

    if calendars:
        async_add_entities(calendars)
        _LOGGER.info("%d Date Countdown calendar(s) created", len(calendars))
    else:
        _LOGGER.warning("No valid events found to create calendars")

class DateCountdownCalendar(CalendarEntity):
    def __init__(self, name: str, first_name: str, event_type: str, event_date: str, entry_id: str):
        self._name = name
        self._first_name = first_name
        self._event_type = event_type
        self._event_date_str = event_date
        self._event_date = self._parse_date(event_date)
        self._attr_unique_id = f"{event_type}_{name.lower().replace(' ', '_')}_{event_date.replace('/', '')}"
        self._attr_name = f"{first_name} {name} - {event_type}".strip()
        self._entry_id = entry_id
        self._next_event: Optional[CalendarEvent] = None

    def _parse_date(self, date_str: str) -> Optional[date]:
        try:
            day, month, year = map(int, date_str.split("/"))
            return date(year, month, day)
        except Exception as e:
            _LOGGER.error("Invalid date format for %s: %s", self._name, e)
            return None

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, self._entry_id)},
            "name": "Date Countdown",
            "manufacturer": "XAV59213"
        }

    @property
    def event(self) -> Optional[CalendarEvent]:
        today = dt_util.now().date()
        if not self._event_date:
            return None

        # Prochain anniversaire de la date
        next_date = date(today.year, self._event_date.month, self._event_date.day)
        if next_date < today:
            next_date = date(today.year + 1, self._event_date.month, self._event_date.day)

        tzinfo = dt_util.DEFAULT_TIME_ZONE
        start = datetime.combine(next_date, time(0, 0), tzinfo=tzinfo)
        end = datetime.combine(next_date, time(23, 59), tzinfo=tzinfo)
        summary = f"{self._attr_name}"

        return CalendarEvent(start=start, end=end, summary=summary)

    async def async_get_events(self, hass: HomeAssistant, start_date: datetime, end_date: datetime):
        """Return calendar events in range."""
        if self.event and start_date <= self.event.start < end_date:
            return [self.event]
        return []

    async def async_update(self) -> None:
        self._next_event = self.event

