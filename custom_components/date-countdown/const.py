"""Constants for Date Countdown integration."""

import logging

_LOGGER = logging.getLogger(__name__)

DOMAIN = "date_countdown"
PLATFORMS = ["sensor"]
DATE_FORMAT = "DD/MM/YYYY"
EVENT_TYPES = ["birthday", "anniversary", "memorial", "promotion", "special_event"]

WEDDING_ANNIVERSARIES = {
    1: "Noces de Coton",
    2: "Noces de Cuir",
    3: "Noces de Froment",
    4: "Noces de Cire",
    5: "Noces de Bois",
    6: "Noces de Chypre",
    7: "Noces de Laine",
    8: "Noces de Coquelicot",
    9: "Noces de Faïence",
    10: "Noces d'Étain",
    11: "Noces de Corail",
    12: "Noces de Soie",
    13: "Noces de Muguet",
    14: "Noces de Plomb",
    15: "Noces de Cristal",
    16: "Noces de Saphir",
    17: "Noces de Rose",
    18: "Noces de Turquoise",
    19: "Noces de Cretonne",
    20: "Noces de Porcelaine",
    21: "Noces d'Opale",
    22: "Noces de Bronze",
    23: "Noces de Béryl",
    24: "Noces de Satin",
    25: "Noces d'Argent",
    26: "Noces de Jade",
    27: "Noces d'Acajou",
    28: "Noces de Nickel",
    29: "Noces de Velours",
    30: "Noces de Perle",
    31: "Noces de Basane",
    32: "Noces de Cuivre",
    33: "Noces de Porphyre",
    34: "Noces d'Ambre",
    35: "Noces de Rubis",
    36: "Noces de Mousseline",
    37: "Noces de Papier",
    38: "Noces de Mercure",
    39: "Noces de Crêpe",
    40: "Noces d'Émeraude",
    41: "Noces de Fer",
    42: "Noces de Nacre",
    43: "Noces de Flanelle",
    44: "Noces de Topaze",
    45: "Noces de Vermeil",
    46: "Noces de Lavande",
    47: "Noces de Cachemire",
    48: "Noces d'Améthyste",
    49: "Noces de Cèdre",
    50: "Noces d'Or",
    51: "Noces de Camélia",
    52: "Noces de Tourmaline",
    53: "Noces de Merisier",
    54: "Noces de Zibeline",
    55: "Noces d'Orchidée",
    56: "Noces de Lapis-Lazuli",
    57: "Noces d'Azurite",
    58: "Noces d'Érable",
    59: "Noces de Vison",
    60: "Noces de Diamant"
}
