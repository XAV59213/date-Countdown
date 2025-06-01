"""Config flow for Date Countdown integration.

This module handles the configuration flow for the Date Countdown integration,
allowing users to manage events (add, edit, delete) through the Home Assistant UI.
The 'Saint du jour' sensor is enabled by default and not configurable.
"""

import logging
from typing import Any, Dict, Optional
import re
import voluptuous as vol
from datetime import date
from homeassistant import config_entries
from homeassistant.core import callback
from homeassistant.data_entry_flow import FlowResult

from .const import DOMAIN, EVENT_TYPES, DATE_FORMAT

_LOGGER = logging.getLogger(__name__)

class DateCountdownConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Date Countdown."""

    VERSION = 1

    async def async_step_user(self, user_input: Optional[Dict[str, Any]] = None) -> FlowResult:
        """Handle the initial step."""
        _LOGGER.debug("Starting async_step_user with user_input: %s", user_input)
        if user_input is not None:
            _LOGGER.info("Creating entry with default configuration")
            return self.async_create_entry(
                title="Date Countdown",
                data={"events": []}  # No saint_of_the_day option, always enabled
            )

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({}),  # Empty schema, no user input required
            description_placeholders={"event_types": ", ".join(EVENT_TYPES)}
        )

    @staticmethod
    @callback
    def async_get_options_flow(config_entry: config_entries.ConfigEntry) -> config_entries.OptionsFlow:
        """Get the options flow for this handler."""
        _LOGGER.debug("Initializing options flow for config_entry: %s", config_entry.entry_id)
        return DateCountdownOptionsFlow(config_entry)

class DateCountdownOptionsFlow(config_entries.OptionsFlow):
    """Handle options flow for Date Countdown."""

    def __init__(self, config_entry: config_entries.ConfigEntry) -> None:
        """Initialize options flow."""
        _LOGGER.debug("Initializing DateCountdownOptionsFlow")
        self.events = None  # Initialize events later in async_step_init

    async def async_step_init(self, user_input: Optional[Dict[str, Any]] = None) -> FlowResult:
        """Manage the options."""
        _LOGGER.debug("async_step_init called with user_input: %s", user_input)
        # Initialize events from config_entry.options
        if self.events is None:
            self.events = self.config_entry.options.get("events", [])
            _LOGGER.debug("Initialized events: %s", self.events)

        if user_input is not None:
            action = user_input.get("action")
            if action not in ["add", "edit", "delete"]:
                _LOGGER.warning("Invalid action received: %s", action)
                return self.async_show_form(
                    step_id="init",
                    data_schema=vol.Schema({
                        vol.Required("action"): vol.In(["add", "edit", "delete"])
                    }),
                    errors={"action": "invalid_action"}
                )
            _LOGGER.info("Selected action: %s", action)
            if action == "add":
                return await self.async_step_add_event()
            elif action in ("edit", "delete"):
                return await self.async_step_select_event(user_input)

        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema({
                vol.Required("action"): vol.In(["add", "edit", "delete"])
            })
        )

    async def async_step_add_event(self, user_input: Optional[Dict[str, Any]] = None) -> FlowResult:
        """Handle adding a new event."""
        _LOGGER.debug("async_step_add_event called with user_input: %s", user_input)
        errors = {}
        if user_input is not None:
            # Validate date format
            if not re.match(r"^\d{2}/\d{2}/\d{4}$", user_input["date"]):
                errors["date"] = "invalid_date_format"
                _LOGGER.warning("Invalid date format: %s", user_input["date"])
            else:
                try:
                    day, month, year = map(int, user_input["date"].split('/'))
                    date(year, month, day)  # Validate date
                except (ValueError, TypeError) as e:
                    errors["date"] = "invalid_date_format"
                    _LOGGER.error("Date validation failed: %s", e)
                else:
                    _LOGGER.info("Adding event: %s", user_input)
                    self.events.append({
                        "name": user_input["name"],
                        "first_name": user_input.get("first_name", ""),
                        "date": user_input["date"],
                        "type": user_input["type"]
                    })
                    return self.async_create_entry(
                        title="",
                        data={"events": self.events}  # No saint_of_the_day option
                    )

        # Define translated labels for event types
        event_type_options = {
            "birthday": "Anniversaire",
            "anniversary": "Anniversaire de mariage",
            "memorial": "Mémorial",
            "promotion": "Promotion",
            "special_event": "Événement spécial"
        }

        return self.async_show_form(
            step_id="add_event",
            data_schema=vol.Schema({
                vol.Required("name", description="Nom de l'événement ou de la personne"): str,
                vol.Optional("first_name", description="Prénom (optionnel)"): str,
                vol.Required("date", description=f"Date (format: {DATE_FORMAT})"): str,
                vol.Required("type", description="Type d'événement"): vol.In(event_type_options),
            }),
            errors=errors,
            description_placeholders={"date_format": DATE_FORMAT}
        )

    async def async_step_select_event(self, user_input: Optional[Dict[str, Any]] = None) -> FlowResult:
        """Handle selecting an event to edit or delete."""
        _LOGGER.debug("async_step_select_event called with user_input: %s", user_input)
        if not self.events:
            _LOGGER.warning("No events available for selection")
            return self.async_show_form(
                step_id="init",
                data_schema=vol.Schema({
                    vol.Required("action"): vol.In(["add", "edit", "delete"])
                }),
                errors={"base": "no_events"}
            )

        if user_input is not None:
            if "event" not in user_input:
                _LOGGER.warning("No event selected in user_input")
                return self.async_show_form(
                    step_id="select_event",
                    data_schema=vol.Schema({
                        vol.Required("event"): vol.In({str(i): f"{e['name']} ({e['type']})" for i, e in enumerate(self.events)}),
                        vol.Required("action"): str
                    }),
                    errors={"event": "event_required"}
                )

            event_index = int(user_input["event"])
            _LOGGER.info("Selected event index: %s for action: %s", event_index, user_input["action"])
            if user_input["action"] == "edit":
                return await self.async_step_edit_event({"event_index": event_index})
            elif user_input["action"] == "delete":
                self.events.pop(event_index)
                _LOGGER.info("Deleted event at index: %s", event_index)
                return self.async_create_entry(
                    title="",
                    data={"events": self.events}  # No saint_of_the_day option
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
        _LOGGER.debug("async_step_edit_event called with user_input: %s", user_input)
        errors = {}
        event_index = user_input.get("event_index", 0)
        if user_input is not None and "name" in user_input:
            if not re.match(r"^\d{2}/\d{2}/\d{4}$", user_input["date"]):
                errors["date"] = "invalid_date_format"
                _LOGGER.warning("Invalid date format for edit: %s", user_input["date"])
            else:
                try:
                    day, month, year = map(int, user_input["date"].split('/'))
                    date(year, month, day)
                except (ValueError, TypeError) as e:
                    errors["date"] = "invalid_date_format"
                    _LOGGER.error("Date validation failed for edit: %s", e)
                else:
                    _LOGGER.info("Updating event at index %s: %s", event_index, user_input)
                    self.events[event_index] = {
                        "name": user_input["name"],
                        "first_name": user_input.get("first_name", ""),
                        "date": user_input["date"],
                        "type": user_input["type"]
                    }
                    return self.async_create_entry(
                        title="",
                        data={"events": self.events}  # No saint_of_the_day option
                    )

        event = self.events[event_index]
        # Define translated labels for event types
        event_type_options = {
            "birthday": "Anniversaire",
            "anniversary": "Anniversaire de mariage",
            "memorial": "Mémorial",
            "promotion": "Promotion",
            "special_event": "Événement spécial"
        }
        return self.async_show_form(
            step_id="edit_event",
            data_schema=vol.Schema({
                vol.Required("name", description="Nom de l'événement ou de la personne", default=event["name"]): str,
                vol.Optional("first_name", description="Prénom (optionnel)", default=event.get("first_name", "")): str,
                vol.Required("date", description=f"Date (format: {DATE_FORMAT})", default=event["date"]): str,
                vol.Required("type", description="Type d'événement", default=event["type"]): vol.In(event_type_options),
            }),
            errors=errors,
            description_placeholders={"date_format": DATE_FORMAT}
        )
