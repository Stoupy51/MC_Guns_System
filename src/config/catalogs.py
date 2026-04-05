
# Weapon & Equipment Catalog constants

# Primary weapons: (item_id, display_name, category, magazine_id, default_mag_count, in_loadout)
# For consumable mags (shells/bullets), default_mag_count = total bullets in one stack slot
PRIMARY_WEAPONS: list[tuple[str, str, str, str, int, bool]] = [
    # Assault Rifles
    ("ak47",   "AK-47",       "Assault Rifle", "ak47_mag",   3, True),
    ("m16a4",  "M16A4",       "Assault Rifle", "m16a4_mag",  3, True),
    ("famas",  "FAMAS",       "Assault Rifle", "famas_mag",  3, True),
    ("aug",    "AUG",         "Assault Rifle", "aug_mag",    3, True),
    ("m4a1",   "M4A1",        "Assault Rifle", "m4a1_mag",   3, True),
    # Battle Rifles
    ("fnfal",  "FN FAL",      "Battle Rifle",  "fnfal_mag",  3, True),
    ("g3a3",   "G3A3",        "Battle Rifle",  "g3a3_mag",   3, True),
    ("scar17", "SCAR-17",     "Battle Rifle",  "scar17_mag", 3, True),
    # SMGs
    ("mp5",    "MP5",         "SMG",           "mp5_mag",    4, True),
    ("mp7",    "MP7",         "SMG",           "mp7_mag",    4, True),
    ("mac10",  "MAC-10",      "SMG",           "mac10_mag",  4, True),
    ("ppsh41", "PPSh-41",     "SMG",           "ppsh41_mag", 3, True),
    ("sten",   "Sten",        "SMG",           "sten_mag",   3, True),
    # LMGs
    ("m249",   "M249",        "LMG",           "m249_mag",   3, True),
    ("rpk",    "RPK",         "LMG",           "rpk_mag",    3, True),
    # DMR / Snipers
    ("svd",    "SVD",         "DMR",           "svd_mag",    3, True),
    ("m82",    "M82",         "Sniper",        "m82_mag",    3, True),
    ("mosin",  "Mosin-Nagant", "Sniper",       "mosin_bullet", 10, True),
    ("m24",    "M24",         "Sniper",        "m24_bullet",   10, True),
    # Shotguns
    ("spas12", "SPAS-12",     "Shotgun",       "spas12_shell", 16, True),
    ("m500",   "M500",        "Shotgun",       "m500_shell",   12, True),
    ("m590",   "M590",        "Shotgun",       "m590_shell",   16, True),
    # Launchers
    ("rpg7",   "RPG-7",       "Launcher",      "rpg7_rocket",  3, True),
]

# Index lookup: weapon_id -> index in PRIMARY_WEAPONS
PRIMARY_INDEX: dict[str, int] = {w[0]: i for i, w in enumerate(PRIMARY_WEAPONS)}

# Secondary weapons: (item_id, display_name, magazine_id, default_mag_count, in_loadout)
SECONDARY_WEAPONS: list[tuple[str, str, str, int, bool]] = [
    ("m1911",   "M1911",   "m1911_mag",   2, True),
    ("m9",      "M9",      "m9_mag",      2, True),
    ("deagle",  "Deagle",  "deagle_mag",  2, True),
    ("makarov", "Makarov", "makarov_mag", 2, True),
    ("glock17", "Glock 17", "glock17_mag", 2, True),
    ("glock18", "Glock 18", "glock18_mag", 2, True),
    ("vz61",    "VZ-61",   "vz61_mag",    2, True),
    ("ray_gun", "Ray Gun", "element_115",  3, False),
]

# Index lookup: weapon_id -> index in SECONDARY_WEAPONS
SECONDARY_INDEX: dict[str, int] = {w[0]: i for i, w in enumerate(SECONDARY_WEAPONS)}

# Equipment presets: (preset_id, display_name, items_dict)
# items_dict maps equipment item_id -> count
EQUIPMENT_PRESETS: list[tuple[str, str, dict[str, int]]] = [
    ("frag2",        "2x Frag Grenade",          {"frag_grenade": 2}),
    ("semtex2",      "2x Semtex",                {"semtex": 2}),
    ("flash2",       "2x Flash Grenade",         {"flash_grenade": 2}),
    ("smoke2",       "2x Smoke Grenade",         {"smoke_grenade": 2}),
    ("frag_flash",   "Frag + Flash",             {"frag_grenade": 1, "flash_grenade": 1}),
    ("frag_smoke",   "Frag + Smoke",             {"frag_grenade": 1, "smoke_grenade": 1}),
    ("semtex_flash", "Semtex + Flash",           {"semtex": 1, "flash_grenade": 1}),
    ("semtex_smoke", "Semtex + Smoke",           {"semtex": 1, "smoke_grenade": 1}),
    ("flash_smoke",  "Flash + Smoke",            {"flash_grenade": 1, "smoke_grenade": 1}),
    ("none",         "No Equipment",             {}),
]

# Scope variant definitions per weapon base ID
# Maps base weapon ID -> tuple of available scope suffixes ("" = iron sights)
SCOPE_VARIANTS: dict[str, tuple[str, ...]] = {
    # Full range: Iron Sights, Red Dot, Holographic, 3x Scope, 4x Scope
    "ak47": ("", "_1", "_2", "_3", "_4"),
    "m16a4": ("", "_1", "_2", "_3", "_4"),
    "famas": ("", "_1", "_2", "_3", "_4"),
    "aug": ("", "_1", "_2", "_3", "_4"),
    "m4a1": ("", "_1", "_2", "_3", "_4"),
    "fnfal": ("", "_1", "_2", "_3", "_4"),
    "g3a3": ("", "_1", "_2", "_3", "_4"),
    "scar17": ("", "_1", "_2", "_3", "_4"),
    "mp5": ("", "_1", "_2", "_3", "_4"),
    "mp7": ("", "_1", "_2", "_3", "_4"),
    "svd": ("", "_1", "_2", "_3", "_4"),
    "m82": ("", "_1", "_2", "_3", "_4"),
    "m24": ("", "_1", "_2", "_3", "_4"),
    "rpk": ("", "_1", "_2", "_3", "_4"),
    # Up to 3x: Iron Sights, Red Dot, Holographic, 3x Scope
    "spas12": ("", "_1", "_2", "_3"),
    "m500": ("", "_1", "_2", "_3"),
    "m590": ("", "_1", "_2", "_3"),
    "m249": ("", "_1", "_2", "_3"),
    # Iron Sights + Red Dot only
    "mosin": ("", "_1"),
    # Iron Sights + 4x Scope only (secondary)
    "deagle": ("", "_4"),
}

# Scope suffix -> display name
SCOPE_NAMES: dict[str, str] = {
    "": "Iron Sights",
    "_1": "Holographic",
    "_2": "Kobra",
    "_3": "ACOG Red Dot (3x Scope)",
    "_4": "Mk4 (4x Scope)",
}

# Ordered scope suffixes for trigger offset mapping (offset 0-4)
ALL_SCOPE_SUFFIXES: list[str] = ["", "_1", "_2", "_3", "_4"]

# Trigger value ranges for custom loadout system
TRIG_EDITOR_START         = 100   # Open loadout editor
TRIG_MARKETPLACE          = 101   # Open marketplace browser
TRIG_MY_LOADOUTS          = 102   # Open my loadouts manager
TRIG_PRIMARY_BASE         = 200   # 200 + primary_weapon_index
TRIG_PRIMARY_SCOPE_BASE   = 230   # 230 + scope_index (0=iron, 1=_1, 2=_2, 3=_3, 4=_4)
TRIG_SECONDARY_BASE       = 250   # 250 + secondary_weapon_index (258 = None)
TRIG_SECONDARY_NONE       = 258   # Skip secondary weapon
TRIG_SECONDARY_SCOPE_BASE = 260   # 260 + scope_index
TRIG_EQUIPMENT_BASE       = 300   # 300 + equipment_preset_index
TRIG_SAVE_PUBLIC          = 350   # Save loadout as public
TRIG_SAVE_PRIVATE         = 351   # Save loadout as private
TRIG_BACK_SECONDARY       = 360   # Back to secondary weapon dialog
TRIG_BACK_EQUIPMENT       = 370   # Back to equipment dialog
TRIG_BACK_PERKS           = 380   # Back to perks dialog
TRIG_PRIMARY_MAGS_BASE    = 390   # 390 + count (1-5) -> pick primary mag count (391-395)
TRIG_SECONDARY_MAGS_BASE  = 396   # 396 + count (0-5) -> pick secondary mag count (396-401)

# Perk selection triggers: base + perk index
TRIG_PERK_BASE            = 410   # 410 + perk_index -> toggle perk (410-414 for 5 perks)
TRIG_PERKS_DONE           = 450   # Done selecting perks -> go to confirm

# Grenade slot selection triggers
TRIG_EQUIP_SLOT1_BASE     = 460   # 460 + grenade_index (0=none,1=frag,2=semtex,3=flash,4=smoke)
TRIG_EQUIP_SLOT2_BASE     = 470   # 470 + grenade_index (0=none,1=frag,2=semtex,3=flash,4=smoke)

TRIG_SELECT_BASE          = 1000  # 1000 + loadout_id -> use as active class
TRIG_FAVORITE_BASE        = 1100  # 1100 + loadout_id -> toggle favorite
TRIG_LIKE_BASE            = 1200  # 1200 + loadout_id -> like loadout
TRIG_DELETE_BASE          = 1300  # 1300 + loadout_id -> delete own loadout
TRIG_TOGGLE_VIS_BASE      = 1400  # 1400 + loadout_id -> toggle public/private
TRIG_SET_DEFAULT_BASE     = 1500  # 1500 + loadout_id -> set as default
TRIG_UNSET_DEFAULT        = 1599  # Unset default loadout

# Filter / Sort view triggers
TRIG_MARKETPLACE_ALL          = 1600  # Marketplace: show all public (favorites first)
TRIG_MARKETPLACE_FAV_ONLY     = 1601  # Marketplace: show only player's favorited loadouts
TRIG_MARKETPLACE_LIKES        = 1602  # Marketplace: show all sorted by likes descending
TRIG_MY_LOADOUTS_FAV_ONLY     = 1603  # My Loadouts: show only favorited own loadouts

# Pick-10 System Constants
PICK10_TOTAL = 10  # Total points budget

# Point costs (each item costs this many points)
COST_PRIMARY_WEAPON    = 1  # The primary weapon itself
COST_PRIMARY_SCOPE     = 1  # Any scope on primary (iron sights = 0)
COST_PRIMARY_MAG       = 1  # Per magazine (base 1 mag included separately)
COST_SECONDARY_WEAPON  = 1  # The secondary weapon itself
COST_SECONDARY_SCOPE   = 1  # Any scope on secondary (iron sights = 0)
COST_SECONDARY_MAG     = 1  # Per magazine
COST_GRENADE           = 1  # Per grenade (slot 1 and slot 2)
COST_PERK              = 1  # Per perk

# Grenade types: (item_id, display_name)
GRENADE_TYPES: list[tuple[str, str]] = [
    ("",              "None"),
    ("frag_grenade",  "Frag Grenade"),
    ("semtex",        "Semtex"),
    ("flash_grenade", "Flash"),
    ("smoke_grenade", "Smoke"),
]

# Perks: (perk_id, display_name, description, score_name)
# score_name is the mgs.special.* scoreboard used for each perk effect
PERKS: list[tuple[str, str, str, str]] = [
    ("quick_reload",  "Sleight of Hand", "Reload 50% faster", "quick_reload"),
    ("quick_swap",    "Fast Hands",      "Swap weapons 50% faster", "quick_swap"),
    ("infinite_ammo", "Overkill",        "Unlimited ammo for 30s on spawn", "infinite_ammo"),
]

# Max number of perks selectable (limited further by available points)
MAX_PERKS = 3
