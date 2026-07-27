""" Weapon, equipment and loadout-editor catalog constants. """
# Imports
from dataclasses import dataclass


# Classes
@dataclass(frozen=True)
class Weapon:
	""" A primary weapon catalog entry. For consumable mags (shells/bullets),
	default_mag_count is the total bullets in one stack slot. """
	item_id: str
	display_name: str
	category: str
	magazine_id: str
	default_mag_count: int
	in_loadout: bool

@dataclass(frozen=True)
class SecondaryWeapon:
	""" A secondary (sidearm) catalog entry. """
	item_id: str
	display_name: str
	magazine_id: str
	default_mag_count: int
	in_loadout: bool

@dataclass(frozen=True)
class EquipmentPreset:
	""" A grenade/equipment preset: maps equipment item_id -> count. """
	preset_id: str
	display_name: str
	items: dict[str, int]

@dataclass(frozen=True)
class CamoVariant:
	""" A free cosmetic camo: suffix appended after the scope suffix. """
	suffix: str
	display_name: str

@dataclass(frozen=True)
class GrenadeType:
	""" A throwable grenade slot option ("" = None). """
	item_id: str
	display_name: str

@dataclass(frozen=True)
class Perk:
	""" A loadout perk; score_name is the mgs.special.* flag set when on the loadout. """
	perk_id: str
	display_name: str
	description: str
	score_name: str

# Constants
PRIMARY_WEAPONS: list[Weapon] = [
	# Assault Rifles
	Weapon(item_id="ak47",   display_name="AK-47",        category="Assault Rifle", magazine_id="ak47_mag",     default_mag_count=3,  in_loadout=True),
	Weapon(item_id="m16a4",  display_name="M16A4",        category="Assault Rifle", magazine_id="m16a4_mag",    default_mag_count=3,  in_loadout=True),
	Weapon(item_id="famas",  display_name="FAMAS",        category="Assault Rifle", magazine_id="famas_mag",    default_mag_count=3,  in_loadout=True),
	Weapon(item_id="aug",    display_name="AUG",          category="Assault Rifle", magazine_id="aug_mag",      default_mag_count=3,  in_loadout=True),
	Weapon(item_id="m4a1",   display_name="M4A1",         category="Assault Rifle", magazine_id="m4a1_mag",     default_mag_count=3,  in_loadout=True),
	# Battle Rifles
	Weapon(item_id="fnfal",  display_name="FN FAL",       category="Battle Rifle",  magazine_id="fnfal_mag",    default_mag_count=3,  in_loadout=True),
	Weapon(item_id="g3a3",   display_name="G3A3",         category="Battle Rifle",  magazine_id="g3a3_mag",     default_mag_count=3,  in_loadout=True),
	Weapon(item_id="scar17", display_name="SCAR-17",      category="Battle Rifle",  magazine_id="scar17_mag",   default_mag_count=3,  in_loadout=True),
	# SMGs
	Weapon(item_id="mp5",    display_name="MP5",          category="SMG",           magazine_id="mp5_mag",      default_mag_count=4,  in_loadout=True),
	Weapon(item_id="mp7",    display_name="MP7",          category="SMG",           magazine_id="mp7_mag",      default_mag_count=4,  in_loadout=True),
	Weapon(item_id="mac10",  display_name="MAC-10",       category="SMG",           magazine_id="mac10_mag",    default_mag_count=4,  in_loadout=True),
	Weapon(item_id="ppsh41", display_name="PPSh-41",      category="SMG",           magazine_id="ppsh41_mag",   default_mag_count=3,  in_loadout=True),
	Weapon(item_id="sten",   display_name="Sten",         category="SMG",           magazine_id="sten_mag",     default_mag_count=3,  in_loadout=True),
	# LMGs
	Weapon(item_id="m249",   display_name="M249",         category="LMG",           magazine_id="m249_mag",     default_mag_count=3,  in_loadout=True),
	Weapon(item_id="rpk",    display_name="RPK",          category="LMG",           magazine_id="rpk_mag",      default_mag_count=3,  in_loadout=True),
	# DMR / Snipers
	Weapon(item_id="svd",    display_name="SVD",          category="DMR",           magazine_id="svd_mag",      default_mag_count=3,  in_loadout=True),
	Weapon(item_id="m82",    display_name="M82",          category="Sniper",        magazine_id="m82_mag",      default_mag_count=3,  in_loadout=True),
	Weapon(item_id="mosin",  display_name="Mosin-Nagant", category="Sniper",        magazine_id="mosin_bullet", default_mag_count=10, in_loadout=True),
	Weapon(item_id="m24",    display_name="M24",          category="Sniper",        magazine_id="m24_bullet",   default_mag_count=10, in_loadout=True),
	# Shotguns
	Weapon(item_id="spas12", display_name="SPAS-12",      category="Shotgun",       magazine_id="spas12_shell", default_mag_count=16, in_loadout=True),
	Weapon(item_id="m500",   display_name="M500",         category="Shotgun",       magazine_id="m500_shell",   default_mag_count=12, in_loadout=True),
	Weapon(item_id="m590",   display_name="M590",         category="Shotgun",       magazine_id="m590_shell",   default_mag_count=16, in_loadout=True),
	# Launchers
	Weapon(item_id="rpg7",   display_name="RPG-7",        category="Launcher",      magazine_id="rpg7_rocket",  default_mag_count=3,  in_loadout=True),
]

PRIMARY_INDEX: dict[str, int] = {w.item_id: i for i, w in enumerate(PRIMARY_WEAPONS)}

SECONDARY_WEAPONS: list[SecondaryWeapon] = [
	SecondaryWeapon(item_id="m1911",   display_name="M1911",    magazine_id="m1911_mag",   default_mag_count=2, in_loadout=True),
	SecondaryWeapon(item_id="m9",      display_name="M9",       magazine_id="m9_mag",      default_mag_count=2, in_loadout=True),
	SecondaryWeapon(item_id="deagle",  display_name="Deagle",   magazine_id="deagle_mag",  default_mag_count=2, in_loadout=True),
	SecondaryWeapon(item_id="makarov", display_name="Makarov",  magazine_id="makarov_mag", default_mag_count=2, in_loadout=True),
	SecondaryWeapon(item_id="glock17", display_name="Glock 17", magazine_id="glock17_mag", default_mag_count=2, in_loadout=True),
	SecondaryWeapon(item_id="glock18", display_name="Glock 18", magazine_id="glock18_mag", default_mag_count=2, in_loadout=True),
	SecondaryWeapon(item_id="vz61",    display_name="VZ-61",    magazine_id="vz61_mag",    default_mag_count=2, in_loadout=True),
	SecondaryWeapon(item_id="ray_gun", display_name="Ray Gun",  magazine_id="element_115", default_mag_count=3, in_loadout=False),
]

SECONDARY_INDEX: dict[str, int] = {w.item_id: i for i, w in enumerate(SECONDARY_WEAPONS)}

EQUIPMENT_PRESETS: list[EquipmentPreset] = [
	EquipmentPreset(preset_id="frag2",        display_name="2x Frag Grenade",  items={"frag_grenade": 2}),
	EquipmentPreset(preset_id="semtex2",      display_name="2x Semtex",        items={"semtex": 2}),
	EquipmentPreset(preset_id="flash2",       display_name="2x Flash Grenade", items={"flash_grenade": 2}),
	EquipmentPreset(preset_id="smoke2",       display_name="2x Smoke Grenade", items={"smoke_grenade": 2}),
	EquipmentPreset(preset_id="frag_flash",   display_name="Frag + Flash",     items={"frag_grenade": 1, "flash_grenade": 1}),
	EquipmentPreset(preset_id="frag_smoke",   display_name="Frag + Smoke",     items={"frag_grenade": 1, "smoke_grenade": 1}),
	EquipmentPreset(preset_id="semtex_flash", display_name="Semtex + Flash",   items={"semtex": 1, "flash_grenade": 1}),
	EquipmentPreset(preset_id="semtex_smoke", display_name="Semtex + Smoke",   items={"semtex": 1, "smoke_grenade": 1}),
	EquipmentPreset(preset_id="flash_smoke",  display_name="Flash + Smoke",    items={"flash_grenade": 1, "smoke_grenade": 1}),
	EquipmentPreset(preset_id="none",         display_name="No Equipment",     items={}),
]

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
	# Up to 3x
	"spas12": ("", "_1", "_2", "_3"),
	"m500": ("", "_1", "_2", "_3"),
	"m590": ("", "_1", "_2", "_3"),
	"m249": ("", "_1", "_2", "_3"),
	# Iron Sights + Red Dot only
	"mosin": ("", "_1"),
	# Iron Sights + 4x Scope only (secondary)
	"deagle": ("", "_4"),
}
""" Available scope suffixes per base weapon id ("" = iron sights). """

SCOPE_NAMES: dict[str, str] = {
	"": "Iron Sights",
	"_1": "Holographic",
	"_2": "Kobra",
	"_3": "ACOG Red Dot (3x Scope)",
	"_4": "Mk4 (4x Scope)",
}

ALL_SCOPE_SUFFIXES: list[str] = ["", "_1", "_2", "_3", "_4"]
""" Ordered scope suffixes for trigger offset mapping (offset 0-4). """

TRIG_EDITOR_START         = 100
""" Open loadout editor (create new), then show the hub. """
TRIG_MARKETPLACE          = 101
""" Open marketplace browser. """
TRIG_MY_LOADOUTS          = 102
""" Open my loadouts manager. """

# Editor hub (CoD-style main page): one trigger per category row + remove buttons
TRIG_HUB                  = 103
""" Re-open the editor hub (also used by "Unavailable" no-op rows). """
TRIG_HUB_PRIMARY          = 104
""" Open the primary weapon submenu. """
TRIG_HUB_PRIMARY_MAGS     = 105
""" Open the primary magazine submenu. """
TRIG_HUB_SECONDARY        = 106
""" Open the secondary weapon submenu. """
TRIG_HUB_SECONDARY_MAGS   = 107
""" Open the secondary magazine submenu. """
TRIG_HUB_EQUIP1           = 108
""" Open the grenade slot 1 submenu. """
TRIG_HUB_EQUIP2           = 109
""" Open the grenade slot 2 submenu. """
TRIG_HUB_PERKS            = 110
""" Open the perks submenu. """
TRIG_REMOVE_PRIMARY       = 111
""" Clear the primary weapon. """
TRIG_REMOVE_SECONDARY     = 112
""" Clear the secondary weapon. """

TRIG_PRIMARY_BASE         = 200
""" 200 + primary_weapon_index. """
TRIG_PRIMARY_SCOPE_BASE   = 230
""" 230 + scope_index (0=iron, 1=_1, 2=_2, 3=_3, 4=_4). """
TRIG_SECONDARY_BASE       = 250
""" 250 + secondary_weapon_index. """
TRIG_SECONDARY_SCOPE_BASE = 260
""" 260 + scope_index. """
TRIG_SAVE_PUBLIC          = 350
""" Save loadout as public. """
TRIG_SAVE_PRIVATE         = 351
""" Save loadout as private. """
TRIG_PRIMARY_MAGS_BASE    = 390
""" 390 + count (1-5) -> pick primary mag count (391-395). """
TRIG_SECONDARY_MAGS_BASE  = 396
""" 396 + count (0-5) -> pick secondary mag count (396-401). """
TRIG_PERK_BASE            = 410
""" 410 + perk_index -> toggle perk. """
TRIG_EQUIP_SLOT1_BASE     = 460
""" 460 + grenade_index (0=none,1=frag,2=semtex,3=flash,4=smoke). """
TRIG_EQUIP_SLOT2_BASE     = 470
""" 470 + grenade_index. """
TRIG_PRIMARY_CAMO_BASE    = 480
""" 480-484 = pick primary camo. """
TRIG_SECONDARY_CAMO_BASE  = 490
""" 490-494 = pick secondary camo. """
TRIG_EQUIP1_CAMO_BASE     = 500
""" 500-504 = pick grenade slot 1 camo. """
TRIG_EQUIP2_CAMO_BASE     = 510
""" 510-514 = pick grenade slot 2 camo. """
TRIG_OVERKILL_SEC_BASE    = 520
""" 520 + primary_weapon_index = Overkill secondary. """

TRIG_SELECT_BASE          = 10000
""" + loadout_id -> use as active class. """
TRIG_FAVORITE_BASE        = 20000
""" + loadout_id -> toggle favorite. """
TRIG_LIKE_BASE            = 30000
""" + loadout_id -> like loadout. """
TRIG_DELETE_BASE          = 40000
""" + loadout_id -> delete own loadout. """
TRIG_TOGGLE_VIS_BASE      = 50000
""" + loadout_id -> toggle public/private. """
TRIG_SET_DEFAULT_BASE     = 60000
""" + loadout_id -> set as default. """
TRIG_UNSET_DEFAULT        = 69999
""" Unset default loadout. """
TRIG_EDIT_BASE            = 70000
""" + loadout_id -> edit own loadout (re-opens the hub pre-filled). """
TRIG_MANAGE_BASE          = 80000
""" + loadout_id -> open the per-loadout manage submenu. """
""" Loadout action triggers: base + loadout_id. IDs auto-increment and are never reused, so each
action gets a 10000-wide range (the old 100-wide ranges broke past 99 loadouts). """

TRIG_MARKETPLACE_ALL          = 1600
""" Marketplace: show all public (favorites first). """
TRIG_MARKETPLACE_FAV_ONLY     = 1601
""" Marketplace: show only player's favorited loadouts. """
TRIG_MARKETPLACE_LIKES        = 1602
""" Marketplace: show all sorted by likes descending. """
TRIG_MY_LOADOUTS_FAV_ONLY     = 1603
""" My Loadouts: show only favorited own loadouts. """

PICK10_TOTAL = 10
""" Total Pick-10 points budget. """

COST_PRIMARY_WEAPON    = 1
COST_PRIMARY_SCOPE     = 1
""" Iron sights are free. """
COST_PRIMARY_MAG       = 1
""" Per magazine (base 1 mag included separately). """
COST_SECONDARY_WEAPON  = 1
COST_SECONDARY_SCOPE   = 1
""" Iron sights are free. """
COST_SECONDARY_MAG     = 1
COST_GRENADE           = 1
""" Per grenade (slot 1 and slot 2). """
COST_PERK              = 1

CAMO_VARIANTS: list[CamoVariant] = [
	CamoVariant(suffix="",                     display_name="Default"),
	CamoVariant(suffix="_autumn",              display_name="Autumn"),
	CamoVariant(suffix="_galaxy",              display_name="Galaxy"),
	CamoVariant(suffix="_gold",                display_name="Gold"),
	CamoVariant(suffix="_red_polymer_stripes", display_name="Red Polymer"),
]
""" Free cosmetic camos; the suffix is appended after the scope suffix (ak47 + _3 + _gold). """

GRENADE_TYPES: list[GrenadeType] = [
	GrenadeType(item_id="",              display_name="None"),
	GrenadeType(item_id="frag_grenade",  display_name="Frag Grenade"),
	GrenadeType(item_id="semtex",        display_name="Semtex"),
	GrenadeType(item_id="flash_grenade", display_name="Flash"),
	GrenadeType(item_id="smoke_grenade", display_name="Smoke"),
]

PERKS: list[Perk] = [
	Perk(perk_id="quick_reload",  display_name="Sleight of Hand", description="Reload 50% faster",                       score_name="quick_reload"),
	Perk(perk_id="quick_swap",    display_name="Fast Hands",      description="Swap weapons 50% faster",                 score_name="quick_swap"),
	Perk(perk_id="juggernaut",    display_name="Juggernaut",      description="Increases health to survive more damage", score_name="juggernaut"),
	Perk(perk_id="scavenger",     display_name="Scavenger",       description="Resupplies ammo on every kill",           score_name="scavenger"),
	Perk(perk_id="flak_jacket",   display_name="Flak Jacket",     description="Halves damage from explosives",           score_name="flak_jacket"),
	Perk(perk_id="tracker",       display_name="Tracker",         description="Reveals recent enemy footprints",         score_name="tracker"),
	Perk(perk_id="tactical_mask", display_name="Tactical Mask",   description="Reduces flash, stun, and gas effects",    score_name="tactical_mask"),
	Perk(perk_id="overkill",      display_name="Overkill",        description="Carry a second primary weapon",           score_name="overkill"),
	Perk(perk_id="quick_fix",     display_name="Quick Fix",       description="Health regen starts right after a kill",  score_name="quick_fix"),
]
""" Effects are wired in functional/multiplayer/loadouts/class_selection.py. """

MAX_PERKS = 3
""" Max selectable perks, limited further by available points. """

