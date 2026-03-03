
# Imports
from stewbeet import JsonDict

# Consumable magazine item IDs (stack count = bullet count, uses set_consumable_count modifier)
CONSUMABLE_MAGS: set[str] = {"rpg7_rocket", "mosin_bullet", "m24_bullet", "spas12_shell", "m500_shell", "m590_shell"}

# Balanced team-vs-team class loadouts (Python-side definitions)
# Used at build time to generate SNBT for storage initialization
CLASSES: dict[str, JsonDict] = {
    "assault": {
        "name": "Assault",
        "lore": "Versatile frontline",
        "main": {"gun": "ak47", "mag": "ak47_mag", "mag_count": 3},
        "secondary": {"gun": "m1911", "mag": "m1911_mag", "mag_count": 2},
        "equipment": {"frag_grenade": 2, "smoke_grenade": 1},
    },
    "rifleman": {
        "name": "Rifleman",
        "lore": "Accurate mid-range",
        "main": {"gun": "m16a4", "mag": "m16a4_mag", "mag_count": 3},
        "secondary": {"gun": "m9", "mag": "m9_mag", "mag_count": 2},
        "equipment": {"flash_grenade": 1, "smoke_grenade": 1},
    },
    "support": {
        "name": "Support",
        "lore": "Suppressive heavy",
        "main": {"gun": "m249", "mag": "m249_mag", "mag_count": 3},
        "secondary": {"gun": "glock17", "mag": "glock17_mag", "mag_count": 2},
        "equipment": {"smoke_grenade": 2},
    },
    "sniper": {
        "name": "Sniper",
        "lore": "Long-range precision",
        "main": {"gun": "m24_4", "mag": "m24_bullet", "mag_count": 10},
        "secondary": {"gun": "deagle", "mag": "deagle_mag", "mag_count": 2},
        "equipment": {"flash_grenade": 1},
    },
    "smg": {
        "name": "SMG",
        "lore": "Close quarters",
        "main": {"gun": "mp7", "mag": "mp7_mag", "mag_count": 4},
        "secondary": {"gun": "glock18", "mag": "glock18_mag", "mag_count": 2},
        "equipment": {"flash_grenade": 2},
    },
    "shotgunner": {
        "name": "Shotgunner",
        "lore": "Breaching / CQB",
        "main": {"gun": "spas12", "mag": "spas12_shell", "mag_count": 16},
        "secondary": {"gun": "m9", "mag": "m9_mag", "mag_count": 2},
        "equipment": {"semtex": 2},
    },
    "engineer": {
        "name": "Engineer",
        "lore": "Objective / demolitions",
        "main": {"gun": "mp5", "mag": "mp5_mag", "mag_count": 3},
        "secondary": {"gun": "makarov", "mag": "makarov_mag", "mag_count": 2},
        "equipment": {"semtex": 2, "smoke_grenade": 1},
    },
    "medic": {
        "name": "Medic",
        "lore": "Team sustain",
        "main": {"gun": "famas", "mag": "famas_mag", "mag_count": 3},
        "secondary": {"gun": "m1911", "mag": "m1911_mag", "mag_count": 2},
        "equipment": {"smoke_grenade": 2},
    },
    "marksman": {
        "name": "Marksman",
        "lore": "Semi-auto precision",
        "main": {"gun": "svd", "mag": "svd_mag", "mag_count": 3},
        "secondary": {"gun": "glock17", "mag": "glock17_mag", "mag_count": 2},
        "equipment": {"flash_grenade": 1, "smoke_grenade": 1},
    },
    "heavy": {
        "name": "Heavy",
        "lore": "Armored suppressor",
        "main": {"gun": "rpk", "mag": "rpk_mag", "mag_count": 3},
        "secondary": {"gun": "makarov", "mag": "makarov_mag", "mag_count": 2},
        "equipment": {"frag_grenade": 2},
    },
}

# Class number assignments (1-indexed, used for scoreboard mgs.mp.class)
CLASS_IDS: dict[str, int] = {class_id: idx + 1 for idx, class_id in enumerate(CLASSES)}

# Trigger value offset (trigger_value = TRIGGER_OFFSET + class_num)
TRIGGER_OFFSET: int = 10


def get_class_description(class_id: str) -> str:
    """ Get the hover/lore description text for a class. """
    data = CLASSES[class_id]
    main_gun: str = data["main"]["gun"].upper().replace("_", " ")
    secondary_gun: str = data.get("secondary", {}).get("gun", "").upper().replace("_", " ")
    return f"{data['lore']}\nMain: {main_gun}\nSecondary: {secondary_gun}"


def build_class_snbt(ns: str, class_id: str, class_data: JsonDict, class_num: int) -> str:
    """ Build the SNBT representation of a class for storage initialization.
    The format is designed for dynamic loadout application via recursive slot iteration. """
    trigger_value: int = TRIGGER_OFFSET + class_num
    main_gun: str = class_data["main"]["gun"]
    secondary_gun: str = class_data.get("secondary", {}).get("gun", "")

    # Build the flat slot list (pre-computed slot assignments)
    slots: list[str] = []
    def add_slot(slot: str, loot: str, count: int = 1, consumable: bool = False, bullets: int = 0) -> None:
        slots.append(
            f'{{slot:"{slot}",loot:"{ns}:i/{loot}",count:{count},consumable:{"1b" if consumable else "0b"},bullets:{bullets}}}'
        )

    # Primary weapon → hotbar.0
    add_slot("hotbar.0", main_gun)

    # Secondary weapon → hotbar.1
    if secondary_gun:
        add_slot("hotbar.1", secondary_gun)

    # Equipment (grenades) → hotbar.8, hotbar.7, ...
    equip_slot: int = 8
    for item_id, count in class_data.get("equipment", {}).items():
        add_slot(f"hotbar.{equip_slot}", item_id, count=count)
        equip_slot -= 1

    # Magazines → inventory.0, inventory.1, ...
    inv_slot: int = 0

    # Primary magazines
    mag_id: str = class_data["main"]["mag"]
    mag_count: int = class_data["main"].get("mag_count", 0)
    if mag_id in CONSUMABLE_MAGS:
        add_slot(f"inventory.{inv_slot}", mag_id, consumable=True, bullets=mag_count)
        inv_slot += 1
    else:
        for _ in range(mag_count):
            add_slot(f"inventory.{inv_slot}", mag_id)
            inv_slot += 1

    # Secondary magazines
    if "secondary" in class_data:
        sec_mag_id: str = class_data["secondary"]["mag"]
        sec_mag_count: int = class_data["secondary"].get("mag_count", 0)
        if sec_mag_id in CONSUMABLE_MAGS:
            add_slot(f"inventory.{inv_slot}", sec_mag_id, consumable=True, bullets=sec_mag_count)
            inv_slot += 1
        else:
            for _ in range(sec_mag_count):
                add_slot(f"inventory.{inv_slot}", sec_mag_id)
                inv_slot += 1

    slots_snbt: str = ",".join(slots)
    return (
        f'{{id:"{class_id}",name:"{class_data["name"]}",lore:"{class_data["lore"]}",'
        f'trigger_value:{trigger_value},main_gun:"{main_gun}",secondary_gun:"{secondary_gun}",'
        f'slots:[{slots_snbt}]}}'
    )

