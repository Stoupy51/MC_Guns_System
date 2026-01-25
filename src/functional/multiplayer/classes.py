
# Imports
from stewbeet import JsonDict

# Balanced team-vs-team class loadouts
# Format:
#   name, lore
#   main: {"gun": id, "mag": id, "mag_count": x}
#   secondary: {"gun": id, "mag": id, "mag_count": x}
#   melee: melee_id
#   equipment: dict of item_id -> count
#   special flags preserved where present
classes: JsonDict = {
    "assault": {
        "name": "Assault",
        "lore": "Versatile frontline",
        "main": {"gun": "ak47", "mag": "ak47_mag", "mag_count": 3},
        "secondary": {"gun": "m1911", "mag": "m1911_mag", "mag_count": 1},
        "melee": "knife",
        "equipment": {
            "frag_grenade": 2,
            "smoke_grenade": 1,
        },
    },

    "rifleman": {
        "name": "Rifleman",
        "lore": "Accurate mid-range",
        "main": {"gun": "m16a4", "mag": "m16a4_mag", "mag_count": 2},
        "secondary": {"gun": "glock17", "mag": "glock17_mag", "mag_count": 2},
        "melee": "knife",
        "equipment": {"flash_2": 1},
    },

    "support": {
        "name": "Support",
        "lore": "Suppressive heavy",
        "main": {"gun": "m249", "mag": "m249_mag", "mag_count": 3},
        "secondary": {"gun": "makarov", "mag": "makarov_mag", "mag_count": 2},
        "melee": "knife",
        "equipment": {"flash_4": 1},
        "special": {"resupply": True},
    },

    "sniper": {
        "name": "Sniper",
        "lore": "Long-range precision",
        "main": {"gun": "m24", "mag": "m24_mag", "mag_count": 2},
        "secondary": {"gun": "deagle", "mag": "deagle_mag", "mag_count": 2},
        "melee": "knife",
        "equipment": {"flash_1": 1},
        "special": {"bipod": True},
    },

    "smg": {
        "name": "SMG",
        "lore": "Close quarters",
        "main": {"gun": "mp5", "mag": "mp5_mag", "mag_count": 3},
        "secondary": {"gun": "glock18", "mag": "glock18_mag", "mag_count": 2},
        "melee": "knife",
        "equipment": {"flash_5": 1},
    },

    "shotgunner": {
        "name": "Shotgunner",
        "lore": "Breaching / CQB",
        "main": {"gun": "m590", "mag": "m590_mag", "mag_count": 3},
        "secondary": {"gun": "m1911", "mag": "m1911_mag", "mag_count": 1},
        "melee": "knife",
        "equipment": {"flash_3": 1},
    },

    "engineer": {
        "name": "Engineer",
        "lore": "Objective / demolitions (limited)",
        "main": {"gun": "mac10", "mag": "mac10_mag", "mag_count": 3},
        "secondary": {"gun": "makarov", "mag": "makarov_mag", "mag_count": 1},
        "melee": "knife",
        "equipment": {"flash_2": 1},
        "special": {"can_place_explosive": True},
    },

    "medic": {
        "name": "Medic",
        "lore": "Team sustain",
        "main": {"gun": "famas", "mag": "famas_mag", "mag_count": 2},
        "secondary": {"gun": "makarov", "mag": "makarov_mag", "mag_count": 2},
        "melee": "knife",
        "equipment": {"flash_1": 1},
        "special": {"revive_bonus": True},
    },
}




