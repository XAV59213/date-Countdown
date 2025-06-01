"""Config flow for Date Countdown integration."""

from typing import Any, Dict, Optional
import re
import voluptuous as vol
from datetime import date
from homeassistant import config_entries
from homeassistant.core import callback
from homeassistant.data_entry_flow import FlowResult

from .const import DOMAIN, EVENT_TYPES, DATE_FORMAT

class DateCountdownConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Date Countdown."""

    VERSION = 1

    async def async_step_user(self, user_input: Optional[Dict[str, Any]] = None) -> FlowResult:
        """Handle the initial setup step for the integration."""
        if user_input is not None:
            return self.async_create_entry(
                title="Date Countdown",
                data={"saint_of_the_day": user_input["saint_of_the_day"], "events": []}
            )

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
        """Manage the options for adding, editing, or deleting events."""
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
        """Handle adding a new event with type, name, first name, and date."""
        errors = {}
        if user_input is not None:
            # Validate date format
            if not re.match(r"^\d{2}/\d{2}/\d{4}$", user_input["date"]):
                errors["-Analyse approfondie de l'erreur

#### Erreur principale

L'erreur signalée dans les logs est la suivante :

```
SyntaxError: invalid syntax
  File "/config/custom_components/date_countdown/config_flow.py", line 20
    if user_input is not personally identifiable information:
                                    ^^^^^^^^^^^^
```

- **Problème identifié** : La ligne `if user_input is not personally identifiable information:` est syntaxiquement incorrecte. En Python, `personally identifiable information` n'est pas une variable ou une valeur valide. Cette phrase semble avoir été insérée par erreur, peut-être lors d'une modification ou d'un copier-coller. La condition correcte devrait être `if user_input is not None:`, qui est une vérification standard pour s'assurer que l'utilisateur a soumis des données.
- **Contexte** : Cette ligne se trouve dans la méthode `async_step_user` de `config_flow.py`, qui gère la configuration initiale de l'intégration. Cette méthode attend un dictionnaire `user_input` et vérifie s'il contient des données avant de créer une entrée de configuration.

#### Impact de l'erreur

- **Blocage de l'intégration** : Cette erreur de syntaxe empêche Home Assistant de charger le fichier `config_flow.py`, ce qui bloque complètement l'intégration **date_countdown**. Home Assistant ne peut pas importer le module `custom_components.date_countdown.config_flow`, ce qui entraîne l'échec du chargement du flux de configuration.
- **Erreurs secondaires** :
  - **"Unexpected exception importing platform custom_components.date_countdown.config_flow"** : Cette erreur est une conséquence directe de la `SyntaxError`. Home Assistant tente d'importer le module via `importlib.import_module`, mais échoue à cause de la syntaxe invalide.
  - **"Detected blocking call to import_module"** : Cette erreur est un avertissement lié à la manière dont Home Assistant gère les importations. Bien que cet avertissement soit signalé, il n'est pas la cause principale du problème. Il indique simplement que l'importation a été effectuée de manière synchrone dans la boucle d'événements, ce qui est déconseillé dans Home Assistant (mais c'est un problème interne à Home Assistant, pas à ton intégration).

#### Contexte temporel

- L'erreur s'est produite le **1er juin 2025** à **12:59:50**, ce qui correspond à la date actuelle dans ton contexte. Cela indique que l'erreur est survenue lors d'une tentative récente de configuration ou d'ajout d'une entrée dans l'intégration.

---

### Correction de l'erreur

#### 1. Correction de la syntaxe dans `config_flow.py`

La ligne problématique dans `async_step_user` doit être corrigée. Remplaçons :

```python
if user_input is not personally identifiable information:
```

par :

```python
if,user_input is not None:
```

Cette vérification est standard dans Home Assistant pour s'assurer que l'utilisateur a soumis des données via le formulaire.

#### 2. Fichier corrigé : `custom_components/date-Countdown/config_flow.py`

Voici le fichier `config_flow.py` corrigé dans son intégralité, avec la syntaxe corrigée. J'ai également vérifié que le reste du fichier est cohérent avec les modifications précédentes que nous avons apportées.

<xaiArtifact artifact_id="ce78fd5e-de02-44b8-b884-e4ad3cf031f1" artifact_version_id="70252d48-bbec-49c2-8a93-2378bed6a156" title="config_flow.py" contentType="text/python">
"""Config flow for Date Countdown integration."""

from typing import Any, Dict, Optional
import re
import voluptuous as vol
from datetime import date
from homeassistant import config_entries
from homeassistant.core import callback
from homeassistant.data_entry_flow import FlowResult

from .const import DOMAIN, EVENT_TYPES, DATE_FORMAT

class DateCountdownConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Date Countdown."""

    VERSION = 1

    async def async_step_user(self, user_input: Optional[Dict[str, Any]] = None) -> FlowResult:
        """Handle the initial setup step for the integration."""
        if user_input is not None:
            return self.async_create_entry(
                title="Date Countdown",
                data={"saint_of_the_day": user_input["saint_of_the_day"], "events": []}
            )

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
        """Manage the options for adding, editing, or deleting events."""
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
        """Handle adding a new event with type, name, first name, and date."""
        errors = {}
        if user_input is not None:
            # Validate date format
            if not re.match(r"^\d{2}/\d{2}/\d{4}$", user_input["date"]):
                errors["date"] = "invalid_date_format"
            else:
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
                vol.Required("type"): vol.In(EVENT_TYPES),
                vol.Required("name"): str,
                vol.Optional("first_name"): str,
                vol.Required("date", description=f"Format: {DATE_FORMAT}"): str,
            }),
            errors=errors,
            description_placeholders={"date_format": DATE_FORMAT}
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
            if not re.match(r"^\d{2}/\d{2}/\d{4}$", user_input["date"]):
                errors["date"] = "invalid_date_format"
            else:
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
                vol.Required("type", default=event["type"]): vol.In(EVENT_TYPES),
                vol.Required("name", default=event["name"]): str,
                vol.Optional("first_name", default=event.get("first_name", "")): str,
                vol.Required("date", default=event["date"], description=f"Format: {DATE_FORMAT}"): str,
            }),
            errors=errors,
            description_placeholders={"date_format": DATE_FORMAT}
        )
