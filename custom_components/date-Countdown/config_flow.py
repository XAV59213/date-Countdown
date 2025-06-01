"""Config flow for Date Countdown integration."""

from typing import Any, Dict, Optional
import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import callback
from homeassistant.data_entry_flow import FlowResult

from .const import DOMAIN, EVENT_TYPES

class DateCountdownConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Date Countdown."""

    VERSION = 1

    async def async_step_user(self, user_input: Optional[Dict[str, Any]] = None) -> FlowResult:
        """Handle the initial step."""
        if user_input is not None:
            return self.async_create_entry(title="Date Countdown", data=user_input)

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Optional("saint_of_the_day", default=True): bool,
            }),
            description_placeholders={"event_types": ", ".join(EVENT_TYPES)}
        )

    @staticmethod
    @callback
    def async_get_options_flow(config_entry: config_entries.ConfigEntry) -> config_entries.OptionsFlow:
        """Get the options flow for this handler."""
        return DateCountdownOptionsFlow(config_entry)

class DateCountdownOptionsFlow(config_entries.OptionsFlow):
    """Handle options flow for Date Countdown."""

    def __init__(self, config_entry: config_entries.ConfigEntry) -> None:
        """Initialize options flow."""
        self.config_entry = config_entry
        self.events = self.config_entry.options.get("events", [])

    async def async_step_init(self, user_input: Optional[Dict[str, Any]] = None) -> FlowResult:
        """Manage the options."""
        if user_input is not None:
            if user_input.get("action") == "add":
                return await self.async_step_add_event()
            elif user_input.get("action") == "edit":
                return await self.async_step_select_event(user_input)
            elif user_input.get("action") == "delete":
                return await self.async_step_select_event(user_input)

        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema({
                vol.Required("action"): vol.In(["add", "edit", "delete"])
            })
        )

    async def async_step_add_event(self, user_input: Optional[Dict[str, Any]] = None) -> FlowResult:
        """Handle adding a new event."""
        errors = {}
        if user_input is not None:
            # Validate date format
            try:
                day, month, year = map(int, user_input["date"].split('/'))
                date(year, month, day)  # Validate date
            except (ValueError, TypeError):
                errors["date"] = "invalid_date_format"
            else:
                self.events.append({
                    "name": user_input["name"],
                    "first_name": user_input.get("first_name", ""),
                    "date": user_input["date"],
                    "type": user_input["type"]
                })
                return self.async_create_entry(
                    title="",
                    data={"saint_of_the_day": self.config_entry.options.get("saint_of_the_day", True), "events": self.events}
                )

        return self.async_show_form(
            step_id="add_event",
            data_schema=vol.Schema({
                vol.Required("name"): str,
                vol.Optional("first_name"): str,
                vol.Required("date"): str,
                vol.Required("type"): vol.In(EVENT_TYPES)
            }),
            errors=errors
        )

    async def async_step_select_event(self, user_input: Optional[Dict[str, Any]] = None) -> FlowResult:
        """Handle selecting an event to edit or delete."""
        if user_input is not None:
            event_index = int(user_input["event"])
            if user_input["action"] == "edit":
                return await self.async_step_edit_event({"event_index": event_index})
            elif user_input["action"] == "delete":
                self.events.pop(event_index)
                return self.async_create_entry(
                    title="",
                    data={"saint_of_the_day": self.config_entry.options.get("saint_of_the_day", True), "events": self.events}
                )

        event_options = {str(i): f"{e['name']} ({e['type']})" for i, e in enumerate(self.events)}
        return self.async_show_form(
            step_id="select_event",
            data_schema=vol.Schema({
                vol.Required("event"): vol.In(event_options),
                vol.Required("action"): str
            })
        )

    async def async_step_edit_event(self, user_input: Optional[Dict[str, Any]] = None) -> FlowResult:
        """Handle editing an event."""
        errors = {}
        event_index = user_input.get("event_index", 0)
        if user_input is not None and "name" in user_input:
            try:
                day, month, year = map(int, user_input["date"].split('/'))
                date(year, month, day)
            except (ValueError, TypeError):
                errors["date"] = "invalid_date_format"
            else:
                self.events[event_index] = {
                    "name": user_input["name"],
                    "first_name": user_input.get("first_name", ""),
                    "date": user_input["date"],
                    "type": user_input["type"]
                }
                return self.async_create_entry(
                    title="",
                    data={"saint_of_the_day": self.config_entry.options.get("saint_of_the_day", True), "events": self.events}
                )

        event = self.events[event_index]
        return self.async_show_form(
            step_id="edit_event",
            data_schema=vol.Schema({
                vol.Required("name", default=event["name"]): str,
                vol.Optional("first_name", default=event.get("first_name", "")): str,
                vol.Required("date", default=event["date"]): str,
                vol.Required("type", default=event["type"]): vol.In(EVENT_TYPES)
            }),
            errors=errors
        )
