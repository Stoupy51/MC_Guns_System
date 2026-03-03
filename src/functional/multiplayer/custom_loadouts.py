
# ruff: noqa: E501
# Imports
from stewbeet import Mem, write_load_file, write_versioned_function

from .classes import CONSUMABLE_MAGS, TRIGGER_OFFSET

# ============================================================
# Weapon & Equipment Catalogs
# Used at build time to generate dialogs and compute loadout slots
# ============================================================

# Primary weapons: (item_id, display_name, category, magazine_id, default_mag_count)
# For consumable mags (shells/bullets), default_mag_count = total bullets in one stack slot
PRIMARY_WEAPONS: list[tuple[str, str, str, str, int]] = [
	# Assault Rifles
	("ak47",   "AK-47",       "Assault Rifle", "ak47_mag",   3),
	("m16a4",  "M16A4",       "Assault Rifle", "m16a4_mag",  3),
	("famas",  "FAMAS",       "Assault Rifle", "famas_mag",  3),
	("aug",    "AUG",         "Assault Rifle", "aug_mag",    3),
	("m4a1",   "M4A1",        "Assault Rifle", "m4a1_mag",   3),
	# Battle Rifles
	("fnfal",  "FN FAL",      "Battle Rifle",  "fnfal_mag",  3),
	("g3a3",   "G3A3",        "Battle Rifle",  "g3a3_mag",   3),
	("scar17", "SCAR-17",     "Battle Rifle",  "scar17_mag", 3),
	# SMGs
	("mp5",    "MP5",         "SMG",           "mp5_mag",    4),
	("mp7",    "MP7",         "SMG",           "mp7_mag",    4),
	("mac10",  "MAC-10",      "SMG",           "mac10_mag",  4),
	("ppsh41", "PPSh-41",     "SMG",           "ppsh41_mag", 3),
	("sten",   "Sten",        "SMG",           "sten_mag",   3),
	# LMGs
	("m249",   "M249",        "LMG",           "m249_mag",   3),
	("rpk",    "RPK",         "LMG",           "rpk_mag",    3),
	# DMR / Snipers
	("svd",    "SVD",         "DMR",           "svd_mag",    3),
	("m82",    "M82",         "Sniper",        "m82_mag",    3),
	("mosin",  "Mosin-Nagant","Sniper",        "mosin_bullet", 10),
	("m24",    "M24",         "Sniper",        "m24_bullet",   10),
	# Shotguns
	("spas12", "SPAS-12",     "Shotgun",       "spas12_shell", 16),
	("m500",   "M500",        "Shotgun",       "m500_shell",   12),
	("m590",   "M590",        "Shotgun",       "m590_shell",   16),
	# Launchers
	("rpg7",   "RPG-7",       "Launcher",      "rpg7_rocket",  3),
]

# Index lookup: weapon_id → index in PRIMARY_WEAPONS
PRIMARY_INDEX: dict[str, int] = {w[0]: i for i, w in enumerate(PRIMARY_WEAPONS)}

# Secondary weapons: (item_id, display_name, magazine_id, default_mag_count)
SECONDARY_WEAPONS: list[tuple[str, str, str, int]] = [
	("m1911",   "M1911",   "m1911_mag",   2),
	("m9",      "M9",      "m9_mag",      2),
	("deagle",  "Deagle",  "deagle_mag",  2),
	("makarov", "Makarov", "makarov_mag", 2),
	("glock17", "Glock 17","glock17_mag", 2),
	("glock18", "Glock 18","glock18_mag", 2),
	("vz61",    "VZ-61",   "vz61_mag",    2),
]

# Index lookup: weapon_id → index in SECONDARY_WEAPONS
SECONDARY_INDEX: dict[str, int] = {w[0]: i for i, w in enumerate(SECONDARY_WEAPONS)}

# Equipment presets: (preset_id, display_name, items_dict)
# items_dict maps equipment item_id → count
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
# Maps base weapon ID → tuple of available scope suffixes ("" = iron sights)
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

# Scope suffix → display name
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
TRIG_EDITOR_START         = 100  # Open loadout editor
TRIG_MARKETPLACE          = 101  # Open marketplace browser
TRIG_MY_LOADOUTS          = 102  # Open my loadouts manager
TRIG_PRIMARY_BASE         = 200  # 200 + primary_weapon_index
TRIG_PRIMARY_SCOPE_BASE   = 230  # 230 + scope_index (0=iron, 1=_1, 2=_2, 3=_3, 4=_4)
TRIG_SECONDARY_BASE       = 250  # 250 + secondary_weapon_index (258 = None)
TRIG_SECONDARY_NONE       = 258  # Skip secondary weapon
TRIG_SECONDARY_SCOPE_BASE = 260  # 260 + scope_index
TRIG_EQUIPMENT_BASE       = 300  # 300 + equipment_preset_index
TRIG_SAVE_PUBLIC          = 350  # Save loadout as public
TRIG_SAVE_PRIVATE         = 351  # Save loadout as private
TRIG_SELECT_BASE      = 1000 # 1000 + loadout_id → use as active class
TRIG_FAVORITE_BASE    = 1100 # 1100 + loadout_id → toggle favorite
TRIG_LIKE_BASE        = 1200 # 1200 + loadout_id → like loadout
TRIG_DELETE_BASE      = 1300 # 1300 + loadout_id → delete own loadout
TRIG_TOGGLE_VIS_BASE  = 1400 # 1400 + loadout_id → toggle public/private
TRIG_SET_DEFAULT_BASE = 1500 # 1500 + loadout_id → set as default
TRIG_UNSET_DEFAULT    = 1599 # Unset default loadout


def build_custom_loadout_slots_snbt(ns: str, primary_id: str, secondary_id: str, equipment_preset_idx: int) -> str:
	"""Build the slots SNBT array from weapon choices (same format as default class slots).
	Returns the SNBT string for the slots array content (without outer brackets)."""
	slots: list[str] = []

	def add_slot(slot: str, loot: str, count: int = 1, consumable: bool = False, bullets: int = 0) -> None:
		slots.append(
			f'{{slot:"{slot}",loot:"{ns}:i/{loot}",count:{count},consumable:{"1b" if consumable else "0b"},bullets:{bullets}}}'
		)

	# Primary weapon → hotbar.0
	primary = PRIMARY_WEAPONS[PRIMARY_INDEX[primary_id]]
	add_slot("hotbar.0", primary[0])

	# Secondary weapon → hotbar.1 (if selected)
	secondary = SECONDARY_WEAPONS[SECONDARY_INDEX[secondary_id]] if secondary_id else None
	if secondary:
		add_slot("hotbar.1", secondary[0])

	# Equipment → hotbar.8, hotbar.7, ...
	preset = EQUIPMENT_PRESETS[equipment_preset_idx]
	equip_slot = 8
	for item_id, count in preset[2].items():
		add_slot(f"hotbar.{equip_slot}", item_id, count=count)
		equip_slot -= 1

	# Primary magazines → inventory.0, inventory.1, ...
	inv_slot = 0
	mag_id = primary[3]
	mag_count = primary[4]
	if mag_id in CONSUMABLE_MAGS:
		add_slot(f"inventory.{inv_slot}", mag_id, consumable=True, bullets=mag_count)
		inv_slot += 1
	else:
		for _ in range(mag_count):
			add_slot(f"inventory.{inv_slot}", mag_id)
			inv_slot += 1

	# Secondary magazines → continuing inventory slots
	if secondary:
		sec_mag_id = secondary[2]
		sec_mag_count = secondary[3]
		if sec_mag_id in CONSUMABLE_MAGS:
			add_slot(f"inventory.{inv_slot}", sec_mag_id, consumable=True, bullets=sec_mag_count)
			inv_slot += 1
		else:
			for _ in range(sec_mag_count):
				add_slot(f"inventory.{inv_slot}", sec_mag_id)
				inv_slot += 1

	return ",".join(slots)


def generate_custom_loadouts() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	## ============================
	## Scoreboards & Storage for custom loadouts
	## ============================
	write_load_file(
f"""
## Custom loadout system
# Unique player IDs (auto-increment, used to identify loadout ownership)
# Global next-pid counter
# Player's default custom loadout ID (0 = none → use standard class)
# Editor state tracker (0 = not editing)
scoreboard objectives add {ns}.mp.pid dummy
execute unless score #next_pid {ns}.data matches 1.. run scoreboard players set #next_pid {ns}.data 1
scoreboard objectives add {ns}.mp.default dummy
scoreboard objectives add {ns}.mp.edit_step dummy
""")

	## Initialize custom loadout storage (only if not already set)
	write_load_file(
f"""
# Custom loadouts list (persists across reloads)
execute unless data storage {ns}:multiplayer custom_loadouts run data modify storage {ns}:multiplayer custom_loadouts set value []
# Per-player preference data (persists across reloads)
execute unless data storage {ns}:multiplayer player_data run data modify storage {ns}:multiplayer player_data set value []
# Auto-increment counter for loadout IDs
execute unless data storage {ns}:multiplayer next_loadout_id run data modify storage {ns}:multiplayer next_loadout_id set value 1
""")

	## ============================
	## Assign player ID on first interaction (called from player tick if pid == 0)
	## ============================
	write_versioned_function("multiplayer/assign_pid",
f"""
# Assign a unique player ID
scoreboard players operation @s {ns}.mp.pid = #next_pid {ns}.data
scoreboard players add #next_pid {ns}.data 1

# Initialize player data entry in storage
data modify storage {ns}:temp _new_player set value {{pid:0,favorites:[],liked:[],default_loadout:0}}
execute store result storage {ns}:temp _new_player.pid int 1 run scoreboard players get @s {ns}.mp.pid
data modify storage {ns}:multiplayer player_data append from storage {ns}:temp _new_player
""")

	## ============================
	## Player tick hook: assign pid if needed
	## ============================
	write_versioned_function("player/tick",
f"""
# Custom loadouts: assign player ID if not yet assigned
execute unless score @s {ns}.mp.pid matches 1.. run function {ns}:v{version}/multiplayer/assign_pid
""", prepend=True)

	## ====================================================================
	## LOADOUT EDITOR — 4-step dialog flow
	## ====================================================================

	## ============================
	## Step 1: editor/start — Build and show primary weapon selection dialog
	## ============================
	# Build the dialog statically since the weapon list is fixed at build time
	primary_actions: list[str] = []
	for idx, (gun_id, display, category, _mag, _mc) in enumerate(PRIMARY_WEAPONS):
		trig = TRIG_PRIMARY_BASE + idx
		primary_actions.append(
			f'{{label:{{text:"{display}",color:"green"}},'
			f'tooltip:{{text:"{category}"}},'
			f'action:{{type:"run_command",command:"/trigger {ns}.player.config set {trig}"}}}}'
		)
	primary_actions_snbt = ",".join(primary_actions)

	write_versioned_function("multiplayer/editor/start",
f"""
# Mark editor as active (step 1 = picking primary)
scoreboard players set @s {ns}.mp.edit_step 1

# Build primary weapon selection dialog
data modify storage {ns}:temp dialog set value {{\
type:"minecraft:multi_action",\
title:{{text:"Create Loadout — Pick Primary",color:"gold",bold:true}},\
body:[{{type:"minecraft:plain_message",contents:{{text:"Choose your primary weapon.",color:"gray"}}}}],\
actions:[{primary_actions_snbt}],\
columns:2,\
after_action:"close",\
exit_action:{{label:"Cancel"}}\
}}

# Show dialog
function {ns}:v{version}/multiplayer/show_dialog with storage {ns}:temp
""")

	## ============================
	## Step 2: editor/pick_primary — Store primary choice, route to scope or secondary
	## ============================
	# For each primary weapon, generate a dispatch line that stores the choice in temp
	# Include scope defaults: primary_scope="", primary_scope_name="Iron Sights", primary_full=gun_id
	pick_primary_lines = ""
	for idx, (gun_id, display, category, mag_id, mag_count) in enumerate(PRIMARY_WEAPONS):
		trig = TRIG_PRIMARY_BASE + idx
		pick_primary_lines += (
			f'execute if score @s {ns}.player.config matches {trig} run '
			f'data modify storage {ns}:temp editor set value '
			f'{{primary:"{gun_id}",primary_name:"{display}",primary_mag:"{mag_id}",primary_mag_count:{mag_count},'
			f'primary_scope:"",primary_scope_name:"Iron Sights",primary_full:"{gun_id}"}}\n'
		)

	# Build scope routing: weapons with scope variants → scope dialog, others → secondary dialog
	scope_route_lines = ""
	# Group weapons by their scope variant set for routing
	scope_set_func: dict[tuple[str, ...], str] = {
		("", "_1", "_2", "_3", "_4"): "scope/primary_full",
		("", "_1", "_2", "_3"):       "scope/primary_no4",
		("", "_1"):                   "scope/primary_1only",
	}
	for gun_id, *_ in PRIMARY_WEAPONS:
		if gun_id in SCOPE_VARIANTS:
			variants = SCOPE_VARIANTS[gun_id]
			func_name = scope_set_func[variants]
			scope_route_lines += (
				f'execute if data storage {ns}:temp editor{{primary:"{gun_id}"}} run '
				f'return run function {ns}:v{version}/multiplayer/editor/{func_name}\n'
			)

	write_versioned_function("multiplayer/editor/pick_primary",
f"""
# Store primary weapon choice based on trigger value
{pick_primary_lines}
# Route: weapons with scope variants go to scope dialog, others skip to secondary
{scope_route_lines}
# No scope variants: go directly to secondary selection
function {ns}:v{version}/multiplayer/editor/show_secondary_dialog
""")

	## ============================
	## Scope dialogs for primary weapon (one per unique scope variant set)
	## ============================
	# Helper: build scope action buttons SNBT
	def scope_actions_snbt(trig_base: int, variants: tuple[str, ...]) -> str:
		actions: list[str] = []
		for suffix in variants:
			idx = ALL_SCOPE_SUFFIXES.index(suffix)
			trig = trig_base + idx
			name = SCOPE_NAMES[suffix]
			actions.append(
				f'{{label:{{text:"{name}",color:"green"}},'
				f'action:{{type:"run_command",command:"/trigger {ns}.player.config set {trig}"}}}}'
			)
		return ",".join(actions)

	# Full scope set: Iron Sights, Red Dot, Holographic, 3x Scope, 4x Scope
	full_scope_snbt = scope_actions_snbt(TRIG_PRIMARY_SCOPE_BASE, ("", "_1", "_2", "_3", "_4"))
	write_versioned_function("multiplayer/editor/scope/primary_full",
f"""
data modify storage {ns}:temp dialog set value {{\
type:"minecraft:multi_action",\
title:{{text:"Create Loadout — Pick Scope",color:"gold",bold:true}},\
body:[{{type:"minecraft:plain_message",contents:{{text:"Choose your optic attachment.",color:"gray"}}}}],\
actions:[{full_scope_snbt}],\
columns:2,\
after_action:"close",\
exit_action:{{label:"Cancel"}}\
}}
function {ns}:v{version}/multiplayer/show_dialog with storage {ns}:temp
""")

	# No _4 set: Iron Sights, Red Dot, Holographic, 3x Scope
	no4_scope_snbt = scope_actions_snbt(TRIG_PRIMARY_SCOPE_BASE, ("", "_1", "_2", "_3"))
	write_versioned_function("multiplayer/editor/scope/primary_no4",
f"""
data modify storage {ns}:temp dialog set value {{\
type:"minecraft:multi_action",\
title:{{text:"Create Loadout — Pick Scope",color:"gold",bold:true}},\
body:[{{type:"minecraft:plain_message",contents:{{text:"Choose your optic attachment.",color:"gray"}}}}],\
actions:[{no4_scope_snbt}],\
columns:2,\
after_action:"close",\
exit_action:{{label:"Cancel"}}\
}}
function {ns}:v{version}/multiplayer/show_dialog with storage {ns}:temp
""")

	# Mosin: Iron Sights, Red Dot only
	mosin_scope_snbt = scope_actions_snbt(TRIG_PRIMARY_SCOPE_BASE, ("", "_1"))
	write_versioned_function("multiplayer/editor/scope/primary_1only",
f"""
data modify storage {ns}:temp dialog set value {{\
type:"minecraft:multi_action",\
title:{{text:"Create Loadout — Pick Scope",color:"gold",bold:true}},\
body:[{{type:"minecraft:plain_message",contents:{{text:"Choose your optic attachment.",color:"gray"}}}}],\
actions:[{mosin_scope_snbt}],\
columns:2,\
after_action:"close",\
exit_action:{{label:"Cancel"}}\
}}
function {ns}:v{version}/multiplayer/show_dialog with storage {ns}:temp
""")

	## ============================
	## editor/pick_primary_scope — Store scope choice, compute full weapon ID, show secondary
	## ============================
	pick_scope_lines = ""
	for suffix in ALL_SCOPE_SUFFIXES:
		idx = ALL_SCOPE_SUFFIXES.index(suffix)
		trig = TRIG_PRIMARY_SCOPE_BASE + idx
		name = SCOPE_NAMES[suffix]
		pick_scope_lines += (
			f'execute if score @s {ns}.player.config matches {trig} run '
			f'data modify storage {ns}:temp editor.primary_scope set value "{suffix}"\n'
		)
		pick_scope_lines += (
			f'execute if score @s {ns}.player.config matches {trig} run '
			f'data modify storage {ns}:temp editor.primary_scope_name set value "{name}"\n'
		)

	write_versioned_function("multiplayer/editor/pick_primary_scope",
f"""
# Store scope choice
{pick_scope_lines}
# Compute full weapon ID: base + scope suffix (e.g. "ak47" + "_3" = "ak47_3")
function {ns}:v{version}/multiplayer/editor/set_primary_full with storage {ns}:temp editor

# Show secondary weapon dialog
function {ns}:v{version}/multiplayer/editor/show_secondary_dialog
""")

	## Macro: compute primary_full = primary + primary_scope
	write_versioned_function("multiplayer/editor/set_primary_full",
f"""$data modify storage {ns}:temp editor.primary_full set value "$(primary)$(primary_scope)"
""")

	## ============================
	## show_secondary_dialog — Build and show secondary weapon selection dialog
	## ============================
	secondary_actions: list[str] = []
	for idx, (gun_id, display, mag_id, _mc) in enumerate(SECONDARY_WEAPONS):
		trig = TRIG_SECONDARY_BASE + idx
		secondary_actions.append(
			f'{{label:{{text:"{display}",color:"green"}},'
			f'tooltip:{{text:"Pistol"}},'
			f'action:{{type:"run_command",command:"/trigger {ns}.player.config set {trig}"}}}}'
		)
	# Add "None" option
	secondary_actions.append(
		f'{{label:{{text:"No Secondary",color:"red"}},'
		f'tooltip:{{text:"Skip secondary weapon"}},'
		f'action:{{type:"run_command",command:"/trigger {ns}.player.config set {TRIG_SECONDARY_NONE}"}}}}'
	)
	secondary_actions_snbt = ",".join(secondary_actions)

	write_versioned_function("multiplayer/editor/show_secondary_dialog",
f"""
scoreboard players set @s {ns}.mp.edit_step 2

data modify storage {ns}:temp dialog set value {{\
type:"minecraft:multi_action",\
title:{{text:"Create Loadout — Pick Secondary",color:"gold",bold:true}},\
body:[{{type:"minecraft:plain_message",contents:{{text:"Choose your secondary weapon (or skip).",color:"gray"}}}}],\
actions:[{secondary_actions_snbt}],\
columns:2,\
after_action:"close",\
exit_action:{{label:"Cancel"}}\
}}
function {ns}:v{version}/multiplayer/show_dialog with storage {ns}:temp
""")

	## ============================
	## Step 3: editor/pick_secondary — Store secondary choice, route to scope or equipment
	## ============================
	pick_secondary_lines = ""
	for idx, (gun_id, display, mag_id, mag_count) in enumerate(SECONDARY_WEAPONS):
		trig = TRIG_SECONDARY_BASE + idx
		pick_secondary_lines += (
			f'execute if score @s {ns}.player.config matches {trig} run '
			f'data modify storage {ns}:temp editor.secondary set value "{gun_id}"\n'
		)
		pick_secondary_lines += (
			f'execute if score @s {ns}.player.config matches {trig} run '
			f'data modify storage {ns}:temp editor.secondary_name set value "{display}"\n'
		)
		pick_secondary_lines += (
			f'execute if score @s {ns}.player.config matches {trig} run '
			f'data modify storage {ns}:temp editor.secondary_mag set value "{mag_id}"\n'
		)
		pick_secondary_lines += (
			f'execute if score @s {ns}.player.config matches {trig} run '
			f'data modify storage {ns}:temp editor.secondary_mag_count set value {mag_count}\n'
		)
		# Set scope defaults
		pick_secondary_lines += (
			f'execute if score @s {ns}.player.config matches {trig} run '
			f'data modify storage {ns}:temp editor.secondary_scope set value ""\n'
		)
		pick_secondary_lines += (
			f'execute if score @s {ns}.player.config matches {trig} run '
			f'data modify storage {ns}:temp editor.secondary_scope_name set value "Iron Sights"\n'
		)
		pick_secondary_lines += (
			f'execute if score @s {ns}.player.config matches {trig} run '
			f'data modify storage {ns}:temp editor.secondary_full set value "{gun_id}"\n'
		)
	# Handle "None" option
	pick_secondary_lines += (
		f'execute if score @s {ns}.player.config matches {TRIG_SECONDARY_NONE} run '
		f'data modify storage {ns}:temp editor.secondary set value ""\n'
	)
	pick_secondary_lines += (
		f'execute if score @s {ns}.player.config matches {TRIG_SECONDARY_NONE} run '
		f'data modify storage {ns}:temp editor.secondary_name set value "None"\n'
	)
	pick_secondary_lines += (
		f'execute if score @s {ns}.player.config matches {TRIG_SECONDARY_NONE} run '
		f'data modify storage {ns}:temp editor.secondary_scope set value ""\n'
	)
	pick_secondary_lines += (
		f'execute if score @s {ns}.player.config matches {TRIG_SECONDARY_NONE} run '
		f'data modify storage {ns}:temp editor.secondary_scope_name set value ""\n'
	)
	pick_secondary_lines += (
		f'execute if score @s {ns}.player.config matches {TRIG_SECONDARY_NONE} run '
		f'data modify storage {ns}:temp editor.secondary_full set value ""\n'
	)

	# Route: deagle has scope variants → show scope dialog, others → equipment
	secondary_scope_route = (
		f'execute if data storage {ns}:temp editor{{secondary:"deagle"}} run '
		f'return run function {ns}:v{version}/multiplayer/editor/scope/secondary_4only\n'
	)

	write_versioned_function("multiplayer/editor/pick_secondary",
f"""
# Store secondary weapon choice based on trigger value
{pick_secondary_lines}
# Route: deagle → scope dialog, others → equipment dialog
{secondary_scope_route}
# No scope variants: go directly to equipment selection
function {ns}:v{version}/multiplayer/editor/show_equipment_dialog
""")

	## ============================
	## Secondary scope dialog: deagle (Iron Sights + 4x Scope)
	## ============================
	deagle_scope_snbt = scope_actions_snbt(TRIG_SECONDARY_SCOPE_BASE, ("", "_4"))
	write_versioned_function("multiplayer/editor/scope/secondary_4only",
f"""
data modify storage {ns}:temp dialog set value {{\
type:"minecraft:multi_action",\
title:{{text:"Create Loadout — Pick Scope (Secondary)",color:"gold",bold:true}},\
body:[{{type:"minecraft:plain_message",contents:{{text:"Choose your secondary optic.",color:"gray"}}}}],\
actions:[{deagle_scope_snbt}],\
columns:2,\
after_action:"close",\
exit_action:{{label:"Cancel"}}\
}}
function {ns}:v{version}/multiplayer/show_dialog with storage {ns}:temp
""")

	## ============================
	## editor/pick_secondary_scope — Store scope choice, compute full ID, show equipment
	## ============================
	pick_sec_scope_lines = ""
	for suffix in ALL_SCOPE_SUFFIXES:
		idx = ALL_SCOPE_SUFFIXES.index(suffix)
		trig = TRIG_SECONDARY_SCOPE_BASE + idx
		name = SCOPE_NAMES[suffix]
		pick_sec_scope_lines += (
			f'execute if score @s {ns}.player.config matches {trig} run '
			f'data modify storage {ns}:temp editor.secondary_scope set value "{suffix}"\n'
		)
		pick_sec_scope_lines += (
			f'execute if score @s {ns}.player.config matches {trig} run '
			f'data modify storage {ns}:temp editor.secondary_scope_name set value "{name}"\n'
		)

	write_versioned_function("multiplayer/editor/pick_secondary_scope",
f"""
# Store secondary scope choice
{pick_sec_scope_lines}
# Compute full secondary weapon ID
function {ns}:v{version}/multiplayer/editor/set_secondary_full with storage {ns}:temp editor

# Show equipment dialog
function {ns}:v{version}/multiplayer/editor/show_equipment_dialog
""")

	## Macro: compute secondary_full = secondary + secondary_scope
	write_versioned_function("multiplayer/editor/set_secondary_full",
f"""$data modify storage {ns}:temp editor.secondary_full set value "$(secondary)$(secondary_scope)"
""")

	## ============================
	## show_equipment_dialog — Build and show equipment preset selection dialog
	## ============================
	equipment_actions: list[str] = []
	for idx, (preset_id, display, items) in enumerate(EQUIPMENT_PRESETS):
		trig = TRIG_EQUIPMENT_BASE + idx
		equipment_actions.append(
			f'{{label:{{text:"{display}",color:"green"}},'
			f'action:{{type:"run_command",command:"/trigger {ns}.player.config set {trig}"}}}}'
		)
	equipment_actions_snbt = ",".join(equipment_actions)

	write_versioned_function("multiplayer/editor/show_equipment_dialog",
f"""
scoreboard players set @s {ns}.mp.edit_step 3

data modify storage {ns}:temp dialog set value {{\
type:"minecraft:multi_action",\
title:{{text:"Create Loadout — Pick Equipment",color:"gold",bold:true}},\
body:[{{type:"minecraft:plain_message",contents:{{text:"Choose your equipment loadout.",color:"gray"}}}}],\
actions:[{equipment_actions_snbt}],\
columns:2,\
after_action:"close",\
exit_action:{{label:"Cancel"}}\
}}
function {ns}:v{version}/multiplayer/show_dialog with storage {ns}:temp
""")

	## ============================
	## Step 4: editor/pick_equipment — Store equipment, show confirm dialog
	## ============================
	pick_equipment_lines = ""
	for idx, (preset_id, display, items) in enumerate(EQUIPMENT_PRESETS):
		trig = TRIG_EQUIPMENT_BASE + idx
		pick_equipment_lines += (
			f'execute if score @s {ns}.player.config matches {trig} run '
			f'data modify storage {ns}:temp editor.equipment_idx set value {idx}\n'
		)
		pick_equipment_lines += (
			f'execute if score @s {ns}.player.config matches {trig} run '
			f'data modify storage {ns}:temp editor.equipment_name set value "{display}"\n'
		)

	write_versioned_function("multiplayer/editor/pick_equipment",
f"""
# Store equipment preset choice
{pick_equipment_lines}
# Advance to step 4
scoreboard players set @s {ns}.mp.edit_step 4

# Build confirmation dialog with summary
# We use a notice-style dialog with two action buttons (public/private)
data modify storage {ns}:temp dialog set value {{\
type:"minecraft:multi_action",\
title:{{text:"Create Loadout — Confirm",color:"gold",bold:true}},\
body:[\
{{type:"minecraft:plain_message",contents:{{text:"Review your loadout:",color:"white"}}}},\
{{type:"minecraft:item",item:{{id:"minecraft:poisonous_potato",components:{{"minecraft:item_model":"{ns}:placeholder"}}}},description:{{contents:[{{"text":"Loading...","color":"gray"}}]}}}}\
],\
actions:[\
{{label:{{text:"Save as Public",color:"green"}},tooltip:{{text:"Everyone can see and use this loadout"}},action:{{type:"run_command",command:"/trigger {ns}.player.config set {TRIG_SAVE_PUBLIC}"}}}},\
{{label:{{text:"Save as Private",color:"yellow"}},tooltip:{{text:"Only you can see and use this loadout"}},action:{{type:"run_command",command:"/trigger {ns}.player.config set {TRIG_SAVE_PRIVATE}"}}}}\
],\
columns:2,\
after_action:"close",\
exit_action:{{label:"Cancel"}}\
}}

# Show dialog via macro-built summary
function {ns}:v{version}/multiplayer/editor/show_confirm with storage {ns}:temp editor
""")

	## ============================
	## editor/show_confirm — macro function to build the confirmation body text
	## ============================
	write_versioned_function("multiplayer/editor/show_confirm",
f"""
# Build summary body using macro substitution
$data modify storage {ns}:temp dialog.body set value [\
{{type:"minecraft:plain_message",contents:["",{{"text":"▸ Primary: ","color":"white"}},{{"text":"$(primary_name)","color":"green","bold":true}},{{"text":" ($(primary_scope_name))","color":"dark_green"}}]}},\
{{type:"minecraft:plain_message",contents:["",{{"text":"▸ Secondary: ","color":"white"}},{{"text":"$(secondary_name)","color":"yellow","bold":true}},{{"text":" ($(secondary_scope_name))","color":"gold"}}]}},\
{{type:"minecraft:plain_message",contents:["",{{"text":"▸ Equipment: ","color":"white"}},{{"text":"$(equipment_name)","color":"aqua","bold":true}}]}},\
{{type:"minecraft:plain_message",contents:{{text:"\\nSave this loadout?","color":"gray"}}}}\
]

# Show the dialog
function {ns}:v{version}/multiplayer/show_dialog with storage {ns}:temp
""")

	## ============================
	## editor/save — Create the loadout entry and store it
	## Called with trigger 350 (public) or 351 (private)
	## ============================
	# Build the slot computation for every possible combination at runtime
	# Since we can't run Python at runtime, we pre-build slot data for each weapon combo.
	# Instead, we generate the slots dynamically using a macro function.
	# The save function reads from editor temp, computes slots, and appends to custom_loadouts.

	# First, generate a mapping from weapon IDs to their slot data
	# We need a macro that accepts primary/secondary/equipment_idx and builds slots
	# Since we can't do arbitrary computation in mcfunction, we pre-generate all possible
	# primary→slots and secondary→slots at build time as storage entries.

	# Pre-generate primary weapon slot data (hotbar.0 + magazines)
	primary_slot_entries: list[str] = []
	for gun_id, display, category, mag_id, mag_count in PRIMARY_WEAPONS:
		slots = [f'{{slot:"hotbar.0",loot:"{ns}:i/{gun_id}",count:1,consumable:0b,bullets:0}}']
		inv_slot = 0
		if mag_id in CONSUMABLE_MAGS:
			slots.append(f'{{slot:"inventory.{inv_slot}",loot:"{ns}:i/{mag_id}",count:1,consumable:1b,bullets:{mag_count}}}')
			inv_slot += 1
		else:
			for _ in range(mag_count):
				slots.append(f'{{slot:"inventory.{inv_slot}",loot:"{ns}:i/{mag_id}",count:1,consumable:0b,bullets:0}}')
				inv_slot += 1
		slots_snbt = ",".join(slots)
		primary_slot_entries.append(f'{{id:"{gun_id}",slots:[{slots_snbt}],next_inv_slot:{inv_slot}}}')

	primary_slot_table_snbt = ",".join(primary_slot_entries)

	# Pre-generate secondary weapon slot data (hotbar.1 + magazines, inv_slot is relative)
	secondary_slot_entries: list[str] = []
	for gun_id, display, mag_id, mag_count in SECONDARY_WEAPONS:
		slots = [f'{{slot:"hotbar.1",loot:"{ns}:i/{gun_id}",count:1,consumable:0b,bullets:0}}']
		# Secondary mag slots start at a variable inv_slot, so we use relative offsets
		# and fix them up at save time. Use placeholder "inv_offset_N" style.
		rel_slots: list[str] = []
		if mag_id in CONSUMABLE_MAGS:
			rel_slots.append(f'{{loot:"{ns}:i/{mag_id}",count:1,consumable:1b,bullets:{mag_count}}}')
		else:
			for _ in range(mag_count):
				rel_slots.append(f'{{loot:"{ns}:i/{mag_id}",count:1,consumable:0b,bullets:0}}')
		rel_snbt = ",".join(rel_slots)
		slots_snbt = ",".join(slots)
		secondary_slot_entries.append(f'{{id:"{gun_id}",fixed_slots:[{slots_snbt}],mag_slots:[{rel_snbt}]}}')

	secondary_slot_table_snbt = ",".join(secondary_slot_entries)

	# Pre-generate equipment slot data (hotbar.8, hotbar.7, ...)
	equipment_slot_entries: list[str] = []
	for preset_id, display, items in EQUIPMENT_PRESETS:
		equip_slots: list[str] = []
		equip_slot = 8
		for item_id, count in items.items():
			equip_slots.append(f'{{slot:"hotbar.{equip_slot}",loot:"{ns}:i/{item_id}",count:{count},consumable:0b,bullets:0}}')
			equip_slot -= 1
		equip_snbt = ",".join(equip_slots)
		equipment_slot_entries.append(f'{{id:"{preset_id}",slots:[{equip_snbt}]}}')

	equipment_slot_table_snbt = ",".join(equipment_slot_entries)

	# Write slot lookup tables to storage on load
	write_load_file(
f"""
# Slot lookup tables for custom loadout editor (pre-computed at build time)
data modify storage {ns}:multiplayer primary_slot_table set value [{primary_slot_table_snbt}]
data modify storage {ns}:multiplayer secondary_slot_table set value [{secondary_slot_table_snbt}]
data modify storage {ns}:multiplayer equipment_slot_table set value [{equipment_slot_table_snbt}]
""")

	## ============================
	## editor/save — Main save function
	## ============================
	# Generate dispatch lines to find the right slot data from the lookup tables
	save_primary_dispatch = ""
	for idx, (gun_id, *_) in enumerate(PRIMARY_WEAPONS):
		save_primary_dispatch += (
			f'execute if data storage {ns}:temp editor{{primary:"{gun_id}"}} run '
			f'data modify storage {ns}:temp _build.primary_data set from storage {ns}:multiplayer primary_slot_table[{idx}]\n'
		)

	save_secondary_dispatch = ""
	for idx, (gun_id, *_) in enumerate(SECONDARY_WEAPONS):
		save_secondary_dispatch += (
			f'execute if data storage {ns}:temp editor{{secondary:"{gun_id}"}} run '
			f'data modify storage {ns}:temp _build.secondary_data set from storage {ns}:multiplayer secondary_slot_table[{idx}]\n'
		)

	save_equipment_dispatch = ""
	for idx, (preset_id, *_) in enumerate(EQUIPMENT_PRESETS):
		save_equipment_dispatch += (
			f'execute if data storage {ns}:temp editor{{equipment_idx:{idx}}} run '
			f'data modify storage {ns}:temp _build.equipment_data set from storage {ns}:multiplayer equipment_slot_table[{idx}]\n'
		)

	write_versioned_function("multiplayer/editor/save",
f"""
# Determine visibility from trigger value
scoreboard players set #cl_public {ns}.data 0
execute if score @s {ns}.player.config matches {TRIG_SAVE_PUBLIC} run scoreboard players set #cl_public {ns}.data 1

# Initialize build workspace
data modify storage {ns}:temp _build set value {{}}

# Look up primary weapon slot data
{save_primary_dispatch}
# Look up secondary weapon slot data (skip if no secondary)
{save_secondary_dispatch}
# Look up equipment slot data
{save_equipment_dispatch}

# Build the final loadout entry
# Start with base structure
data modify storage {ns}:temp _new_loadout set value {{id:0,owner_pid:0,owner_name:"",name:"",public:0b,likes:0,main_gun:"",secondary_gun:"",slots:[]}}

# Set loadout ID from counter
execute store result storage {ns}:temp _new_loadout.id int 1 run data get storage {ns}:multiplayer next_loadout_id

# Increment the counter
execute store result score #temp {ns}.data run data get storage {ns}:multiplayer next_loadout_id
scoreboard players add #temp {ns}.data 1
execute store result storage {ns}:multiplayer next_loadout_id int 1 run scoreboard players get #temp {ns}.data

# Set owner info
execute store result storage {ns}:temp _new_loadout.owner_pid int 1 run scoreboard players get @s {ns}.mp.pid
# Owner name is set by a macro call (pass player display name via team prefix trick)

# Set weapon info (store the full scope-modified weapon IDs)
data modify storage {ns}:temp _new_loadout.main_gun set from storage {ns}:temp editor.primary_full
data modify storage {ns}:temp _new_loadout.secondary_gun set from storage {ns}:temp editor.secondary_full

# Set visibility
execute if score #cl_public {ns}.data matches 1 run data modify storage {ns}:temp _new_loadout.public set value 1b

# Override weapon loot entries with scope-modified weapon IDs (e.g. "ak47_3" instead of "ak47")
function {ns}:v{version}/multiplayer/editor/fix_primary_loot with storage {ns}:temp editor
execute if data storage {ns}:temp _build.secondary_data run function {ns}:v{version}/multiplayer/editor/fix_secondary_loot with storage {ns}:temp editor

# Build the combined slot list: primary slots + secondary slots + equipment slots
# 1. Copy primary weapon & magazine slots
data modify storage {ns}:temp _new_loadout.slots set from storage {ns}:temp _build.primary_data.slots

# 2. Append secondary gun slot (hotbar.1)
execute if data storage {ns}:temp _build.secondary_data run data modify storage {ns}:temp _new_loadout.slots append from storage {ns}:temp _build.secondary_data.fixed_slots[0]

# 3. Append secondary magazine slots (need to fix inventory slot numbers)
# Get next_inv_slot from primary data to know where secondary mags start
execute store result score #inv_slot {ns}.data run data get storage {ns}:temp _build.primary_data.next_inv_slot
# Use recursive function to append secondary mags with correct slot numbers
execute if data storage {ns}:temp _build.secondary_data.mag_slots[0] run function {ns}:v{version}/multiplayer/editor/append_sec_mags

# 4. Append equipment slots
execute if data storage {ns}:temp _build.equipment_data.slots[0] run function {ns}:v{version}/multiplayer/editor/append_equip_slots

# Auto-generate loadout name: "Primary + Secondary" or just "Primary"
function {ns}:v{version}/multiplayer/editor/set_name with storage {ns}:temp editor

# Append to the custom loadouts list
data modify storage {ns}:multiplayer custom_loadouts append from storage {ns}:temp _new_loadout

# Reset editor state
scoreboard players set @s {ns}.mp.edit_step 0

# Notify player
function {ns}:v{version}/multiplayer/editor/notify_saved with storage {ns}:temp editor
""")

	## ============================
	## editor/set_name — macro to auto-name the loadout
	## ============================
	write_versioned_function("multiplayer/editor/set_name",
f"""$data modify storage {ns}:temp _new_loadout.name set value "$(primary_name) + $(secondary_name)"
""")

	## ============================
	## editor/notify_saved — tellraw confirmation
	## ============================
	write_versioned_function("multiplayer/editor/notify_saved",
f"""$tellraw @s ["",{{"text":"[MGS] ","color":"gold"}},{{"text":"Loadout saved: ","color":"white"}},{{"text":"$(primary_name) + $(secondary_name)","color":"green","bold":true}}]
""")

	## ============================
	## editor/fix_primary_loot — macro: override primary weapon loot with scope-modified ID
	## ============================
	write_versioned_function("multiplayer/editor/fix_primary_loot",
f"""$data modify storage {ns}:temp _build.primary_data.slots[0].loot set value "{ns}:i/$(primary_full)"
""")

	## ============================
	## editor/fix_secondary_loot — macro: override secondary weapon loot with scope-modified ID
	## ============================
	write_versioned_function("multiplayer/editor/fix_secondary_loot",
f"""$data modify storage {ns}:temp _build.secondary_data.fixed_slots[0].loot set value "{ns}:i/$(secondary_full)"
""")

	## ============================
	## editor/append_sec_mags — recursive: fix inventory slot numbers for secondary magazines
	## ============================
	write_versioned_function("multiplayer/editor/append_sec_mags",
f"""
# Copy the first mag slot template
data modify storage {ns}:temp _sec_mag set from storage {ns}:temp _build.secondary_data.mag_slots[0]

# Set the correct inventory slot number using score
# Build the slot string: "inventory.N"
execute store result storage {ns}:temp _inv_n int 1 run scoreboard players get #inv_slot {ns}.data
function {ns}:v{version}/multiplayer/editor/set_sec_mag_slot with storage {ns}:temp

# Append to loadout slots
data modify storage {ns}:temp _new_loadout.slots append from storage {ns}:temp _sec_mag

# Increment inv_slot counter
scoreboard players add #inv_slot {ns}.data 1

# Remove processed and recurse
data remove storage {ns}:temp _build.secondary_data.mag_slots[0]
execute if data storage {ns}:temp _build.secondary_data.mag_slots[0] run function {ns}:v{version}/multiplayer/editor/append_sec_mags
""")

	## ============================
	## editor/set_sec_mag_slot — macro to set the slot field with correct inventory index
	## ============================
	write_versioned_function("multiplayer/editor/set_sec_mag_slot",
f"""$data modify storage {ns}:temp _sec_mag.slot set value "inventory.$(_inv_n)"
""")

	## ============================
	## editor/append_equip_slots — recursive: append equipment slots to the loadout
	## ============================
	write_versioned_function("multiplayer/editor/append_equip_slots",
f"""
# Append the first equipment slot
data modify storage {ns}:temp _new_loadout.slots append from storage {ns}:temp _build.equipment_data.slots[0]

# Remove and recurse
data remove storage {ns}:temp _build.equipment_data.slots[0]
execute if data storage {ns}:temp _build.equipment_data.slots[0] run function {ns}:v{version}/multiplayer/editor/append_equip_slots
""")

	## ====================================================================
	## STUB FUNCTIONS — Placeholders for features to be implemented next
	## ====================================================================

	# Marketplace: browse public custom loadouts
	write_versioned_function("multiplayer/marketplace/browse",
f"""
# TODO: Build dialog listing all public custom loadouts with select/favorite/like buttons
tellraw @s [{{"text":"[MGS] ","color":"gold"}},{{"text":"Marketplace coming soon!","color":"yellow"}}]
""")

	# My Loadouts: browse own custom loadouts
	write_versioned_function("multiplayer/my_loadouts/browse",
f"""
# TODO: Build dialog listing player's own custom loadouts with manage actions
tellraw @s [{{"text":"[MGS] ","color":"gold"}},{{"text":"My Loadouts coming soon!","color":"yellow"}}]
""")

	# Select/use a custom loadout in-game
	write_versioned_function("multiplayer/custom/select",
f"""
# TODO: Look up custom loadout by ID and apply it (similar to apply_class)
tellraw @s [{{"text":"[MGS] ","color":"gold"}},{{"text":"Custom loadout selection coming soon!","color":"yellow"}}]
""")

	# Toggle favorite on a custom loadout
	write_versioned_function("multiplayer/custom/toggle_favorite",
f"""
# TODO: Add/remove loadout ID from player's favorites list
tellraw @s [{{"text":"[MGS] ","color":"gold"}},{{"text":"Favorites coming soon!","color":"yellow"}}]
""")

	# Like a custom loadout
	write_versioned_function("multiplayer/custom/like",
f"""
# TODO: Increment loadout's like counter, track in player's liked list
tellraw @s [{{"text":"[MGS] ","color":"gold"}},{{"text":"Likes coming soon!","color":"yellow"}}]
""")

	# Delete own custom loadout
	write_versioned_function("multiplayer/custom/delete",
f"""
# TODO: Find and remove loadout from custom_loadouts list if owner matches
tellraw @s [{{"text":"[MGS] ","color":"gold"}},{{"text":"Delete coming soon!","color":"yellow"}}]
""")

	# Toggle public/private on own custom loadout
	write_versioned_function("multiplayer/custom/toggle_visibility",
f"""
# TODO: Toggle public flag on own loadout
tellraw @s [{{"text":"[MGS] ","color":"gold"}},{{"text":"Visibility toggle coming soon!","color":"yellow"}}]
""")

	# Set default custom loadout
	write_versioned_function("multiplayer/custom/set_default",
f"""
# TODO: Set the default custom loadout for auto-selection on game start
tellraw @s [{{"text":"[MGS] ","color":"gold"}},{{"text":"Default loadout coming soon!","color":"yellow"}}]
""")

	# Unset default loadout
	write_versioned_function("multiplayer/custom/unset_default",
f"""
# Unset default custom loadout - use standard class instead
scoreboard players set @s {ns}.mp.default 0
tellraw @s [{{"text":"[MGS] ","color":"gold"}},{{"text":"Default loadout cleared. Standard class will be used.","color":"green"}}]
""")
