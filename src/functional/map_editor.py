
# ruff: noqa: E501
# Map Editor - Generic for Multiplayer, Missions, and Zombies maps
# Provides an in-game editor with mode switching for placing map elements.
# Elements are placed via spawn eggs detected by advancement (item_used_on_block).
# Markers in the world represent elements during editing; storage is written on save.

from typing import Any, cast

from stewbeet import Advancement, JsonDict, Mem, set_json_encoder, write_load_file, write_versioned_function

from .helpers import MGS_TAG, btn
from .zombies.perks import PERK_DEFINITIONS, RECOMMENDED_PRICES

MAX_MAPS = 50

# Perk reference lines for the perk_machine tooltips, generated from the perk registry so they can
# never drift out of sync with the actual perks (ids grouped 5/line, prices as "Name N" grouped 3/line).
_PERK_IDS: list[str] = list(PERK_DEFINITIONS.keys())
_PERK_ID_DOC: str = (
	"Perk granted by this machine:\n"
	+ "\n".join(" · ".join(_PERK_IDS[i:i + 5]) for i in range(0, len(_PERK_IDS), 5))
	+ "\n\nThe Random Perk power-up and Der Wunderfizz only roll perks that have a\n"
	"machine placed on this map (unless a Wunderfizz has all_perks set), so\n"
	"which perks you place here shapes what they can grant."
)
_PERK_PRICE_PAIRS: list[str] = [f'{PERK_DEFINITIONS[pid].display_name} {RECOMMENDED_PRICES.get(pid, 2000)}' for pid in _PERK_IDS]
_PERK_PRICE_DOC: str = (
	"Cost in points to buy this perk.\n"
	"Leave at -1 to auto-resolve the recommended price from perk_id.\n"
	"Recommended prices:\n"
	+ "\n".join(" · ".join(_PERK_PRICE_PAIRS[i:i + 3]) for i in range(0, len(_PERK_PRICE_PAIRS), 3))
)

# Element Definitions ───────────────────────────────────────────
# All element types across all modes. Each has display properties, save info, and egg model.
# save_type: "base" (single, handled specially), "spawn" (list of [x,y,z,yaw]), "point" (list of [x,y,z])
#            "zb_object" (list of compound objects with pos/rotation/group_id + extra fields)
ALL_ELEMENTS: dict[str, JsonDict] = {
	"base_coordinates":   {"name": "Base Coordinates", "color": "light_purple", "particle": [1.0, 0.0, 1.0], "particle_scale": 1.5, "has_rotation": False, "egg_model": "minecraft:endermite_spawn_egg", "save_type": "base", "emoji": "⬟"},
	"red_spawn":          {"name": "Red Spawn",        "color": "red",          "particle": [1.0, 0.2, 0.2], "particle_scale": 1.0, "has_rotation": True,  "egg_model": "minecraft:magma_cube_spawn_egg", "save_type": "spawn", "save_path": "spawning_points.red", "emoji": "●"},
	"blue_spawn":         {"name": "Blue Spawn",       "color": "blue",         "particle": [0.2, 0.2, 1.0], "particle_scale": 1.0, "has_rotation": True,  "egg_model": "minecraft:dolphin_spawn_egg", "save_type": "spawn", "save_path": "spawning_points.blue", "emoji": "●"},
	"general_spawn":      {"name": "General Spawn",    "color": "yellow",       "particle": [1.0, 1.0, 0.2], "particle_scale": 1.0, "has_rotation": True,  "egg_model": "minecraft:blaze_spawn_egg", "save_type": "spawn", "save_path": "spawning_points.general", "emoji": "●"},
	"out_of_bounds":      {"name": "Out of Bounds",    "color": "dark_red",     "particle": [0.6, 0.0, 0.0], "particle_scale": 1.0, "has_rotation": False, "egg_model": "minecraft:spider_spawn_egg", "save_type": "point", "save_path": "out_of_bounds", "emoji": "☠"},
	"boundary":           {"name": "Boundary Corner",  "color": "gray",         "particle": [0.8, 0.8, 0.8], "particle_scale": 1.0, "has_rotation": False, "egg_model": "minecraft:skeleton_spawn_egg", "save_type": "point", "save_path": "boundaries", "emoji": "◻"},
	"search_and_destroy": {"name": "S&D Objective",    "color": "gold",         "particle": [1.0, 0.6, 0.0], "particle_scale": 1.0, "has_rotation": False, "egg_model": "minecraft:fox_spawn_egg", "save_type": "point", "save_path": "search_and_destroy", "emoji": "💣"},
	"domination":         {"name": "Domination Point", "color": "green",        "particle": [0.0, 1.0, 0.0], "particle_scale": 1.0, "has_rotation": False, "egg_model": "minecraft:creeper_spawn_egg", "save_type": "point", "save_path": "domination", "emoji": "🏴"},
	"hardpoint":          {"name": "Hardpoint Zone",   "color": "dark_purple",  "particle": [0.5, 0.0, 0.5], "particle_scale": 1.0, "has_rotation": False, "egg_model": "minecraft:warden_spawn_egg", "save_type": "point", "save_path": "hardpoint", "emoji": "⚡"},
	"start_command":      {"name": "Start Command",    "color": "aqua",         "particle": [0.0, 0.9, 0.9], "particle_scale": 1.0, "has_rotation": False, "egg_model": "minecraft:allay_spawn_egg", "save_type": "start_command", "save_path": "start_commands", "emoji": "⚙"},
	"respawn_command":    {"name": "Respawn Command",  "color": "dark_aqua",    "particle": [0.0, 0.7, 0.7], "particle_scale": 1.0, "has_rotation": False, "egg_model": "minecraft:vex_spawn_egg", "save_type": "respawn_command", "save_path": "respawn_commands", "emoji": "↺"},
	# Mission elements
	"mission_spawn":      {"name": "Mission Spawn",    "color": "aqua",         "particle": [0.0, 1.0, 1.0], "particle_scale": 1.0, "has_rotation": True,  "egg_model": "minecraft:villager_spawn_egg", "save_type": "spawn", "save_path": "spawning_points.mission", "emoji": "●"},
	"enemy":              {"name": "Enemy",            "color": "red",          "particle": [1.0, 0.2, 0.2], "particle_scale": 1.0, "has_rotation": False, "egg_model": "minecraft:pillager_spawn_egg", "save_type": "enemy", "save_path": "enemies", "emoji": "👤", "config_uses_default_function": True},
	# Config (utility, no marker)
	"config":             {"name": "⚙ Config",         "color": "white",        "particle": [1.0, 1.0, 1.0], "particle_scale": 0.5, "has_rotation": False, "egg_model": "minecraft:allay_spawn_egg", "save_type": "config", "emoji": "⚙"},
	# Zombies elements (zb_object: compound data with pos/rotation/group_id + extra fields)
	"zombie_spawn":       {"name": "Zombie Spawn",     "color": "dark_green",   "particle": [0.0, 0.5, 0.0], "particle_scale": 1.0, "has_rotation": True,  "egg_model": "minecraft:zombie_spawn_egg",      "save_type": "zb_object", "save_path": "spawning_points.zombies", "emoji": "🧟",
                           "defaults": {"activation_box": []}},
	"player_spawn_zb":    {"name": "Player Spawn",     "color": "aqua",         "particle": [0.0, 1.0, 1.0], "particle_scale": 1.0, "has_rotation": True,  "egg_model": "minecraft:villager_spawn_egg",    "save_type": "zb_object", "save_path": "spawning_points.players", "emoji": "●",
                           "defaults": {}},
	# Special spawns are the "not a regular zombie" spawn set: dog rounds use them today, mini-bosses
	# and other scripted arrivals can reuse them later. A map without any simply never gets those rounds.
	"special_spawn":      {"name": "Special Spawn",    "color": "dark_red",     "particle": [0.6, 0.0, 0.2], "particle_scale": 1.0, "has_rotation": True,  "egg_model": "minecraft:wolf_spawn_egg",        "save_type": "zb_object", "save_path": "spawning_points.special", "emoji": "🐺",
                           "defaults": {"activation_box": []}},
	"wallbuy":            {"name": "Wallbuy",          "color": "yellow",       "particle": [1.0, 1.0, 0.0], "particle_scale": 1.0, "has_rotation": True,  "egg_model": "minecraft:iron_golem_spawn_egg",  "save_type": "zb_object", "save_path": "wallbuys", "emoji": "🔫",
                           "defaults": {"name": "", "price": 1000, "refill_price": 500, "refill_price_pap": 4500, "weapon_id": "m1911", "magazine_id": "m1911_mag"}},
	"door":               {
		"name": "Door", "color": "gold", "particle": [1.0, 0.6, 0.0], "particle_scale": 1.0, "has_rotation": True,
		"egg_model": "minecraft:hoglin_spawn_egg", "save_type": "zb_object", "save_path": "doors", "emoji": "🚪",
		"defaults": {"name": "Door", "back_name": "Door", "price": 1000, "partial_price": 0, "link_id": 1, "back_group_id": -1, "block": "", "animation": 0, "sound": ""},
		"requires_offhand_block": True,
	},
	# Trap types: 0 = fire, 1 = electric, 2 = turret
	"trap":               {"name": "Trap",             "color": "red",          "particle": [1.0, 0.2, 0.2], "particle_scale": 1.0, "has_rotation": True,  "egg_model": "minecraft:cave_spider_spawn_egg", "save_type": "zb_object", "save_path": "traps", "emoji": "🔮",
                           "defaults": {"price": 1000, "type": 0, "duration": 200, "cooldown": 1200, "effect_radius": [3.0, 2.0, 3.0], "offset_pos": [0, 0, 0], "power": True}},
	"perk_machine":       {"name": "Perk Machine",     "color": "dark_purple",  "particle": [0.5, 0.0, 0.5], "particle_scale": 1.0, "has_rotation": True,  "egg_model": "minecraft:witch_spawn_egg",       "save_type": "zb_object", "save_path": "perks", "emoji": "🧪",
                           "defaults": {"name": "", "price": -1, "partial_price": 0, "perk_id": "juggernog", "power": True, "display_item": "", "item_model": ""}},
	"wunderfizz":         {"name": "Der Wunderfizz",   "color": "gold",         "particle": [1.0, 0.7, 0.0], "particle_scale": 1.0, "has_rotation": True,  "egg_model": "minecraft:bee_spawn_egg",         "save_type": "zb_object", "save_path": "wunderfizz", "emoji": "🎰",
                           "defaults": {"name": "Der Wunderfizz", "price": 1500, "power": True, "all_perks": False, "can_start_on": True, "display_item": "", "item_model": ""}},
	"pap_machine":        {"name": "Pack-a-Punch",     "color": "dark_red",     "particle": [0.8, 0.1, 0.1], "particle_scale": 1.0, "has_rotation": True,  "egg_model": "minecraft:creaking_spawn_egg",    "save_type": "zb_object", "save_path": "pap_machines", "emoji": "🔥",
                           "defaults": {"name": "Pack-a-Punch", "price": 5000, "power": True, "display_item": "", "item_model": ""}},
	"mystery_box_pos":    {"name": "Mystery Box Pos",  "color": "light_purple", "particle": [1.0, 0.0, 1.0], "particle_scale": 1.0, "has_rotation": True,  "egg_model": "minecraft:evoker_spawn_egg",      "save_type": "zb_object", "save_path": "mystery_box.positions", "emoji": "📦",
                           "defaults": {"can_start_on": True, "display_item": "", "item_model": ""}},
	"power_switch":       {"name": "Power Switch",     "color": "green",        "particle": [0.0, 1.0, 0.0], "particle_scale": 1.0, "has_rotation": True,  "egg_model": "minecraft:slime_spawn_egg",       "save_type": "zb_object", "save_path": "power_switch", "emoji": "⚡",
                           "defaults": {}},
	"barrier":            {"name": "Barrier",          "color": "aqua",         "particle": [0.0, 1.0, 1.0], "particle_scale": 1.0, "has_rotation": True,  "egg_model": "minecraft:guardian_spawn_egg",    "save_type": "zb_object", "save_path": "barriers",     "emoji": "🧱",
                           "defaults": {
                                "block_enabled":  {"Name": "minecraft:oak_fence_gate", "Properties": {"open": "false"}},
                                "block_disabled": {"Name": "minecraft:oak_fence_gate", "Properties": {"open": "true"}},
                                "radius": 2,
                           }},
}

# Elements rendered as real in-game models in the editor (instead of dust particles).
# Each has a maps/editor/displays/<etype> function mirroring the game's own display setup,
# rebuilt every second so rotation/config edits on the marker stay in sync.
MODEL_DISPLAY_ELEMENTS: tuple[str, ...] = ("wallbuy", "perk_machine", "wunderfizz", "pap_machine", "mystery_box_pos", "power_switch", "barrier")

# Field documentation ───────────────────────────────────────────
# Tooltips shown (as a hover "ⓘ") next to constant/enum config fields in the element editor,
# so map makers don't have to guess what the magic numbers mean. Keyed by (element_type, field);
# a plain field-name key acts as a fallback shared across element types (e.g. "power").
FIELD_DOCS: dict[tuple[str, str] | str, str] = {
	("trap", "type"): "Trap behaviour:\n0 = Fire — lethal to zombies, burns players inside\n1 = Electric — lethal to zombies, shocks players inside\n2 = Turret — auto-fires at the nearest zombie every 5 ticks",
	("trap", "duration"): "How long the trap stays active, in ticks (20 ticks = 1 second).",
	("trap", "cooldown"): "Cooldown before the trap can be re-triggered, in ticks (20 = 1s).",
	("door", "animation"): "Open animation:\n0 = Destroy — block-break particles + sound\n1+ = Silent — blocks instantly replaced with air",
	("door", "link_id"): "Doors that share a link_id open together as a single purchase.",
	("door", "partial_price"): "Chip-in payments: points taken per right-click (0 = pay the full price at once).\nExample: price 5000 + partial_price 500 = 10 payments.\nDoor progress is GLOBAL — any mix of players can contribute, and the last\npayment is just whatever is left. Progress is shared by every linked door.",
	("perk_machine", "partial_price"): "Chip-in payments: points taken per right-click (0 = pay the full price at once).\nExample: price 2500 + partial_price 500 = 5 payments.\nPerk progress is LOCAL — each player pays down their own perk, nobody can\ncontribute to someone else's. Progress is lost when the perk is obtained.",
	("door", "back_group_id"): "Zombie spawn group_id unlocked behind this door (-1 = none).",
	("perk_machine", "name"): "Display label shown when hovering the machine.\nLeave EMPTY to auto-resolve the perk's canonical name from perk_id\n(e.g. juggernog -> Juggernog). Only set this to override that name.",
	("perk_machine", "perk_id"): _PERK_ID_DOC,
	("perk_machine", "price"): _PERK_PRICE_DOC,
	("wunderfizz", "all_perks"): "false = the machine only rolls perks that have a machine placed on\nthis map (like the Random Perk power-up).\ntrue = rolls across EVERY defined perk (BO2 Origins behaviour), so it\ncan grant perks with no machine on the map.",
	("wunderfizz", "price"): "Points per use. Cycles perk bottles and grants one random perk the\nbuyer doesn't already own, collectable by the buyer for 10s. Suggested: 1500.",
	("wallbuy", "weapon_id"): "Item id given on purchase. Guns (e.g. m1911, ak47, mp5),\nknives (bowie_knife, ~3000 pts), lethal grenades (frag_grenade,\nsemtex...), or tacticals (monkey_bomb). Non-guns route to their\nown slot: knife hotbar.0, lethals hotbar.7 (x4), tacticals hotbar.6 (x3).",
	("wallbuy", "magazine_id"): "Magazine item paired with the gun (e.g. m1911_mag).\nLeave empty for knife/grenade/tactical wallbuys.",
	("barrier", "radius"): "Block radius the barrier toggles open/closed around its marker.",
	"activation_box": "Optional [x, y, z, dx, dy, dz] box (relative to this spawn, in blocks).\nWhen set, this spawn only produces enemies while a player stands inside the box.\nx/y/z = corner offset from the spawn, dx/dy/dz = size. Empty [] = always active.",
	# Shared fallbacks (any element type):
	"can_start_on": "true = the machine is allowed to be the ACTIVE (usable) spot at game\nstart and after it roams. false = a valid roam destination, but never\nthe first active spot. Only one spot is active at a time; the rest show\na grayed-out disabled model. At least one spot must allow starting.",
	"power": "true = requires the map's power to be switched on before it works\nfalse = always usable",
	"price": "Cost in points to buy/use this element.",
}

# Mode Definitions ──────────────────────────────────────────────
# Each mode defines which elements are available and their slot assignments.
# storage_key: key in {ns}:maps storage (e.g., multiplayer, zombies, missions)
EDITOR_MODES: dict[str, JsonDict] = {
	"multiplayer": {
		"name": "Multiplayer",
		"color": "gold",
		"storage_key": "multiplayer",
		"slots": {
			"base_coordinates": "hotbar.0",
			"red_spawn": "hotbar.1",
			"blue_spawn": "hotbar.2",
			"general_spawn": "hotbar.3",
			"out_of_bounds": "hotbar.4",
			"boundary": "hotbar.5",
			"search_and_destroy": "hotbar.6",
			"domination": "inventory.0",
			"hardpoint": "inventory.1",
			"start_command": "inventory.2",
			"respawn_command": "inventory.3",
		},
	},
	"zombies": {
		"name": "Zombies",
		"color": "dark_green",
		"storage_key": "zombies",
		"slots": {
			"base_coordinates": "hotbar.0",
			"player_spawn_zb": "hotbar.1",
			"zombie_spawn": "hotbar.2",
			"wallbuy": "hotbar.3",
			"door": "hotbar.4",
			"trap": "hotbar.5",
			"perk_machine": "inventory.0",
			"mystery_box_pos": "inventory.1",
			"power_switch": "inventory.2",
			"out_of_bounds": "inventory.3",
			"boundary": "inventory.4",
			"pap_machine": "inventory.5",
			"start_command": "inventory.6",
			"special_spawn": "inventory.7",
			"barrier": "inventory.8",
			"wunderfizz": "inventory.9",
		},
	},
	"missions": {
		"name": "Missions",
		"color": "aqua",
		"storage_key": "missions",
		"slots": {
			"base_coordinates": "hotbar.0",
			"mission_spawn": "hotbar.1",
			"enemy": "hotbar.2",
			"out_of_bounds": "hotbar.3",
			"boundary": "hotbar.4",
			"config": "hotbar.5",
			"start_command": "inventory.0",
			"respawn_command": "inventory.1",
		},
	},
}

MODE_LIST: list[str] = list(EDITOR_MODES.keys())


def generate_map_editor() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	sep = '{"text":"============================================","color":"dark_gray"}'

	# Scoreboards & Storage Init ─────────────────────────────────
	write_load_file(f"""
# Map editor scoreboards
scoreboard objectives add {ns}.mp.map_edit dummy
scoreboard objectives add {ns}.mp.map_idx dummy
scoreboard objectives add {ns}.mp.map_mode dummy
scoreboard objectives add {ns}.mp.map_disp dummy

# Reuse warped fungus on stick detection (shared with class menu)
scoreboard objectives add {ns}.class_menu minecraft.used:minecraft.warped_fungus_on_a_stick
""")

	storage_init_lines = "\n".join(
		f'execute unless data storage {ns}:maps {mode_info["storage_key"]} run data modify storage {ns}:maps {mode_info["storage_key"]} set value []'
		for mode_info in EDITOR_MODES.values()
	)
	write_load_file(f"""
# Initialize maps storage for all modes
{storage_init_lines}
""")

	# Advancement for egg placement detection ─────────────────────
	adv: JsonDict = {
		"criteria": {
			"requirement": {
				"trigger": "minecraft:item_used_on_block",
				"conditions": {
					"location": [
						{
							"condition": "minecraft:match_tool",
							"predicate": {
								"predicates": {
									"minecraft:custom_data": {ns: {"editor": True}}
								}
							}
						}
					]
				}
			}
		},
		"rewards": {
			"function": f"{ns}:v{version}/maps/editor/on_place"
		}
	}
	Mem.ctx.data[ns].advancements[f"v{version}/maps/editor/on_place"] = set_json_encoder(Advancement(adv), max_level=-1)

	# Mode tab buttons (used in all list views) ──────────────────
	mode_tabs = ",".join(
		btn(mode_info["name"], f"/function {ns}:v{version}/maps/editor/list/{mode_key}", mode_info["color"], f"View {mode_info['name']} maps")
		for mode_key, mode_info in EDITOR_MODES.items()
	)

	# Menu Entry Point ───────────────────────────────────────────
	write_versioned_function("maps/editor/menu", f"""
# Default: show multiplayer maps
function {ns}:v{version}/maps/editor/list/multiplayer
""")

	# Per-Mode Map List ──────────────────────────────────────────
	for mode_key, mode_info in EDITOR_MODES.items():
		sk = mode_info["storage_key"]
		create_btn = btn("+ Create New Map", f"/function {ns}:v{version}/maps/editor/create/{mode_key}", "green", f"Create a new {mode_info['name']} map")

		write_versioned_function(f"maps/editor/list/{mode_key}", f"""
tellraw @s {sep}
tellraw @s ["","       🗺 ",[{{"text":"","color":"gold","bold":true}},{{"text":"Map Editor"}}]," 🗺"]
tellraw @s {sep}
tellraw @s ["  ",{mode_tabs}]
tellraw @s ""

# Copy maps list for iteration
data modify storage {ns}:temp map_menu.list set from storage {ns}:maps {sk}
data modify storage {ns}:temp map_menu.mode set value "{mode_key}"
scoreboard players set #map_menu_idx {ns}.data 0

# Show each map
execute if data storage {ns}:temp map_menu.list[0] run function {ns}:v{version}/maps/editor/menu_entry

# No maps message
execute unless data storage {ns}:maps {sk}[0] run tellraw @s ["  ",{{"text":"No maps created yet.","color":"gray","italic":true}}]

tellraw @s ""
tellraw @s ["  ",{create_btn}]
tellraw @s {sep}
""")

	# Menu Entry (recursive - one map per call) ──────────────────
	write_versioned_function("maps/editor/menu_entry", f"""
# Read current map name and id
data modify storage {ns}:temp map_menu.current set from storage {ns}:temp map_menu.list[0]

# Flatten fields for macro
data modify storage {ns}:temp map_menu.name set from storage {ns}:temp map_menu.current.name
data modify storage {ns}:temp map_menu.id set from storage {ns}:temp map_menu.current.id

# Store current index for macro
execute store result storage {ns}:temp map_menu.idx int 1 run scoreboard players get #map_menu_idx {ns}.data

# Display the entry using macro
function {ns}:v{version}/maps/editor/menu_entry_display with storage {ns}:temp map_menu

# Advance to next
data remove storage {ns}:temp map_menu.list[0]
scoreboard players add #map_menu_idx {ns}.data 1
execute if data storage {ns}:temp map_menu.list[0] run function {ns}:v{version}/maps/editor/menu_entry
""")

	write_versioned_function("maps/editor/menu_entry_display", f"""
$tellraw @s ["  ",{{"text":"$(name)","color":"white"}},{{"text":" ($(id))","color":"gray"}}," ",[{{"text":"[","color":"yellow","click_event":{{"action":"suggest_command","command":"/function {ns}:v{version}/maps/editor/enter {{idx:$(idx),mode:$(mode)}}"}},"hover_event":{{"action":"show_text","value":"Edit this map"}}}},{{"text":"Edit"}},"]"]," ",[{{"text":"[","color":"red","click_event":{{"action":"suggest_command","command":"/function {ns}:v{version}/maps/editor/delete {{idx:$(idx),mode:$(mode)}}"}},"hover_event":{{"action":"show_text","value":"Delete this map"}}}},{{"text":"Delete"}},"]"]]
""")

	# Map Creation (per mode) ────────────────────────────────────
	for mode_key, mode_info in EDITOR_MODES.items():
		sk = mode_info["storage_key"]
		create_snbt = r"id:'my_map',name:'My Map',description:'A new map',base_coordinates:[0,64,0],start_commands:[],respawn_commands:[]"
		back_btn = btn("◀ Back", f"/function {ns}:v{version}/maps/editor/list/{mode_key}", "yellow", "Back to map list")

		write_versioned_function(f"maps/editor/create/{mode_key}", f"""
tellraw @s {sep}
tellraw @s ["","  📝 ",[{{"text":"","color":"gold","bold":true}},{{"text":"Create New {mode_info['name']} Map"}}]]
tellraw @s {sep}
tellraw @s {{"text":"Run this command to create a new map:","color":"yellow"}}
tellraw @s [{{"text":"","color":"aqua","click_event":{{"action":"suggest_command","command":"/data modify storage {ns}:maps {sk} append value {{{create_snbt}}}"}}}},"/data modify storage {ns}:maps {sk} append value {{...}}"]
tellraw @s ["  ",{{"text":"⬆ Click to paste the command, then edit the id/name/description.","color":"gray","italic":true}}]
tellraw @s ""
tellraw @s ["  ",{back_btn}]
tellraw @s {sep}
""")

	# Delete Map (macro with mode) ───────────────────────────────
	write_versioned_function("maps/editor/delete", f"""
$data remove storage {ns}:maps $(mode)[$(idx)]
tellraw @s [{MGS_TAG},{{"text":"Map deleted.","color":"red"}}]

# Refresh menu for the same mode
$function {ns}:v{version}/maps/editor/list/$(mode)
""")

	# Enter Editor Mode (macro with mode+idx) ────────────────────
	mode_score_lines = "\n".join(
		f'execute if data storage {ns}:temp map_edit{{mode:"{mk}"}} run scoreboard players set @s {ns}.mp.map_mode {i}'
		for i, mk in enumerate(MODE_LIST)
	)

	write_versioned_function("maps/editor/enter", f"""
# Store mode and index
$scoreboard players set @s {ns}.mp.map_idx $(idx)
$data modify storage {ns}:temp map_edit.mode set value "$(mode)"

# Set mode score from mode string
{mode_score_lines}

# Mark player as in editor mode
scoreboard players set @s {ns}.mp.map_edit 1
tag @s add {ns}.map_editor

# Set display mode to match save mode
scoreboard players operation @s {ns}.mp.map_disp = @s {ns}.mp.map_mode

# Store index for macro access
execute store result storage {ns}:temp map_edit.idx int 1 run scoreboard players get @s {ns}.mp.map_idx

# Load map data
function {ns}:v{version}/maps/editor/load_map_data with storage {ns}:temp map_edit

# Switch to creative, clear inventory
gamemode creative @s
clear @s

# Load base_coordinates into scores for relative computation
execute store result score #base_x {ns}.data run data get storage {ns}:temp map_edit.map.base_coordinates[0]
execute store result score #base_y {ns}.data run data get storage {ns}:temp map_edit.map.base_coordinates[1]
execute store result score #base_z {ns}.data run data get storage {ns}:temp map_edit.map.base_coordinates[2]

# Teleport to base coordinates
execute store result storage {ns}:temp _tp.x int 1 run scoreboard players get #base_x {ns}.data
execute store result storage {ns}:temp _tp.y int 1 run scoreboard players get #base_y {ns}.data
execute store result storage {ns}:temp _tp.z int 1 run scoreboard players get #base_z {ns}.data
function {ns}:v{version}/shared/tp_to_position with storage {ns}:temp _tp

# Summon markers for existing elements, then build their model displays
function {ns}:v{version}/maps/editor/summon_existing
function {ns}:v{version}/maps/editor/refresh_displays

# Give editor tools (dispatch by mode)
function {ns}:v{version}/maps/editor/give_tools

# Initialize zombies element defaults (only for zombies mode)
execute if score @s {ns}.mp.map_mode matches {MODE_LIST.index("zombies")} run function {ns}:v{version}/maps/editor/init_zb_defaults

# Announce
tellraw @s [{MGS_TAG},{{"text":"Entered map editor for: ","color":"green"}},{{"text":"","color":"white"}},{{"storage":"{ns}:temp","nbt":"map_edit.map.name","interpret":true}}]
tellraw @s [{MGS_TAG},{{"text":"Place eggs to add elements. DESTROY egg (hotbar 9) removes nearest element.","color":"yellow"}}]
tellraw @s [{MGS_TAG},{{"text":"Need collaborators? ","color":"gray"}},{btn("Invite All Players", f"/function {ns}:v{version}/maps/editor/invite_all", "aqua", "Put all online players into this editor session")}]
tellraw @s [{MGS_TAG},{{"text":"Use ","color":"gray"}},{btn("Save & Exit", f"/function {ns}:v{version}/maps/editor/save_exit", "green", "Save changes and exit editor")},{{"text":" or "}},{btn("Exit", f"/function {ns}:v{version}/maps/editor/exit", "red", "Discard changes and exit editor")}]
""")

	write_versioned_function("maps/editor/invite_all", f"""
# Must be called by a player already in editor mode
execute unless score @s {ns}.mp.map_edit matches 1 run return run tellraw @s [{MGS_TAG},{{"text":"You must be in map editor to invite players.","color":"red"}}]

# Share caller's editor session state with everyone not currently editing
scoreboard players set @a {ns}.mp.map_edit 1
scoreboard players operation @a[scores={{{ns}.mp.map_edit=1}}] {ns}.mp.map_idx = @s {ns}.mp.map_idx
scoreboard players operation @a[scores={{{ns}.mp.map_edit=1}}] {ns}.mp.map_mode = @s {ns}.mp.map_mode
scoreboard players operation @a[scores={{{ns}.mp.map_edit=1}}] {ns}.mp.map_disp = @s {ns}.mp.map_disp
tag @a[scores={{{ns}.mp.map_edit=1}}] add {ns}.map_editor

# Put invited players in creative and sync inventory/tools
gamemode creative @a[scores={{{ns}.mp.map_edit=1}}]
clear @a[scores={{{ns}.mp.map_edit=1}}]
execute as @a[scores={{{ns}.mp.map_edit=1}}] run function {ns}:v{version}/maps/editor/give_tools

# Teleport invited players to current base coordinates
execute store result storage {ns}:temp _tp.x int 1 run scoreboard players get #base_x {ns}.data
execute store result storage {ns}:temp _tp.y int 1 run scoreboard players get #base_y {ns}.data
execute store result storage {ns}:temp _tp.z int 1 run scoreboard players get #base_z {ns}.data
execute as @a[scores={{{ns}.mp.map_edit=1}}] run function {ns}:v{version}/shared/tp_to_position with storage {ns}:temp _tp

tellraw @a[scores={{{ns}.mp.map_edit=1}}] [{MGS_TAG},{{"text":"Editor session synced for all players.","color":"aqua"}}]
""")

	write_versioned_function("maps/editor/load_map_data", f"""
$data modify storage {ns}:temp map_edit.map set from storage {ns}:maps $(mode)[$(idx)]
""")

	# Summon Existing Elements ───────────────────────────────────
	summon_dispatch = "\n".join(
		f'execute if score @s {ns}.mp.map_mode matches {i} run function {ns}:v{version}/maps/editor/summon_existing/{mk}'
		for i, mk in enumerate(MODE_LIST)
	)

	write_versioned_function("maps/editor/summon_existing", f"""
# Summon base coordinates marker (common to all modes)
execute store result score #bx {ns}.data run data get storage {ns}:temp map_edit.map.base_coordinates[0]
execute store result score #by {ns}.data run data get storage {ns}:temp map_edit.map.base_coordinates[1]
execute store result score #bz {ns}.data run data get storage {ns}:temp map_edit.map.base_coordinates[2]
execute store result storage {ns}:temp _pos.x double 1 run scoreboard players get #bx {ns}.data
execute store result storage {ns}:temp _pos.y double 1 run scoreboard players get #by {ns}.data
execute store result storage {ns}:temp _pos.z double 1 run scoreboard players get #bz {ns}.data
function {ns}:v{version}/maps/editor/summon_base_marker with storage {ns}:temp _pos

# Restore start_function and tick_function to the base marker from map data
execute if data storage {ns}:temp map_edit.map.start_function run data modify entity @n[tag={ns}.element.base_coordinates] data.start_function set from storage {ns}:temp map_edit.map.start_function
execute if data storage {ns}:temp map_edit.map.tick_function run data modify entity @n[tag={ns}.element.base_coordinates] data.tick_function set from storage {ns}:temp map_edit.map.tick_function

# Mode-specific elements
{summon_dispatch}
""")

	# Per-mode summon functions
	for mode_key, mode_info in EDITOR_MODES.items():
		summon_lines: list[str] = []
		for etype in mode_info["slots"]:
			einfo = ALL_ELEMENTS[etype]
			if einfo["save_type"] in ("base", "config"):
				continue  # handled in parent / no markers
			save_path = einfo["save_path"]
			if einfo["save_type"] == "spawn":
				summon_lines.append(f'data modify storage {ns}:temp _spawn_iter set from storage {ns}:temp map_edit.map.{save_path}')
				summon_lines.append(f'data modify storage {ns}:temp _spawn_iter_tag set value "{ns}.element.{etype}"')
				summon_lines.append(f'execute if data storage {ns}:temp _spawn_iter[0] run function {ns}:v{version}/maps/editor/summon_spawn_iter')
				summon_lines.append("")
			elif einfo["save_type"] == "point":
				summon_lines.append(f'data modify storage {ns}:temp _point_iter set from storage {ns}:temp map_edit.map.{save_path}')
				summon_lines.append(f'data modify storage {ns}:temp _point_iter_tag set value "{ns}.element.{etype}"')
				summon_lines.append(f'execute if data storage {ns}:temp _point_iter[0] run function {ns}:v{version}/maps/editor/summon_point_iter')
				summon_lines.append("")
			elif einfo["save_type"] == "enemy":
				summon_lines.append(f'data modify storage {ns}:temp _enemy_edit_iter set from storage {ns}:temp map_edit.map.{save_path}')
				summon_lines.append(f'execute if data storage {ns}:temp _enemy_edit_iter[0] run function {ns}:v{version}/maps/editor/summon_enemy_edit_iter')
				summon_lines.append("")
			elif einfo["save_type"] == "start_command":
				summon_lines.append(f'data modify storage {ns}:temp _start_cmd_iter set from storage {ns}:temp map_edit.map.{save_path}')
				summon_lines.append(f'execute if data storage {ns}:temp _start_cmd_iter[0] run function {ns}:v{version}/maps/editor/summon_start_command_iter')
				summon_lines.append("")
			elif einfo["save_type"] == "respawn_command":
				summon_lines.append(f'data modify storage {ns}:temp _respawn_cmd_iter set from storage {ns}:temp map_edit.map.{save_path}')
				summon_lines.append(f'execute if data storage {ns}:temp _respawn_cmd_iter[0] run function {ns}:v{version}/maps/editor/summon_respawn_command_iter')
				summon_lines.append("")
			elif einfo["save_type"] == "zb_object":
				summon_lines.append(f'data modify storage {ns}:temp _zb_iter set from storage {ns}:temp map_edit.map.{save_path}')
				summon_lines.append(f'data modify storage {ns}:temp _zb_iter_tag set value "{ns}.element.{etype}"')
				summon_lines.append(f'execute if data storage {ns}:temp _zb_iter[0] run function {ns}:v{version}/maps/editor/summon_zb_object_iter')
				summon_lines.append("")

		write_versioned_function(
			f"maps/editor/summon_existing/{mode_key}",
			"\n".join(summon_lines) if summon_lines else "# No mode-specific elements to summon"
		)

	# Summon helpers (shared) ────────────────────────────────────
	write_versioned_function("maps/editor/summon_base_marker", f"""
$summon minecraft:marker $(x) $(y) $(z) {{Tags:["{ns}.map_element","{ns}.element.base_coordinates"]}}
""")

	# Summon spawn markers - iterates list of [x,y,z,yaw] relative coords
	# Tag is read from {ns}:temp _spawn_iter_tag (set before calling)
	write_versioned_function("maps/editor/summon_spawn_iter", f"""
# Read relative coordinates from first entry
execute store result score #rx {ns}.data run data get storage {ns}:temp _spawn_iter[0][0]
execute store result score #ry {ns}.data run data get storage {ns}:temp _spawn_iter[0][1]
execute store result score #rz {ns}.data run data get storage {ns}:temp _spawn_iter[0][2]

# Add base to get absolute
scoreboard players operation #rx {ns}.data += #base_x {ns}.data
scoreboard players operation #ry {ns}.data += #base_y {ns}.data
scoreboard players operation #rz {ns}.data += #base_z {ns}.data

# Read yaw
data modify storage {ns}:temp _spawn_rot.yaw set from storage {ns}:temp _spawn_iter[0][3]

# Prepare position for macro
execute store result storage {ns}:temp _spos.x double 1 run scoreboard players get #rx {ns}.data
execute store result storage {ns}:temp _spos.y double 1 run scoreboard players get #ry {ns}.data
execute store result storage {ns}:temp _spos.z double 1 run scoreboard players get #rz {ns}.data

# Set tag from stored tag
data modify storage {ns}:temp _spos.tag set from storage {ns}:temp _spawn_iter_tag

# Summon marker with tag
function {ns}:v{version}/maps/editor/summon_spawn_marker with storage {ns}:temp _spos

# Store rotation data on the marker
execute as @n[tag={ns}.new_spawn_marker] run data modify entity @s data.yaw set from storage {ns}:temp _spawn_rot.yaw
tag @e[tag={ns}.new_spawn_marker] remove {ns}.new_spawn_marker

# Advance to next
data remove storage {ns}:temp _spawn_iter[0]
execute if data storage {ns}:temp _spawn_iter[0] run function {ns}:v{version}/maps/editor/summon_spawn_iter
""")

	write_versioned_function("maps/editor/summon_spawn_marker", f"""
$summon minecraft:marker $(x) $(y) $(z) {{Tags:["{ns}.map_element","$(tag)","{ns}.new_spawn_marker"]}}
""")

	# Summon point markers - iterates list of [x,y,z] relative coords
	# Tag is read from {ns}:temp _point_iter_tag (set before calling)
	write_versioned_function("maps/editor/summon_point_iter", f"""
# Read relative coordinates
execute store result score #rx {ns}.data run data get storage {ns}:temp _point_iter[0][0]
execute store result score #ry {ns}.data run data get storage {ns}:temp _point_iter[0][1]
execute store result score #rz {ns}.data run data get storage {ns}:temp _point_iter[0][2]

# Add base
scoreboard players operation #rx {ns}.data += #base_x {ns}.data
scoreboard players operation #ry {ns}.data += #base_y {ns}.data
scoreboard players operation #rz {ns}.data += #base_z {ns}.data

# Prepare position
execute store result storage {ns}:temp _ppos.x double 1 run scoreboard players get #rx {ns}.data
execute store result storage {ns}:temp _ppos.y double 1 run scoreboard players get #ry {ns}.data
execute store result storage {ns}:temp _ppos.z double 1 run scoreboard players get #rz {ns}.data

# Set tag from stored tag
data modify storage {ns}:temp _ppos.tag set from storage {ns}:temp _point_iter_tag

function {ns}:v{version}/maps/editor/summon_point_marker with storage {ns}:temp _ppos

# Advance
data remove storage {ns}:temp _point_iter[0]
execute if data storage {ns}:temp _point_iter[0] run function {ns}:v{version}/maps/editor/summon_point_iter
""")

	write_versioned_function("maps/editor/summon_point_marker", f"""
$summon minecraft:marker $(x) $(y) $(z) {{Tags:["{ns}.map_element","$(tag)"]}}
""")

	# Summon enemy markers - iterates list of {pos:[x,y,z], function:"..."} entries
	write_versioned_function("maps/editor/summon_enemy_edit_iter", f"""
# Read relative position from first entry
execute store result score #rx {ns}.data run data get storage {ns}:temp _enemy_edit_iter[0].pos[0]
execute store result score #ry {ns}.data run data get storage {ns}:temp _enemy_edit_iter[0].pos[1]
execute store result score #rz {ns}.data run data get storage {ns}:temp _enemy_edit_iter[0].pos[2]

# Add base to get absolute
scoreboard players operation #rx {ns}.data += #base_x {ns}.data
scoreboard players operation #ry {ns}.data += #base_y {ns}.data
scoreboard players operation #rz {ns}.data += #base_z {ns}.data

# Prepare position for macro
execute store result storage {ns}:temp _epos.x double 1 run scoreboard players get #rx {ns}.data
execute store result storage {ns}:temp _epos.y double 1 run scoreboard players get #ry {ns}.data
execute store result storage {ns}:temp _epos.z double 1 run scoreboard players get #rz {ns}.data

# Summon marker
function {ns}:v{version}/maps/editor/summon_enemy_marker with storage {ns}:temp _epos

# Store function data on the marker
execute as @n[tag={ns}.new_enemy_marker] run data modify entity @s data.function set from storage {ns}:temp _enemy_edit_iter[0].function
tag @e[tag={ns}.new_enemy_marker] remove {ns}.new_enemy_marker

# Advance to next
data remove storage {ns}:temp _enemy_edit_iter[0]
execute if data storage {ns}:temp _enemy_edit_iter[0] run function {ns}:v{version}/maps/editor/summon_enemy_edit_iter
""")

	write_versioned_function("maps/editor/summon_enemy_marker", f"""
$summon minecraft:marker $(x) $(y) $(z) {{Tags:["{ns}.map_element","{ns}.element.enemy","{ns}.new_enemy_marker"]}}
""")

	# Summon start command markers - iterates list of {pos:[x,y,z], command:"..."} entries
	write_versioned_function("maps/editor/summon_start_command_iter", f"""
# Read relative position from first entry
execute store result score #rx {ns}.data run data get storage {ns}:temp _start_cmd_iter[0].pos[0]
execute store result score #ry {ns}.data run data get storage {ns}:temp _start_cmd_iter[0].pos[1]
execute store result score #rz {ns}.data run data get storage {ns}:temp _start_cmd_iter[0].pos[2]

# Add base to get absolute
scoreboard players operation #rx {ns}.data += #base_x {ns}.data
scoreboard players operation #ry {ns}.data += #base_y {ns}.data
scoreboard players operation #rz {ns}.data += #base_z {ns}.data

# Prepare position for macro
execute store result storage {ns}:temp _cpos.x double 1 run scoreboard players get #rx {ns}.data
execute store result storage {ns}:temp _cpos.y double 1 run scoreboard players get #ry {ns}.data
execute store result storage {ns}:temp _cpos.z double 1 run scoreboard players get #rz {ns}.data

# Summon marker
function {ns}:v{version}/maps/editor/summon_start_command_marker with storage {ns}:temp _cpos

# Store command on marker
execute as @n[tag={ns}.new_start_cmd_marker] run data modify entity @s data.command set from storage {ns}:temp _start_cmd_iter[0].command
tag @e[tag={ns}.new_start_cmd_marker] remove {ns}.new_start_cmd_marker

# Advance to next
data remove storage {ns}:temp _start_cmd_iter[0]
execute if data storage {ns}:temp _start_cmd_iter[0] run function {ns}:v{version}/maps/editor/summon_start_command_iter
""")

	write_versioned_function("maps/editor/summon_start_command_marker", f"""
$summon minecraft:marker $(x) $(y) $(z) {{Tags:["{ns}.map_element","{ns}.element.start_command","{ns}.new_start_cmd_marker"]}}
""")

	# Summon respawn command markers - iterates list of {pos:[x,y,z], command:"..."} entries
	write_versioned_function("maps/editor/summon_respawn_command_iter", f"""
# Read relative position from first entry
execute store result score #rx {ns}.data run data get storage {ns}:temp _respawn_cmd_iter[0].pos[0]
execute store result score #ry {ns}.data run data get storage {ns}:temp _respawn_cmd_iter[0].pos[1]
execute store result score #rz {ns}.data run data get storage {ns}:temp _respawn_cmd_iter[0].pos[2]

# Add base to get absolute
scoreboard players operation #rx {ns}.data += #base_x {ns}.data
scoreboard players operation #ry {ns}.data += #base_y {ns}.data
scoreboard players operation #rz {ns}.data += #base_z {ns}.data

# Prepare position for macro
execute store result storage {ns}:temp _rcpos.x double 1 run scoreboard players get #rx {ns}.data
execute store result storage {ns}:temp _rcpos.y double 1 run scoreboard players get #ry {ns}.data
execute store result storage {ns}:temp _rcpos.z double 1 run scoreboard players get #rz {ns}.data

# Summon marker
function {ns}:v{version}/maps/editor/summon_respawn_command_marker with storage {ns}:temp _rcpos

# Store command on marker
execute as @n[tag={ns}.new_respawn_cmd_marker] run data modify entity @s data.command set from storage {ns}:temp _respawn_cmd_iter[0].command
tag @e[tag={ns}.new_respawn_cmd_marker] remove {ns}.new_respawn_cmd_marker

# Advance to next
data remove storage {ns}:temp _respawn_cmd_iter[0]
execute if data storage {ns}:temp _respawn_cmd_iter[0] run function {ns}:v{version}/maps/editor/summon_respawn_command_iter
""")

	write_versioned_function("maps/editor/summon_respawn_command_marker", f"""
$summon minecraft:marker $(x) $(y) $(z) {{Tags:["{ns}.map_element","{ns}.element.respawn_command","{ns}.new_respawn_cmd_marker"]}}
""")

	# Summon zb_object markers - iterates list of compound objects {pos:[x,y,z], rotation:[yaw,pitch], ...}
	# Tag is read from {ns}:temp _zb_iter_tag (set before calling)
	write_versioned_function("maps/editor/summon_zb_object_iter", f"""
# Read relative position from first entry
execute store result score #rx {ns}.data run data get storage {ns}:temp _zb_iter[0].pos[0]
execute store result score #ry {ns}.data run data get storage {ns}:temp _zb_iter[0].pos[1]
execute store result score #rz {ns}.data run data get storage {ns}:temp _zb_iter[0].pos[2]

# Add base to get absolute
scoreboard players operation #rx {ns}.data += #base_x {ns}.data
scoreboard players operation #ry {ns}.data += #base_y {ns}.data
scoreboard players operation #rz {ns}.data += #base_z {ns}.data

# Prepare position for macro
execute store result storage {ns}:temp _zbpos.x double 1 run scoreboard players get #rx {ns}.data
execute store result storage {ns}:temp _zbpos.y double 1 run scoreboard players get #ry {ns}.data
execute store result storage {ns}:temp _zbpos.z double 1 run scoreboard players get #rz {ns}.data

# Set tag
data modify storage {ns}:temp _zbpos.tag set from storage {ns}:temp _zb_iter_tag

# Summon marker
function {ns}:v{version}/maps/editor/summon_zb_marker with storage {ns}:temp _zbpos

# Copy all compound data onto the marker
execute as @n[tag={ns}.new_zb_marker] run data modify entity @s data set from storage {ns}:temp _zb_iter[0]

# Fill in fields the map predates (config UI would otherwise show a blank row)
execute as @n[tag={ns}.new_zb_marker] run function {ns}:v{version}/maps/editor/backfill_zb_defaults

# Set yaw from rotation for the direction indicator (sync entity Rotation too for model displays)
execute if data storage {ns}:temp _zb_iter[0].rotation as @n[tag={ns}.new_zb_marker] run data modify entity @s data.yaw set from storage {ns}:temp _zb_iter[0].rotation[0]
execute as @n[tag={ns}.new_zb_marker] run data modify entity @s Rotation[0] set from entity @s data.yaw

tag @e[tag={ns}.new_zb_marker] remove {ns}.new_zb_marker

# Advance to next
data remove storage {ns}:temp _zb_iter[0]
execute if data storage {ns}:temp _zb_iter[0] run function {ns}:v{version}/maps/editor/summon_zb_object_iter
""")

	write_versioned_function("maps/editor/summon_zb_marker", f"""
$summon minecraft:marker $(x) $(y) $(z) {{Tags:["{ns}.map_element","$(tag)","{ns}.new_zb_marker"]}}
""")

	# Give Editor Tools (dispatch by mode score) ─────────────────
	destroy_cmd = (
		f'item replace entity @s hotbar.8 with minecraft:bat_spawn_egg'
		f'[minecraft:item_name={{"text":"✘ DESTROY","color":"dark_red","italic":false,"bold":true}},'
		f'minecraft:item_model="minecraft:wither_skeleton_spawn_egg",'
		f'minecraft:custom_data={{{ns}:{{editor:true,type:"destroy"}}}},'
		f'minecraft:entity_data={{id:"minecraft:bat",NoAI:1b,Silent:1b,Invulnerable:1b,Tags:["{ns}.new_element","{ns}.element.destroy"]}}]'
	)

	give_dispatch = "\n".join(
		f'execute if score @s {ns}.mp.map_disp matches {i} run function {ns}:v{version}/maps/editor/give_tools/{mk}'
		for i, mk in enumerate(MODE_LIST)
	)

	save_exit_cmd = (
		f'item replace entity @s inventory.26 with minecraft:bat_spawn_egg'
		f'[minecraft:item_name=["","💾 ",{{"text":"Save & Exit","color":"green","italic":false,"bold":true}}],'
		f'minecraft:item_model="minecraft:turtle_spawn_egg",'
		f'minecraft:custom_data={{{ns}:{{editor:true,type:"editor_save_exit"}}}},'
		f'minecraft:entity_data={{id:"minecraft:bat",NoAI:1b,Silent:1b,Invulnerable:1b,Tags:["{ns}.new_element","{ns}.element.editor_save_exit"]}}]'
	)

	exit_cmd = (
		f'item replace entity @s inventory.25 with minecraft:bat_spawn_egg'
		f'[minecraft:item_name={{"text":"✘ Exit","color":"red","italic":false,"bold":true}},'
		f'minecraft:item_model="minecraft:ghast_spawn_egg",'
		f'minecraft:custom_data={{{ns}:{{editor:true,type:"editor_exit"}}}},'
		f'minecraft:entity_data={{id:"minecraft:bat",NoAI:1b,Silent:1b,Invulnerable:1b,Tags:["{ns}.new_element","{ns}.element.editor_exit"]}}]'
	)

	save_only_cmd = (
		f'item replace entity @s inventory.24 with minecraft:bat_spawn_egg'
		f'[minecraft:item_name=["","💾 ",{{"text":"Save","color":"aqua","italic":false,"bold":true}}],'
		f'minecraft:item_model="minecraft:axolotl_spawn_egg",'
		f'minecraft:custom_data={{{ns}:{{editor:true,type:"editor_save"}}}},'
		f'minecraft:entity_data={{id:"minecraft:bat",NoAI:1b,Silent:1b,Invulnerable:1b,Tags:["{ns}.new_element","{ns}.element.editor_save"]}}]'
	)

	coord_stick_cmd = (
		f'item replace entity @s inventory.23 with minecraft:warped_fungus_on_a_stick'
		f'[minecraft:item_name=["","📐 ",{{"text":"Coord Stick","color":"yellow","italic":false,"bold":true}}],'
		f'minecraft:custom_data={{{ns}:{{coord_stick:true}}}},'
		f'minecraft:item_model="minecraft:stick",'
		f'minecraft:enchantment_glint_override=true]'
	)

	write_versioned_function("maps/editor/give_tools", f"""
# Destroy egg (always in hotbar.8)
{destroy_cmd}

# Utility eggs (bottom-right of inventory)
{save_exit_cmd}
{exit_cmd}
{save_only_cmd}

# Coord stick utility
{coord_stick_cmd}

# Mode-specific eggs
{give_dispatch}
""")

	# Per-mode give_tools
	for mode_key, mode_info in EDITOR_MODES.items():
		egg_cmds: list[str] = []
		for etype, eslot in mode_info["slots"].items():
			einfo = ALL_ELEMENTS[etype]
			egg_cmds.append(
				f'item replace entity @s {eslot} with minecraft:bat_spawn_egg'
				f'[minecraft:item_name={{"text":"{einfo["name"]}","color":"{einfo["color"]}","italic":false}},'
				f'minecraft:item_model="{einfo["egg_model"]}",'
				f'minecraft:custom_data={{{ns}:{{editor:true,type:"{etype}"}}}},'
				f'minecraft:entity_data={{id:"minecraft:bat",NoAI:1b,Silent:1b,Invulnerable:1b,Tags:["{ns}.new_element","{ns}.element.{etype}"]}}]'
			)
		# Zombies mode: add defaults config (hotbar.6) and configure element (hotbar.7) tools
		if mode_key == "zombies":
			egg_cmds.append(
				f'item replace entity @s hotbar.6 with minecraft:bat_spawn_egg'
				f'[minecraft:item_name={{"text":"⚙ Defaults","color":"white","italic":false,"bold":true}},'
				f'minecraft:item_model="minecraft:allay_spawn_egg",'
				f'minecraft:custom_data={{{ns}:{{editor:true,type:"zb_defaults"}}}},'
				f'minecraft:entity_data={{id:"minecraft:bat",NoAI:1b,Silent:1b,Invulnerable:1b,Tags:["{ns}.new_element","{ns}.element.zb_defaults"]}}]'
			)
			egg_cmds.append(
				f'item replace entity @s hotbar.7 with minecraft:bat_spawn_egg'
				f'[minecraft:item_name=["","🔧 ",{{"text":"Configure","color":"aqua","italic":false,"bold":true}}],'
				f'minecraft:item_model="minecraft:breeze_spawn_egg",'
				f'minecraft:custom_data={{{ns}:{{editor:true,type:"zb_configure"}}}},'
				f'minecraft:entity_data={{id:"minecraft:bat",NoAI:1b,Silent:1b,Invulnerable:1b,Tags:["{ns}.new_element","{ns}.element.zb_configure"]}}]'
			)
		write_versioned_function(
			f"maps/editor/give_tools/{mode_key}",
			"\n".join(egg_cmds) if egg_cmds else "# No eggs for this mode"
		)

	# On Place (Advancement Reward) ──────────────────────────────
	write_versioned_function("maps/editor/on_place", f"""
# Revoke advancement immediately so it can trigger again
advancement revoke @s only {ns}:v{version}/maps/editor/on_place

# Only process if player is in editor mode
execute unless score @s {ns}.mp.map_edit matches 1 run return fail

# Find the newly spawned bat entity (tagged by entity_data)
execute as @n[tag={ns}.new_element] at @s run function {ns}:v{version}/maps/editor/process_element
""")

	# Process Placed Element (universal - handles all types) ─────
	process_lines: list[str] = []
	# Destroy handler first
	process_lines.append('# DESTROY handler')
	process_lines.append(f'execute if entity @s[tag={ns}.element.destroy] run function {ns}:v{version}/maps/editor/handle_destroy')
	process_lines.append(f'execute if entity @s[tag={ns}.element.destroy] run return run kill @s')
	process_lines.append("")

	for etype, einfo in ALL_ELEMENTS.items():
		save_type = einfo["save_type"]
		if save_type == "base":
			handler = "handle_base"
		elif save_type == "spawn":
			handler = "handle_spawn"
		elif save_type == "point":
			handler = "handle_point"
		elif save_type == "config":
			handler = "handle_config"
		elif save_type == "enemy":
			handler = "handle_enemy"
		elif save_type == "start_command":
			handler = "handle_start_command"
		elif save_type == "respawn_command":
			handler = "handle_respawn_command"
		elif save_type == "zb_object":
			handler = "handle_zb_object"
		else:
			continue
		process_lines.append(f'execute if entity @s[tag={ns}.element.{etype}] run function {ns}:v{version}/maps/editor/{handler}')
		process_lines.append(f'execute if entity @s[tag={ns}.element.{etype}] run return run kill @s')
		process_lines.append("")

	# Zombies utility tool handlers
	process_lines.append("# Zombies utility tool handlers")
	process_lines.append(f'execute if entity @s[tag={ns}.element.zb_defaults] run function {ns}:v{version}/maps/editor/handle_zb_defaults')
	process_lines.append(f'execute if entity @s[tag={ns}.element.zb_defaults] run return run kill @s')
	process_lines.append(f'execute if entity @s[tag={ns}.element.zb_configure] run function {ns}:v{version}/maps/editor/handle_zb_configure')
	process_lines.append(f'execute if entity @s[tag={ns}.element.zb_configure] run return run kill @s')
	process_lines.append("")

	# Editor utility handlers (save, exit, save & exit)
	process_lines.append("# Editor utility handlers")
	process_lines.append(f'execute if entity @s[tag={ns}.element.editor_save_exit] as @p[tag={ns}.map_editor,distance=..6,sort=nearest] run function {ns}:v{version}/maps/editor/save_exit')
	process_lines.append(f'execute if entity @s[tag={ns}.element.editor_save_exit] run return run kill @s')
	process_lines.append(f'execute if entity @s[tag={ns}.element.editor_exit] as @p[tag={ns}.map_editor,distance=..6,sort=nearest] run function {ns}:v{version}/maps/editor/exit')
	process_lines.append(f'execute if entity @s[tag={ns}.element.editor_exit] run return run kill @s')
	process_lines.append(f'execute if entity @s[tag={ns}.element.editor_save] as @p[tag={ns}.map_editor,distance=..6,sort=nearest] run function {ns}:v{version}/maps/editor/save_only')
	process_lines.append(f'execute if entity @s[tag={ns}.element.editor_save] run return run kill @s')
	process_lines.append("")

	process_lines.append("# Fallback: unknown type")
	process_lines.append("kill @s")

	write_versioned_function("maps/editor/process_element", "\n".join(process_lines))

	# Handle Base Coordinates ────────────────────────────────────
	write_versioned_function("maps/editor/handle_base", f"""
# Preserve start_function and tick_function from existing base marker
execute if data entity @n[tag={ns}.element.base_coordinates] data.start_function run data modify storage {ns}:temp _base_preserve.start_function set from entity @n[tag={ns}.element.base_coordinates] data.start_function
execute if data entity @n[tag={ns}.element.base_coordinates] data.tick_function run data modify storage {ns}:temp _base_preserve.tick_function set from entity @n[tag={ns}.element.base_coordinates] data.tick_function

# Kill any existing base marker
kill @e[tag={ns}.element.base_coordinates]

# Get position
execute store result score #base_x {ns}.data run data get entity @s Pos[0]
execute store result score #base_y {ns}.data run data get entity @s Pos[1]
execute store result score #base_z {ns}.data run data get entity @s Pos[2]

# Summon permanent marker
execute store result storage {ns}:temp _pos.x double 1 run scoreboard players get #base_x {ns}.data
execute store result storage {ns}:temp _pos.y double 1 run scoreboard players get #base_y {ns}.data
execute store result storage {ns}:temp _pos.z double 1 run scoreboard players get #base_z {ns}.data
function {ns}:v{version}/maps/editor/summon_base_marker with storage {ns}:temp _pos

# Restore preserved start_function and tick_function
execute if data storage {ns}:temp _base_preserve.start_function run data modify entity @n[tag={ns}.element.base_coordinates] data.start_function set from storage {ns}:temp _base_preserve.start_function
execute if data storage {ns}:temp _base_preserve.tick_function run data modify entity @n[tag={ns}.element.base_coordinates] data.tick_function set from storage {ns}:temp _base_preserve.tick_function
data remove storage {ns}:temp _base_preserve

# Announce
execute as @a[tag={ns}.map_editor] run tellraw @s [{MGS_TAG},{{"text":"Base coordinates set!","color":"light_purple"}}]
""")

	# Handle Spawn Point (universal) ─────────────────────────────
	spawn_tag_lines = "\n".join(
		f'execute if entity @s[tag={ns}.element.{etype}] run data modify storage {ns}:temp _pos.tag set value "{ns}.element.{etype}"'
		for etype, einfo in ALL_ELEMENTS.items() if einfo["save_type"] == "spawn"
	)
	spawn_msg_lines = "\n".join(
		f'execute if entity @s[tag={ns}.element.{etype}] run tellraw @a[tag={ns}.map_editor] [{MGS_TAG},{{"text":"{einfo["name"]} placed!","color":"{einfo["color"]}"}}]'
		for etype, einfo in ALL_ELEMENTS.items() if einfo["save_type"] == "spawn"
	)

	write_versioned_function("maps/editor/handle_spawn", f"""
# Get position for the permanent marker
execute store result storage {ns}:temp _pos.x double 1 run data get entity @s Pos[0]
execute store result storage {ns}:temp _pos.y double 1 run data get entity @s Pos[1]
execute store result storage {ns}:temp _pos.z double 1 run data get entity @s Pos[2]

# Determine tag from entity
{spawn_tag_lines}

# Summon permanent marker
function {ns}:v{version}/maps/editor/summon_spawn_marker with storage {ns}:temp _pos

# Get player rotation and snap to nearest 45 degrees
execute store result score #yaw {ns}.data run data get entity @p[tag={ns}.map_editor,distance=..6,sort=nearest] Rotation[0]
scoreboard players add #yaw {ns}.data 742
scoreboard players operation #yaw {ns}.data /= #45 {ns}.data
scoreboard players operation #yaw {ns}.data *= #45 {ns}.data
scoreboard players remove #yaw {ns}.data 720
execute as @n[tag={ns}.new_spawn_marker] store result entity @s data.yaw float 1 run scoreboard players get #yaw {ns}.data
tag @n[tag={ns}.new_spawn_marker] remove {ns}.new_spawn_marker

# Announce
{spawn_msg_lines}
""")

	# Handle Point Element (universal) ───────────────────────────
	point_tag_lines = "\n".join(
		f'execute if entity @s[tag={ns}.element.{etype}] run data modify storage {ns}:temp _pos.tag set value "{ns}.element.{etype}"'
		for etype, einfo in ALL_ELEMENTS.items() if einfo["save_type"] == "point"
	)
	point_msg_lines = "\n".join(
		f'execute if entity @s[tag={ns}.element.{etype}] run tellraw @a[tag={ns}.map_editor] [{MGS_TAG},{{"text":"{einfo["name"]} placed!","color":"{einfo["color"]}"}}]'
		for etype, einfo in ALL_ELEMENTS.items() if einfo["save_type"] == "point"
	)

	write_versioned_function("maps/editor/handle_point", f"""
# Get position for permanent marker
execute store result storage {ns}:temp _pos.x double 1 run data get entity @s Pos[0]
execute store result storage {ns}:temp _pos.y double 1 run data get entity @s Pos[1]
execute store result storage {ns}:temp _pos.z double 1 run data get entity @s Pos[2]

# Determine tag
{point_tag_lines}

# Summon permanent marker
function {ns}:v{version}/maps/editor/summon_point_marker with storage {ns}:temp _pos

# Announce
{point_msg_lines}
""")

	# Handle Enemy Element (missions) ────────────────────────────
	write_versioned_function("maps/editor/handle_enemy", f"""
# Initialize default function if missing
execute unless data storage {ns}:temp map_edit.map.default_enemy_function run data modify storage {ns}:temp map_edit.map.default_enemy_function set value "{ns}:mob/default/level_1 {{\\"entity\\":\\"pillager\\"}}"

# Get position for permanent marker
execute store result storage {ns}:temp _pos.x double 1 run data get entity @s Pos[0]
execute store result storage {ns}:temp _pos.y double 1 run data get entity @s Pos[1]
execute store result storage {ns}:temp _pos.z double 1 run data get entity @s Pos[2]

# Summon permanent marker
function {ns}:v{version}/maps/editor/summon_enemy_marker with storage {ns}:temp _pos

# Store the default function on the marker
execute as @n[tag={ns}.new_enemy_marker] run data modify entity @s data.function set from storage {ns}:temp map_edit.map.default_enemy_function
tag @e[tag={ns}.new_enemy_marker] remove {ns}.new_enemy_marker

# Announce
tellraw @a[tag={ns}.map_editor] [{MGS_TAG},{{"text":"Enemy placed!","color":"red"}}]
""")

	# Handle Start Command Element (all modes) ──────────────────
	edit_cmd_btn = btn(
		"Edit Command",
		f'/data modify entity @n[tag={ns}.element.start_command,distance=..10] data.command set value "say Hello from start command"',
		"aqua", "Click to edit the command to run at game start", action="suggest_command"
	)
	write_versioned_function("maps/editor/handle_start_command", f"""
# Get position for permanent marker
execute store result storage {ns}:temp _pos.x double 1 run data get entity @s Pos[0]
execute store result storage {ns}:temp _pos.y double 1 run data get entity @s Pos[1]
execute store result storage {ns}:temp _pos.z double 1 run data get entity @s Pos[2]

# Summon permanent marker
function {ns}:v{version}/maps/editor/summon_start_command_marker with storage {ns}:temp _pos

# Set default command on marker
execute as @n[tag={ns}.new_start_cmd_marker] run data modify entity @s data.command set value "say Hello from start command"
tag @e[tag={ns}.new_start_cmd_marker] remove {ns}.new_start_cmd_marker

# Announce + quick edit helper
tellraw @a[tag={ns}.map_editor] [{MGS_TAG},{{"text":"Start Command placed!","color":"aqua"}}]
tellraw @a[tag={ns}.map_editor] ["  ",{edit_cmd_btn}]
""")

	# Handle Respawn Command Element (multiplayer + missions) ───
	edit_respawn_cmd_btn = btn(
		"Edit Command",
		f'/data modify entity @n[tag={ns}.element.respawn_command,distance=..10] data.command set value "effect give @s minecraft:speed 5 0 true"',
		"dark_aqua", "Click to edit the command to run when players respawn", action="suggest_command"
	)
	write_versioned_function("maps/editor/handle_respawn_command", f"""
# Get position for permanent marker
execute store result storage {ns}:temp _pos.x double 1 run data get entity @s Pos[0]
execute store result storage {ns}:temp _pos.y double 1 run data get entity @s Pos[1]
execute store result storage {ns}:temp _pos.z double 1 run data get entity @s Pos[2]

# Summon permanent marker
function {ns}:v{version}/maps/editor/summon_respawn_command_marker with storage {ns}:temp _pos

# Set default command on marker
execute as @n[tag={ns}.new_respawn_cmd_marker] run data modify entity @s data.command set value "effect give @s minecraft:speed 5 0 true"
tag @e[tag={ns}.new_respawn_cmd_marker] remove {ns}.new_respawn_cmd_marker

# Announce + quick edit helper
tellraw @a[tag={ns}.map_editor] [{MGS_TAG},{{"text":"Respawn Command placed!","color":"dark_aqua"}}]
tellraw @a[tag={ns}.map_editor] ["  ",{edit_respawn_cmd_btn}]
""")

	# Handle ZB Object (zombies compound elements) ───────────────
	# Detect type, copy defaults, get rotation, summon marker with data
	zb_elements = {etype: einfo for etype, einfo in ALL_ELEMENTS.items() if einfo["save_type"] == "zb_object"}

	# Build tag detection lines
	zb_tag_lines: list[str] = []
	for etype in zb_elements:
		zb_tag_lines.append(f'execute if entity @s[tag={ns}.element.{etype}] run data modify storage {ns}:temp _zbpos.tag set value "{ns}.element.{etype}"')
		zb_tag_lines.append(f'execute if entity @s[tag={ns}.element.{etype}] run data modify storage {ns}:temp _zb_new set from storage {ns}:temp map_edit.zb_defaults.{etype}')

	# Build announce lines
	zb_msg_lines: list[str] = []
	for etype, einfo in zb_elements.items():
		zb_msg_lines.append(f'execute if entity @s[tag={ns}.element.{etype}] run tellraw @a[tag={ns}.map_editor] [{MGS_TAG},{{"text":"{einfo["name"]} placed!","color":"{einfo["color"]}"}}]')

	write_versioned_function("maps/editor/handle_zb_object", f"""
# Get position for permanent marker
execute store result storage {ns}:temp _zbpos.x double 1 run data get entity @s Pos[0]
execute store result storage {ns}:temp _zbpos.y double 1 run data get entity @s Pos[1]
execute store result storage {ns}:temp _zbpos.z double 1 run data get entity @s Pos[2]

# Detect type and copy defaults
{chr(10).join(zb_tag_lines)}

# Summon marker
function {ns}:v{version}/maps/editor/summon_zb_marker with storage {ns}:temp _zbpos

# Copy data compound to marker
execute as @n[tag={ns}.new_zb_marker] run data modify entity @s data set from storage {ns}:temp _zb_new

# Apply shared group_id default
execute as @n[tag={ns}.new_zb_marker] run data modify entity @s data.group_id set from storage {ns}:temp map_edit.zb_defaults.group_id

# Get player rotation
execute store result score #yaw {ns}.data run data get entity @p[tag={ns}.map_editor,distance=..6,sort=nearest] Rotation[0]

# Snap yaw: the power switch is mounted on a block face, so it only allows the 4 cardinal facings
# (snap to 90°). Every other zb_object snaps to the nearest 45°. (742 = 720 + 45/2 and 765 = 720 + 90/2
# offset the value positive for rounding; 720 is a multiple of both 45 and 90 and is removed again after.)
execute unless entity @s[tag={ns}.element.power_switch] run scoreboard players add #yaw {ns}.data 742
execute unless entity @s[tag={ns}.element.power_switch] run scoreboard players operation #yaw {ns}.data /= #45 {ns}.data
execute unless entity @s[tag={ns}.element.power_switch] run scoreboard players operation #yaw {ns}.data *= #45 {ns}.data
execute if entity @s[tag={ns}.element.power_switch] run scoreboard players add #yaw {ns}.data 765
execute if entity @s[tag={ns}.element.power_switch] run scoreboard players operation #yaw {ns}.data /= #90 {ns}.data
execute if entity @s[tag={ns}.element.power_switch] run scoreboard players operation #yaw {ns}.data *= #90 {ns}.data
scoreboard players remove #yaw {ns}.data 720

# Apply 180° yaw offset
scoreboard players add #yaw {ns}.data 180

# Store yaw on marker (and sync entity Rotation immediately so the model display below is oriented right away)
execute as @n[tag={ns}.new_zb_marker] store result entity @s data.yaw float 1 run scoreboard players get #yaw {ns}.data
execute as @n[tag={ns}.new_zb_marker] run data modify entity @s Rotation[0] set from entity @s data.yaw

# For doors: capture block from player's offhand (required)
execute if entity @s[tag={ns}.element.door] as @p[tag={ns}.map_editor,distance=..6,sort=nearest] run data modify storage {ns}:temp _zb_offhand_block set from entity @s equipment.offhand.id
execute if entity @s[tag={ns}.element.door] unless data storage {ns}:temp _zb_offhand_block run tellraw @a[tag={ns}.map_editor] [{MGS_TAG},"⚠ ",{{"text":"Door cancelled! Hold a block in offhand.","color":"red"}}]
execute if entity @s[tag={ns}.element.door] unless data storage {ns}:temp _zb_offhand_block run kill @e[tag={ns}.new_zb_marker]
execute if entity @s[tag={ns}.element.door] unless data storage {ns}:temp _zb_offhand_block run return fail
execute if entity @s[tag={ns}.element.door] as @n[tag={ns}.new_zb_marker] run data modify entity @s data.block set from storage {ns}:temp _zb_offhand_block
data remove storage {ns}:temp _zb_offhand_block

tag @e[tag={ns}.new_zb_marker] remove {ns}.new_zb_marker

# Refresh model displays right away (wallbuy/perk/pap/mystery box/power switch)
function {ns}:v{version}/maps/editor/refresh_displays

# Announce
{chr(10).join(zb_msg_lines)}
""")

	# Handle DESTROY ─────────────────────────────────────────────
	write_versioned_function("maps/editor/handle_destroy", f"""
# Find the nearest map element marker (within 3 blocks)
execute at @s unless entity @n[tag={ns}.map_element,distance=..3] run tellraw @a[tag={ns}.map_editor] [{MGS_TAG},{{"text":"No element found within 3 blocks!","color":"red"}}]
execute at @s as @n[tag={ns}.map_element,distance=..3] run function {ns}:v{version}/maps/editor/destroy_element

# Refresh model displays so a destroyed machine's model disappears right away
function {ns}:v{version}/maps/editor/refresh_displays
""")

	# Destroy Element (universal) ────────────────────────────────
	destroy_msg_lines = "\n".join(
		f'execute if entity @s[tag={ns}.element.{etype}] run tellraw @a[tag={ns}.map_editor] [{MGS_TAG},{{"text":"{einfo["name"]} removed!","color":"{einfo["color"]}"}}]'
		for etype, einfo in ALL_ELEMENTS.items() if einfo["save_type"] != "config"
	)

	write_versioned_function("maps/editor/destroy_element", f"""
# @s = the map_element marker to destroy
# Announce what was removed
{destroy_msg_lines}

# Show data dump if element has compound data (zb_object, enemy, spawn)
execute if data entity @s data run tellraw @a[tag={ns}.map_editor] ["  ",{{"text":"Data: ","color":"gray"}},{{"entity":"@s","nbt":"data","color":"white"}}]

# Kill the marker
kill @s
""")

	# Handle Config (missions utility) ───────────────────────────
	config_target = f"@p[tag={ns}.map_editor,distance=..6,sort=nearest]"
	config_lines: list[str] = []
	config_lines.append("# Initialize default enemy function if missing")
	config_lines.append(f'execute unless data storage {ns}:temp map_edit.map.default_enemy_function run data modify storage {ns}:temp map_edit.map.default_enemy_function set value "{ns}:mob/default/level_1 {{\\"entity\\":\\"pillager\\"}}"')
	config_lines.append("")
	config_lines.append(f"tellraw {config_target} {sep}")
	config_lines.append(f'tellraw {config_target} [{{"text":"","color":"white","bold":true}},"  ⚙ ",{{"text":"Enemy Configuration"}}]')
	config_lines.append(f"tellraw {config_target} {sep}")
	config_lines.append(
		f'tellraw {config_target} '
		f'["  ",{{"text":"Default Function: ","color":"gray"}},'
		f'{{"storage":"{ns}:temp","nbt":"map_edit.map.default_enemy_function","color":"white"}}]'
	)
	config_lines.append(f'data modify storage {ns}:temp _cfg.default_fn set from storage {ns}:temp map_edit.map.default_enemy_function')
	config_lines.append(f'function {ns}:v{version}/maps/editor/handle_config_default_btn with storage {ns}:temp _cfg')
	config_lines.append(f'tellraw {config_target} ["  ",{{"text":"ℹ Edit the function path above, then run the command.","color":"dark_gray","italic":true}}]')  # noqa: RUF001
	config_lines.append("")

	# Show nearest configurable elements that can use the default function.
	for etype, einfo in ALL_ELEMENTS.items():
		if not cast(bool, einfo.get("config_uses_default_function", False)):
			continue
		config_lines.append(f'execute if entity @e[tag={ns}.element.{etype},distance=..10] run data modify storage {ns}:temp _cfg.default_fn set from storage {ns}:temp map_edit.map.default_enemy_function')
		config_lines.append(f'execute if entity @e[tag={ns}.element.{etype},distance=..10] run data modify storage {ns}:temp _cfg.nearest_fn set from entity @n[tag={ns}.element.{etype},distance=..10] data.function')
		config_lines.append(f'execute if entity @e[tag={ns}.element.{etype},distance=..10] run function {ns}:v{version}/maps/editor/handle_config_nearest_{etype}_btn with storage {ns}:temp _cfg')

	# Show nearest command-based mission objects.
	for etype in ("start_command", "respawn_command"):
		einfo = ALL_ELEMENTS[etype]
		config_lines.append(f'execute if entity @e[tag={ns}.element.{etype},distance=..10] run data modify storage {ns}:temp _cfg.nearest_cmd set from entity @n[tag={ns}.element.{etype},distance=..10] data.command')
		config_lines.append(f'execute if entity @e[tag={ns}.element.{etype},distance=..10] run function {ns}:v{version}/maps/editor/handle_config_nearest_{etype}_btn with storage {ns}:temp _cfg')

	config_lines.append(f"tellraw {config_target} {sep}")

	write_versioned_function("maps/editor/handle_config", "\n".join(config_lines))

	write_versioned_function("maps/editor/handle_config_default_btn", f"""
$tellraw {config_target} ["    ",{{"text":"[Edit Function]","color":"aqua","click_event":{{"action":"suggest_command","command":"/data modify storage {ns}:temp map_edit.map.default_enemy_function set value \\"$(default_fn)\\""}},"hover_event":{{"action":"show_text","value":"Click to edit the default spawn function for new enemies"}}}}]
""")

	for etype, einfo in ALL_ELEMENTS.items():
		if not cast(bool, einfo.get("config_uses_default_function", False)):
			continue
		write_versioned_function(f"maps/editor/handle_config_nearest_{etype}_btn", f"""
tellraw {config_target} {sep}
tellraw {config_target} ["  ",{{"text":"Nearest {einfo["name"]}: ","color":"yellow","bold":true}},{{"entity":"@n[tag={ns}.element.{etype},distance=..10]","nbt":"data.function","color":"white"}}]
$tellraw {config_target} ["    ",{{"text":"[Edit Nearest {einfo["name"]}]","color":"yellow","click_event":{{"action":"suggest_command","command":"/data modify entity @n[tag={ns}.element.{etype},distance=..10] data.function set value \\"$(nearest_fn)\\""}},"hover_event":{{"action":"show_text","value":"Edit nearest {einfo["name"].lower()} using its current function"}}}}]
""")

	for etype in ("start_command", "respawn_command"):
		einfo = ALL_ELEMENTS[etype]
		write_versioned_function(f"maps/editor/handle_config_nearest_{etype}_btn", f"""
tellraw {config_target} {sep}
tellraw {config_target} ["  ",{{"text":"Nearest {einfo["name"]}: ","color":"yellow","bold":true}},{{"entity":"@n[tag={ns}.element.{etype},distance=..10]","nbt":"data.command","color":"white"}}]
$tellraw {config_target} ["    ",{{"text":"[Edit Nearest {einfo["name"]}]","color":"yellow","click_event":{{"action":"suggest_command","command":"/data modify entity @n[tag={ns}.element.{etype},distance=..10] data.command set value \\"$(nearest_cmd)\\""}},"hover_event":{{"action":"show_text","value":"Edit nearest {einfo["name"].lower()} command using its current value"}}}}]
""")

	# Handle ZB Defaults (configure defaults for new zombies elements)
	def snbt_suggest(val: Any) -> str:
		"""Format a Python value as SNBT for MC commands."""
		if isinstance(val, bool):
			return "1b" if val else "0b"
		elif isinstance(val, int):
			return str(val)
		elif isinstance(val, float):
			return f"{val}f"
		elif isinstance(val, str):
			return f'"{val}"'
		elif isinstance(val, list):
			return "[" + ",".join(snbt_suggest(v) for v in cast(list[Any], val)) + "]"
		elif isinstance(val, dict):
			return "{" + ",".join(f"{k}:{snbt_suggest(v)}" for k, v in cast(dict[str, Any], val).items()) + "}"
		return str(val)
	def snbt_compound(d: JsonDict) -> str:
		"""Convert a Python dict to an SNBT compound string."""
		return "{" + ",".join(f"{k}:{snbt_suggest(v)}" for k, v in d.items()) + "}"

	zb_defaults_lines: list[str] = []
	zb_defaults_lines.append(f"tellraw @a[tag={ns}.map_editor] {sep}")
	zb_defaults_lines.append(f'tellraw @a[tag={ns}.map_editor] [{{"text":"","color":"white","bold":true}},"  ⚙ ",{{"text":"Zombies Element Defaults"}}]')
	zb_defaults_lines.append(f'tellraw @a[tag={ns}.map_editor] ["  ",{{"text":"New elements use these values on placement","color":"gray","italic":true}}]')
	zb_defaults_lines.append(f"tellraw @a[tag={ns}.map_editor] {sep}")
	zb_defaults_lines.append("")

	# Shared group_id default
	group_id_btn = btn(
		"\u270e",
		f"/data modify storage {ns}:temp map_edit.zb_defaults.group_id set value 0",
		"aqua", "Click to edit group_id", action="suggest_command"
	)
	zb_defaults_lines.append(
		f'tellraw @a[tag={ns}.map_editor] '
		f'["  ",{{"text":"group_id: ","color":"gray"}},'
		f'{{"storage":"{ns}:temp","nbt":"map_edit.zb_defaults.group_id","color":"white"}}," ",{group_id_btn}]'
	)
	zb_defaults_lines.append(f'tellraw @a[tag={ns}.map_editor] ["  ",{{"text":"Applies to Zombie Spawn & Player Spawn.","color":"dark_gray","italic":true}}]')
	zb_defaults_lines.append("")

	for etype, einfo in zb_elements.items():
		if not einfo["defaults"]:
			continue  # Skip elements with no type-specific defaults
		zb_defaults_lines.append(
			f'tellraw @a[tag={ns}.map_editor] ["  ","{einfo["emoji"]} ",{{"text":"{einfo["name"]}","color":"{einfo["color"]}","bold":true}}]'
		)
		for field, default_val in einfo["defaults"].items():
			snbt_val = snbt_suggest(default_val)
			edit_btn = btn(
				"✎",
				f"/data modify storage {ns}:temp map_edit.zb_defaults.{etype}.{field} set value {snbt_val}",
				"aqua", f"Click to edit {field}", action="suggest_command"
			)
			zb_defaults_lines.append(
				f'tellraw @a[tag={ns}.map_editor] '
				f'["    ",{{"text":"{field}: ","color":"gray"}},'
				f'{{"storage":"{ns}:temp","nbt":"map_edit.zb_defaults.{etype}.{field}","color":"white"}}," ",{edit_btn}]'
			)
		zb_defaults_lines.append("")

	zb_defaults_lines.append(f"tellraw @a[tag={ns}.map_editor] {sep}")

	write_versioned_function("maps/editor/handle_zb_defaults", "\n".join(zb_defaults_lines))

	# Init ZB Defaults (called on editor enter for zombies mode) ─
	init_defaults_lines: list[str] = []
	init_defaults_lines.append(f'data modify storage {ns}:temp map_edit.zb_defaults.group_id set value 0')
	for etype, einfo in zb_elements.items():
		compound = snbt_compound(einfo["defaults"])
		init_defaults_lines.append(f'data modify storage {ns}:temp map_edit.zb_defaults.{etype} set value {compound}')

	write_versioned_function("maps/editor/init_zb_defaults", "\n".join(init_defaults_lines))

	# Handle ZB Configure (configure nearest element) ────────────
	write_versioned_function("maps/editor/handle_zb_configure", f"""
# Find the nearest map element marker (within 10 blocks)
execute at @s as @n[tag={ns}.map_element,distance=..10] run function {ns}:v{version}/maps/editor/show_element_config
execute at @s unless entity @n[tag={ns}.map_element,distance=..10] run tellraw @a[tag={ns}.map_editor] [{MGS_TAG},{{"text":"No element found within 10 blocks!","color":"red"}}]
""")

	# show_element_config: runs as the nearest marker, shows type-specific fields
	zb_config_lines: list[str] = []
	zb_config_lines.append(f"tellraw @a[tag={ns}.map_editor] {sep}")

	# For each zb_object type, show its fields
	for etype, einfo in zb_elements.items():
		zb_config_lines.append(
			f'execute if entity @s[tag={ns}.element.{etype}] run tellraw @a[tag={ns}.map_editor] '
			f'["  ","{einfo["emoji"]} ",{{"text":"{einfo["name"]} Configuration","color":"{einfo["color"]}","bold":true}}]'
		)
		# group_id only shown for spawn-type zombies elements. Doors don't carry a separate
		# group_id: a door's link_id is its front-room group, and back_group_id is the back room.
		if etype in ("zombie_spawn", "player_spawn_zb", "special_spawn"):
			group_id_edit_btn = btn(
				"✎",
				f"/data modify entity @n[tag={ns}.element.{etype},distance=..10] data.group_id set value 0",
				"yellow", "Click to edit group_id", action="suggest_command"
			)
			zb_config_lines.append(
				f'execute if entity @s[tag={ns}.element.{etype}] run tellraw @a[tag={ns}.map_editor] '
				f'["    ",{{"text":"group_id: ","color":"gray"}},'
				f'{{"entity":"@s","nbt":"data.group_id","color":"white"}}," ",{group_id_edit_btn}]'
			)
		for field, default_val in einfo["defaults"].items():
			snbt_val = snbt_suggest(default_val)
			# Edit button suggests the current default value; optional list fields suggest a
			# usable template instead of empty brackets so they're easy to fill in.
			edit_value = snbt_val
			if field == "activation_box":
				edit_value = "[0, 0, 0, 5, 3, 5]"
			# Door fields (except link_id) use propagation to all doors with same link_id.
			if etype == "door" and field != "link_id":
				# Two entry points, not eight: a macro cannot re-quote its argument, so the string
				# fields and the numeric fields need one variant each.
				kind: str = "text" if isinstance(default_val, str) else "number"
				edit_cmd = f'/function {ns}:v{version}/maps/editor/set_door_link_{kind} {{field:"{field}",value:{snbt_val}}}'
				hover_text = f"Sets {field} on ALL doors with same link_id"
			else:
				edit_cmd = f"/data modify entity @n[tag={ns}.element.{etype},distance=..10] data.{field} set value {edit_value}"
				hover_text = f"Click to edit {field}"
			edit_btn = btn(
				"✎",
				edit_cmd,
				"yellow", hover_text, action="suggest_command"
			)
			# Optional list fields get a "✗" button to clear/disable them (set back to []).
			clear_component: str = ""
			if field == "activation_box":
				clear_btn = btn(
					"✗",
					f"/data modify entity @n[tag={ns}.element.{etype},distance=..10] data.{field} set value []",
					"red", "Clear (disable) the activation box", action="run_command"
				)
				clear_component = f'," ",{clear_btn}'
			# Optional info tooltip for constant/enum fields (e.g. trap type, door animation).
			doc: str | None = FIELD_DOCS.get((etype, field)) or FIELD_DOCS.get(field)
			info_component: str = ""
			if doc:
				doc_escaped = doc.replace("\\", "\\\\").replace('"', '\\"').replace("\n", "\\n")
				info_component = f',"  ",{{"text":"ⓘ","color":"aqua","hover_event":{{"action":"show_text","value":"{doc_escaped}"}}}}'
			zb_config_lines.append(
				f'execute if entity @s[tag={ns}.element.{etype}] run tellraw @a[tag={ns}.map_editor] '
				f'["    ",{{"text":"{field}: ","color":"gray"}},'
				f'{{"entity":"@s","nbt":"data.{field}","color":"white"}}," ",{edit_btn}{clear_component}{info_component}]'
			)

	# Backfill missing config fields on markers summoned from an already-saved map, so a field added
	# to `defaults` after the map was written shows its default in the config UI instead of a blank
	# row (e.g. partial_price on doors/perk machines). Absent-only: never touches a set value.
	backfill_lines: list[str] = []
	for etype, einfo in zb_elements.items():
		for field, default_val in einfo["defaults"].items():
			backfill_lines.append(
				f"execute if entity @s[tag={ns}.element.{etype}] unless data entity @s data.{field} "
				f"run data modify entity @s data.{field} set value {snbt_suggest(default_val)}"
			)
	write_versioned_function("maps/editor/backfill_zb_defaults", "\n".join(backfill_lines))

	# For spawn types: show yaw
	for etype, einfo in ALL_ELEMENTS.items():
		if einfo["save_type"] != "spawn":
			continue
		edit_yaw_btn = btn(
			"✎",
			f"/data modify entity @n[tag={ns}.element.{etype},distance=..10] data.yaw set value 0.0f",
			"yellow", "Click to edit yaw", action="suggest_command"
		)
		zb_config_lines.append(
			f'execute if entity @s[tag={ns}.element.{etype}] run tellraw @a[tag={ns}.map_editor] '
			f'["  ","{einfo["emoji"]} ",{{"text":"{einfo["name"]}","color":"{einfo["color"]}","bold":true}}]'
		)
		zb_config_lines.append(
			f'execute if entity @s[tag={ns}.element.{etype}] run tellraw @a[tag={ns}.map_editor] '
			f'["    ",{{"text":"yaw: ","color":"gray"}},'
			f'{{"entity":"@s","nbt":"data.yaw","color":"white"}}," ",{edit_yaw_btn}]'
		)

	# For zb_object types: show yaw (rotation)
	for etype, _ in zb_elements.items():
		edit_yaw_btn = btn(
			"✎",
			f"/data modify entity @n[tag={ns}.element.{etype},distance=..10] data.yaw set value 0.0f",
			"yellow", "Click to edit yaw", action="suggest_command"
		)
		zb_config_lines.append(
			f'execute if entity @s[tag={ns}.element.{etype}] run tellraw @a[tag={ns}.map_editor] '
			f'["    ",{{"text":"yaw: ","color":"gray"}},'
			f'{{"entity":"@s","nbt":"data.yaw","color":"white"}}," ",{edit_yaw_btn}]'
		)

	# For enemy types: show function. The suggestion must stay version-independent like the map
	# default above, or a map saved today calls a path that a later pack version no longer ships.
	edit_fn_btn = btn(
		"✎",
		f"/data modify entity @n[tag={ns}.element.enemy,distance=..10] data.function set value '{ns}:mob/default/level_1'",
		"yellow", "Click to edit function", action="suggest_command"
	)
	zb_config_lines.append(
		f'execute if entity @s[tag={ns}.element.enemy] run tellraw @a[tag={ns}.map_editor] '
		f'["  ","👤 ",{{"text":"Enemy Configuration","color":"red","bold":true}}]'
	)
	zb_config_lines.append(
		f'execute if entity @s[tag={ns}.element.enemy] run tellraw @a[tag={ns}.map_editor] '
		f'["    ",{{"text":"function: ","color":"gray"}},'
		f'{{"entity":"@s","nbt":"data.function","color":"white"}}," ",{edit_fn_btn}]'
	)

	# For point types: no configurable fields
	for etype, einfo in ALL_ELEMENTS.items():
		if einfo["save_type"] != "point":
			continue
		zb_config_lines.append(
			f'execute if entity @s[tag={ns}.element.{etype}] run tellraw @a[tag={ns}.map_editor] '
			f'["  ","{einfo["emoji"]} ",{{"text":"{einfo["name"]} — no configurable fields","color":"gray","italic":true}}]'
		)

	# For base_coordinates: show start_function and tick_function
	edit_start_fn_btn = btn(
		"✎",
		f'/data modify entity @n[tag={ns}.element.base_coordinates,distance=..10] data.start_function set value "namespace:path/to/function"',
		"yellow", "Click to edit start_function (called once when game starts)", action="suggest_command"
	)
	clear_start_fn_btn = btn(
		"✗",
		f'/data remove entity @n[tag={ns}.element.base_coordinates,distance=..10] data.start_function',
		"red", "Clear start_function (won't be called)", action="run_command"
	)
	edit_tick_fn_btn = btn(
		"✎",
		f'/data modify entity @n[tag={ns}.element.base_coordinates,distance=..10] data.tick_function set value "namespace:path/to/function"',
		"yellow", "Click to edit tick_function (called every game tick)", action="suggest_command"
	)
	clear_tick_fn_btn = btn(
		"✗",
		f'/data remove entity @n[tag={ns}.element.base_coordinates,distance=..10] data.tick_function',
		"red", "Clear tick_function (won't be called)", action="run_command"
	)
	zb_config_lines.append(
		f'execute if entity @s[tag={ns}.element.base_coordinates] run tellraw @a[tag={ns}.map_editor] '
		f'["  ","⬟ ",{{"text":"Base Coordinates Configuration","color":"light_purple","bold":true}}]'
	)
	zb_config_lines.append(
		f'execute if entity @s[tag={ns}.element.base_coordinates] run tellraw @a[tag={ns}.map_editor] '
		f'["    ",{{"text":"start_function: ","color":"gray"}},{{"entity":"@s","nbt":"data.start_function","color":"white"}}," ",{edit_start_fn_btn}," ",{clear_start_fn_btn}]'
	)
	zb_config_lines.append(
		f'execute if entity @s[tag={ns}.element.base_coordinates] run tellraw @a[tag={ns}.map_editor] '
		f'["    ",{{"text":"tick_function: ","color":"gray"}},{{"entity":"@s","nbt":"data.tick_function","color":"white"}}," ",{edit_tick_fn_btn}," ",{clear_tick_fn_btn}]'
	)
	zb_config_lines.append(
		f'execute if entity @s[tag={ns}.element.base_coordinates] run tellraw @a[tag={ns}.map_editor] '
		f'["    ","💎 ",{{"text":"start_function is called once when the game starts, tick_function every game tick.","color":"dark_gray","italic":true}}]'
	)

	zb_config_lines.append(f"tellraw @a[tag={ns}.map_editor] {sep}")

	write_versioned_function("maps/editor/show_element_config", "\n".join(zb_config_lines))

	# Door Link Propagation (set selected field on all doors with same link_id)
	write_versioned_function("maps/editor/set_door_link_apply", f"""
execute unless entity @n[tag={ns}.element.door,distance=..10] run return run tellraw @a[tag={ns}.map_editor] [{MGS_TAG},{{"text":"No door found within 10 blocks!","color":"red"}}]
execute store result score #link_id {ns}.data run data get entity @n[tag={ns}.element.door,distance=..10] data.link_id
execute as @e[tag={ns}.element.door] run function {ns}:v{version}/maps/editor/door_set_if_match
tellraw @a[tag={ns}.map_editor] [{MGS_TAG},{{"text":"Updated ","color":"green"}},{{"storage":"{ns}:temp","nbt":"_door_set.field","color":"yellow"}},{{"text":" for all doors with matching link_id","color":"green"}}]
""")

	write_versioned_function("maps/editor/door_set_if_match", f"""
execute store result score #check {ns}.data run data get entity @s data.link_id
execute if score #check {ns}.data = #link_id {ns}.data run function {ns}:v{version}/maps/editor/door_apply_field with storage {ns}:temp _door_set
""")

	write_versioned_function("maps/editor/door_apply_field", f"""
$data modify entity @s data.$(field) set from storage {ns}:temp _door_set.value
""")

	## Entry points for the door config buttons (macro: field, value)
	write_versioned_function("maps/editor/set_door_link_text", f"""
$data modify storage {ns}:temp _door_set set value {{field:"$(field)",value:"$(value)"}}
function {ns}:v{version}/maps/editor/set_door_link_apply
""")

	write_versioned_function("maps/editor/set_door_link_number", f"""
$data modify storage {ns}:temp _door_set set value {{field:"$(field)",value:$(value)}}
function {ns}:v{version}/maps/editor/set_door_link_apply
""")

	# Save and Exit Editor
	save_dispatch = "\n".join(
		f'execute if score @s {ns}.mp.map_mode matches {i} run function {ns}:v{version}/maps/editor/save_lists/{mk}'
		for i, mk in enumerate(MODE_LIST)
	)

	write_versioned_function("maps/editor/save_exit", f"""
# Only process if in editor mode
execute unless score @s {ns}.mp.map_edit matches 1 run return fail

# Do the actual save
function {ns}:v{version}/maps/editor/do_save

# Cleanup and exit
function {ns}:v{version}/maps/editor/cleanup
tellraw @s [{MGS_TAG},{{"text":"Map saved and editor closed!","color":"green"}}]
""")

	write_versioned_function("maps/editor/save_only", f"""
# Only process if in editor mode
execute unless score @s {ns}.mp.map_edit matches 1 run return fail

# Do the actual save
function {ns}:v{version}/maps/editor/do_save

# Re-give tools (since save clears + re-gives via advancement revoke)
function {ns}:v{version}/maps/editor/give_tools

tellraw @s [{MGS_TAG},{{"text":"Map saved!","color":"green"}}]
""")

	write_versioned_function("maps/editor/do_save", f"""
# Preserve session-modified default enemy function before reloading
data modify storage {ns}:temp _session_enemy_fn set from storage {ns}:temp map_edit.map.default_enemy_function

# Reload map data (preserves metadata like id, name, description, scripts)
execute store result storage {ns}:temp map_edit.idx int 1 run scoreboard players get @s {ns}.mp.map_idx
function {ns}:v{version}/maps/editor/load_map_data with storage {ns}:temp map_edit

# Restore session-modified default enemy function
execute if data storage {ns}:temp _session_enemy_fn run data modify storage {ns}:temp map_edit.map.default_enemy_function set from storage {ns}:temp _session_enemy_fn
data remove storage {ns}:temp _session_enemy_fn

# Rebuild base_coordinates from marker
execute as @n[tag={ns}.element.base_coordinates] at @s run function {ns}:v{version}/maps/editor/save_base

# Load base scores for relative computation
execute store result score #base_x {ns}.data run data get storage {ns}:temp map_edit.map.base_coordinates[0]
execute store result score #base_y {ns}.data run data get storage {ns}:temp map_edit.map.base_coordinates[1]
execute store result score #base_z {ns}.data run data get storage {ns}:temp map_edit.map.base_coordinates[2]

# Save mode-specific lists (reset + rebuild from markers)
{save_dispatch}

# Write back to storage
function {ns}:v{version}/maps/editor/write_back with storage {ns}:temp map_edit
""")

	# Per-mode save lists functions
	for mode_key, mode_info in EDITOR_MODES.items():
		reset_lines: list[str] = []
		rebuild_lines: list[str] = []
		for etype in mode_info["slots"]:
			einfo = ALL_ELEMENTS[etype]
			if einfo["save_type"] in ("base", "config"):
				continue  # handled by save_base / no save data

			save_path = einfo["save_path"]
			if einfo["save_type"] == "spawn":
				reset_lines.append(f'data modify storage {ns}:temp map_edit.map.{save_path} set value []')
				path_suffix = save_path.split(".")[-1]
				rebuild_lines.append(f'execute as @e[tag={ns}.element.{etype}] at @s run function {ns}:v{version}/maps/editor/save_spawn {{path:"{path_suffix}"}}')
			elif einfo["save_type"] == "point":
				reset_lines.append(f'data modify storage {ns}:temp map_edit.map.{save_path} set value []')
				rebuild_lines.append(f'execute as @e[tag={ns}.element.{etype}] at @s run function {ns}:v{version}/maps/editor/save_point {{path:"{save_path}"}}')
			elif einfo["save_type"] == "enemy":
				reset_lines.append(f'data modify storage {ns}:temp map_edit.map.{save_path} set value []')
				rebuild_lines.append(f'execute as @e[tag={ns}.element.{etype}] at @s run function {ns}:v{version}/maps/editor/save_enemy')
			elif einfo["save_type"] == "start_command":
				reset_lines.append(f'data modify storage {ns}:temp map_edit.map.{save_path} set value []')
				rebuild_lines.append(f'execute as @e[tag={ns}.element.{etype}] at @s run function {ns}:v{version}/maps/editor/save_start_command {{path:"{save_path}"}}')
			elif einfo["save_type"] == "respawn_command":
				reset_lines.append(f'data modify storage {ns}:temp map_edit.map.{save_path} set value []')
				rebuild_lines.append(f'execute as @e[tag={ns}.element.{etype}] at @s run function {ns}:v{version}/maps/editor/save_respawn_command {{path:"{save_path}"}}')
			elif einfo["save_type"] == "zb_object":
				reset_lines.append(f'data modify storage {ns}:temp map_edit.map.{save_path} set value []')
				rebuild_lines.append(f'execute as @e[tag={ns}.element.{etype}] at @s run function {ns}:v{version}/maps/editor/save_zb_object {{path:"{save_path}"}}')
		all_lines: list[str] = []
		if reset_lines:
			all_lines.append("# Reset lists")
			all_lines.extend(reset_lines)
			all_lines.append("")
			all_lines.append("# Rebuild from markers")
			all_lines.extend(rebuild_lines)

		write_versioned_function(
			f"maps/editor/save_lists/{mode_key}",
			"\n".join(all_lines) if all_lines else "# No mode-specific elements to save"
		)

	## Save base coordinates from marker
	write_versioned_function("maps/editor/save_base", f"""
# @s = base_coordinates marker, at its position
execute store result storage {ns}:temp map_edit.map.base_coordinates[0] int 1 run data get entity @s Pos[0]
execute store result storage {ns}:temp map_edit.map.base_coordinates[1] int 1 run data get entity @s Pos[1]
execute store result storage {ns}:temp map_edit.map.base_coordinates[2] int 1 run data get entity @s Pos[2]

# Save start_function and tick_function (absent by default, only written if set on marker)
execute if data entity @s data.start_function run data modify storage {ns}:temp map_edit.map.start_function set from entity @s data.start_function
execute unless data entity @s data.start_function run data remove storage {ns}:temp map_edit.map.start_function
execute if data entity @s data.tick_function run data modify storage {ns}:temp map_edit.map.tick_function set from entity @s data.tick_function
execute unless data entity @s data.tick_function run data remove storage {ns}:temp map_edit.map.tick_function
""")

	## Save a spawn point (macro: path = red/blue/general/etc.)
	write_versioned_function("maps/editor/save_spawn", f"""
# @s = marker entity, at its position
# Get absolute position
execute store result score #ax {ns}.data run data get entity @s Pos[0]
execute store result score #ay {ns}.data run data get entity @s Pos[1]
execute store result score #az {ns}.data run data get entity @s Pos[2]

# Compute relative coordinates
scoreboard players operation #ax {ns}.data -= #base_x {ns}.data
scoreboard players operation #ay {ns}.data -= #base_y {ns}.data
scoreboard players operation #az {ns}.data -= #base_z {ns}.data

# Build coordinate array [x, y, z, yaw]
data modify storage {ns}:temp _save_coord set value [0, 0, 0, 0.0f]
execute store result storage {ns}:temp _save_coord[0] int 1 run scoreboard players get #ax {ns}.data
execute store result storage {ns}:temp _save_coord[1] int 1 run scoreboard players get #ay {ns}.data
execute store result storage {ns}:temp _save_coord[2] int 1 run scoreboard players get #az {ns}.data
data modify storage {ns}:temp _save_coord[3] set from entity @s data.yaw

# Append to the correct list
$data modify storage {ns}:temp map_edit.map.spawning_points.$(path) append from storage {ns}:temp _save_coord
""")

	## Save a point element (macro: path = boundaries/out_of_bounds/etc.)
	write_versioned_function("maps/editor/save_point", f"""
# @s = marker entity, at its position
# Get absolute position
execute store result score #ax {ns}.data run data get entity @s Pos[0]
execute store result score #ay {ns}.data run data get entity @s Pos[1]
execute store result score #az {ns}.data run data get entity @s Pos[2]

# Compute relative coordinates
scoreboard players operation #ax {ns}.data -= #base_x {ns}.data
scoreboard players operation #ay {ns}.data -= #base_y {ns}.data
scoreboard players operation #az {ns}.data -= #base_z {ns}.data

# Build coordinate array [x, y, z]
data modify storage {ns}:temp _save_coord set value [0, 0, 0]
execute store result storage {ns}:temp _save_coord[0] int 1 run scoreboard players get #ax {ns}.data
execute store result storage {ns}:temp _save_coord[1] int 1 run scoreboard players get #ay {ns}.data
execute store result storage {ns}:temp _save_coord[2] int 1 run scoreboard players get #az {ns}.data

# Append to the correct list
$data modify storage {ns}:temp map_edit.map.$(path) append from storage {ns}:temp _save_coord
""")

	## Save an enemy element (pos + function)
	write_versioned_function("maps/editor/save_enemy", f"""
# @s = enemy marker, at its position
# Get absolute position
execute store result score #ax {ns}.data run data get entity @s Pos[0]
execute store result score #ay {ns}.data run data get entity @s Pos[1]
execute store result score #az {ns}.data run data get entity @s Pos[2]

# Compute relative coordinates
scoreboard players operation #ax {ns}.data -= #base_x {ns}.data
scoreboard players operation #ay {ns}.data -= #base_y {ns}.data
scoreboard players operation #az {ns}.data -= #base_z {ns}.data

# Build enemy entry {{pos:[x,y,z], function:"..."}}
data modify storage {ns}:temp _save_enemy set value {{pos:[0,0,0],function:""}}
execute store result storage {ns}:temp _save_enemy.pos[0] int 1 run scoreboard players get #ax {ns}.data
execute store result storage {ns}:temp _save_enemy.pos[1] int 1 run scoreboard players get #ay {ns}.data
execute store result storage {ns}:temp _save_enemy.pos[2] int 1 run scoreboard players get #az {ns}.data
data modify storage {ns}:temp _save_enemy.function set from entity @s data.function

# Append to enemies list
data modify storage {ns}:temp map_edit.map.enemies append from storage {ns}:temp _save_enemy
""")

	## Save a start command element (pos + command)
	write_versioned_function("maps/editor/save_start_command", f"""
# @s = start command marker, at its position
# Get absolute position
execute store result score #ax {ns}.data run data get entity @s Pos[0]
execute store result score #ay {ns}.data run data get entity @s Pos[1]
execute store result score #az {ns}.data run data get entity @s Pos[2]

# Compute relative coordinates
scoreboard players operation #ax {ns}.data -= #base_x {ns}.data
scoreboard players operation #ay {ns}.data -= #base_y {ns}.data
scoreboard players operation #az {ns}.data -= #base_z {ns}.data

# Build start command entry {{pos:[x,y,z],command:"..."}}
data modify storage {ns}:temp _save_start_cmd set value {{pos:[0,0,0],command:""}}
execute store result storage {ns}:temp _save_start_cmd.pos[0] int 1 run scoreboard players get #ax {ns}.data
execute store result storage {ns}:temp _save_start_cmd.pos[1] int 1 run scoreboard players get #ay {ns}.data
execute store result storage {ns}:temp _save_start_cmd.pos[2] int 1 run scoreboard players get #az {ns}.data
data modify storage {ns}:temp _save_start_cmd.command set from entity @s data.command

# Append to list path
$data modify storage {ns}:temp map_edit.map.$(path) append from storage {ns}:temp _save_start_cmd
""")

	## Save a respawn command element (pos + command)
	write_versioned_function("maps/editor/save_respawn_command", f"""
# @s = respawn command marker, at its position
# Get absolute position
execute store result score #ax {ns}.data run data get entity @s Pos[0]
execute store result score #ay {ns}.data run data get entity @s Pos[1]
execute store result score #az {ns}.data run data get entity @s Pos[2]

# Compute relative coordinates
scoreboard players operation #ax {ns}.data -= #base_x {ns}.data
scoreboard players operation #ay {ns}.data -= #base_y {ns}.data
scoreboard players operation #az {ns}.data -= #base_z {ns}.data

# Build respawn command entry {{pos:[x,y,z],command:"..."}}
data modify storage {ns}:temp _save_respawn_cmd set value {{pos:[0,0,0],command:""}}
execute store result storage {ns}:temp _save_respawn_cmd.pos[0] int 1 run scoreboard players get #ax {ns}.data
execute store result storage {ns}:temp _save_respawn_cmd.pos[1] int 1 run scoreboard players get #ay {ns}.data
execute store result storage {ns}:temp _save_respawn_cmd.pos[2] int 1 run scoreboard players get #az {ns}.data
data modify storage {ns}:temp _save_respawn_cmd.command set from entity @s data.command

# Append to list path
$data modify storage {ns}:temp map_edit.map.$(path) append from storage {ns}:temp _save_respawn_cmd
""")

	## Save a zb_object element (macro: path = wallbuys/doors/etc.)
	write_versioned_function("maps/editor/save_zb_object", f"""
# @s = marker entity, at its position
# Get absolute position
execute store result score #ax {ns}.data run data get entity @s Pos[0]
execute store result score #ay {ns}.data run data get entity @s Pos[1]
execute store result score #az {ns}.data run data get entity @s Pos[2]

# Compute relative coordinates
scoreboard players operation #ax {ns}.data -= #base_x {ns}.data
scoreboard players operation #ay {ns}.data -= #base_y {ns}.data
scoreboard players operation #az {ns}.data -= #base_z {ns}.data

# Copy marker's data compound as the base entry
data modify storage {ns}:temp _save_zb set from entity @s data

# Overwrite pos with relative coordinates
data modify storage {ns}:temp _save_zb.pos set value [0, 0, 0]
execute store result storage {ns}:temp _save_zb.pos[0] int 1 run scoreboard players get #ax {ns}.data
execute store result storage {ns}:temp _save_zb.pos[1] int 1 run scoreboard players get #ay {ns}.data
execute store result storage {ns}:temp _save_zb.pos[2] int 1 run scoreboard players get #az {ns}.data

# Build rotation array from yaw (pitch is always 0)
data modify storage {ns}:temp _save_zb.rotation set value [0.0f, 0.0f]
data modify storage {ns}:temp _save_zb.rotation[0] set from entity @s data.yaw

# Remove internal-only marker fields (yaw is stored in rotation array)
data remove storage {ns}:temp _save_zb.yaw

# Append to the correct list
$data modify storage {ns}:temp map_edit.map.$(path) append from storage {ns}:temp _save_zb
""")

	## Write map back to storage at the correct index and mode
	write_versioned_function("maps/editor/write_back", f"""
$data modify storage {ns}:maps $(mode)[$(idx)] set from storage {ns}:temp map_edit.map
""")

	# Exit Without Saving ────────────────────────────────────────
	write_versioned_function("maps/editor/exit", f"""
execute unless score @s {ns}.mp.map_edit matches 1 run return fail
function {ns}:v{version}/maps/editor/cleanup
tellraw @s [{MGS_TAG},{{"text":"Exited map editor (changes discarded).","color":"red"}}]
""")

	# Cleanup (shared by save_exit and exit) ─────────────────────
	write_versioned_function("maps/editor/cleanup", f"""
# Kill all editor markers and model displays
kill @e[tag={ns}.map_element]
kill @e[tag={ns}.editor_display]

# Reset editor state
scoreboard players set @s {ns}.mp.map_edit 0
tag @s remove {ns}.map_editor

# Clear editor tools
clear @s
""")

	# Model Displays ─────────────────────────────────────────────
	# Show the real in-game models for wallbuys, perk machines, PAP, mystery boxes, and the
	# power switch while editing. Displays are rebuilt from the markers every second (and on
	# placement/destroy), so edits like rotation or item_model changes stay in sync.
	# Each displays/<etype> function mirrors that system's own setup placement exactly.
	write_versioned_function("maps/editor/refresh_displays", f"""
# Rebuild all editor model displays from the current markers
kill @e[tag={ns}.editor_display]
execute as @e[tag={ns}.element.wallbuy] at @s run function {ns}:v{version}/maps/editor/displays/wallbuy
execute as @e[tag={ns}.element.perk_machine] at @s run function {ns}:v{version}/maps/editor/displays/perk_machine
execute as @e[tag={ns}.element.wunderfizz] at @s run function {ns}:v{version}/maps/editor/displays/wunderfizz
execute as @e[tag={ns}.element.pap_machine] at @s run function {ns}:v{version}/maps/editor/displays/pap_machine
execute as @e[tag={ns}.element.mystery_box_pos] at @s run function {ns}:v{version}/maps/editor/displays/mystery_box_pos
execute as @e[tag={ns}.element.power_switch] at @s run function {ns}:v{version}/maps/editor/displays/power_switch
execute as @e[tag={ns}.element.barrier] at @s run function {ns}:v{version}/maps/editor/displays/barrier
""")

	## Barrier: block_display of the "enabled" (intact) block, mirroring zombies/barriers/place_at
	## so a map maker sees the boards exactly where they will stand in game.
	write_versioned_function("maps/editor/displays/barrier", f"""
# @s = barrier marker, at @s
data modify storage {ns}:temp _ed_bar.yaw set value 0.0f
execute if data entity @s data.yaw run data modify storage {ns}:temp _ed_bar.yaw set from entity @s data.yaw

# Fall back to the element default when the marker has no block configured yet
data modify storage {ns}:temp _ed_bar.block set value {{Name:"minecraft:oak_fence_gate",Properties:{{open:"false"}}}}
execute if data entity @s data.block_enabled run data modify storage {ns}:temp _ed_bar.block set from entity @s data.block_enabled

execute align xyz positioned ~.5 ~.5 ~.5 run function {ns}:v{version}/maps/editor/displays/summon_barrier with storage {ns}:temp _ed_bar
""")
	write_versioned_function("maps/editor/displays/summon_barrier", f"""
# Same placement and transform as zombies/barriers/place_at
$summon minecraft:block_display ~ ~ ~ {{Rotation:[$(yaw),0f],block_state:$(block),transformation:{{left_rotation:[0f,0f,0f,1f],scale:[1f,1f,1f],translation:[-0.5f,-0.5f,-0.5f],right_rotation:[0f,0f,0f,1f]}},Tags:["{ns}.editor_display"]}}
""")

	## Wallbuy: weapon item display against the wall (same placement/scale as zombies/wallbuys setup)
	write_versioned_function("maps/editor/displays/wallbuy", f"""
# @s = wallbuy marker, at @s (marker Rotation is synced from data.yaw)
data modify storage {ns}:temp _ed_disp.weapon_id set from entity @s data.weapon_id
data modify storage {ns}:temp _ed_disp.yaw set value 0.0f
data modify storage {ns}:temp _ed_disp.yaw set from entity @s data.yaw
function {ns}:v{version}/maps/editor/displays/summon_wallbuy with storage {ns}:temp _ed_disp
""")
	write_versioned_function("maps/editor/displays/summon_wallbuy", f"""
# Display offset up + toward the wall face, scale 0.6 (mirrors zombies/wallbuys/place_at + tp)
$summon minecraft:item_display ^ ^0.5 ^-0.49 {{Rotation:[$(yaw),0f],billboard:"fixed",item_display:"fixed",Tags:["{ns}.editor_display","{ns}._ed_new_disp"],transformation:{{left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],translation:[0f,0f,0f],scale:[0.6f,0.6f,0.6f]}}}}
$execute as @n[tag={ns}._ed_new_disp] run loot replace entity @s contents loot {ns}:i/$(weapon_id)
tag @e[tag={ns}._ed_new_disp] remove {ns}._ed_new_disp
""")

	## Perk machine: mirror zombies/perks/setup_iter display logic (default potion model with
	## per-perk override; map-defined display_item/item_model take precedence)
	write_versioned_function("maps/editor/displays/perk_machine", f"""
# @s = perk machine marker, at @s
data modify storage {ns}:temp _pk_disp.tag set value "{ns}.editor_display"
data modify storage {ns}:temp _pk_disp.item_id set value ""
data modify storage {ns}:temp _pk_disp.item_model set value ""
data modify storage {ns}:temp _pk_disp.yaw set value 0.0f
execute if data entity @s data.display_item run data modify storage {ns}:temp _pk_disp.item_id set from entity @s data.display_item
execute if data entity @s data.item_model run data modify storage {ns}:temp _pk_disp.item_model set from entity @s data.item_model
execute if data storage {ns}:temp _pk_disp{{item_id:""}} run data modify storage {ns}:temp _pk_disp.item_id set value "minecraft:potion"
execute if data storage {ns}:temp _pk_disp{{item_model:""}} run data modify storage {ns}:temp _pk_disp.item_model set value "minecraft:potion"
data modify storage {ns}:temp _pk_disp.perk_id set from entity @s data.perk_id
execute if data storage {ns}:temp _pk_disp{{item_model:"minecraft:potion"}} run function {ns}:v{version}/zombies/perks/override_perk_model with storage {ns}:temp _pk_disp
execute if data entity @s data.yaw run data modify storage {ns}:temp _pk_disp.yaw set from entity @s data.yaw
execute align xyz positioned ~.5 ~-.37 ~.5 positioned ^ ^ ^-0.49 run function {ns}:v{version}/zombies/display/summon_machine_display with storage {ns}:temp _pk_disp
""")

	## Der Wunderfizz: mirror zombies/wunderfizz/setup_iter display logic (perk-machine pipeline)
	write_versioned_function("maps/editor/displays/wunderfizz", f"""
# @s = wunderfizz marker, at @s
data modify storage {ns}:temp _wf_disp.tag set value "{ns}.editor_display"
data modify storage {ns}:temp _wf_disp.item_id set value ""
data modify storage {ns}:temp _wf_disp.item_model set value ""
data modify storage {ns}:temp _wf_disp.yaw set value 0.0f
execute if data entity @s data.display_item run data modify storage {ns}:temp _wf_disp.item_id set from entity @s data.display_item
execute if data entity @s data.item_model run data modify storage {ns}:temp _wf_disp.item_model set from entity @s data.item_model
execute if data storage {ns}:temp _wf_disp{{item_id:""}} run data modify storage {ns}:temp _wf_disp.item_id set value "minecraft:potion"
execute if data storage {ns}:temp _wf_disp{{item_model:""}} run data modify storage {ns}:temp _wf_disp.item_model set value "{ns}:der_wunderfizz"
execute if data entity @s data.yaw run data modify storage {ns}:temp _wf_disp.yaw set from entity @s data.yaw
execute align xyz positioned ~.5 ~-.37 ~.5 positioned ^ ^ ^-0.49 run function {ns}:v{version}/zombies/display/summon_machine_display with storage {ns}:temp _wf_disp
""")

	## Pack-a-Punch: mirror zombies/pap/setup_iter display logic
	write_versioned_function("maps/editor/displays/pap_machine", f"""
# @s = pap machine marker, at @s
data modify storage {ns}:temp _pap_disp.tag set value "{ns}.editor_display"
data modify storage {ns}:temp _pap_disp.item_id set value ""
data modify storage {ns}:temp _pap_disp.item_model set value ""
data modify storage {ns}:temp _pap_disp.yaw set value 0.0f
execute if data entity @s data.display_item run data modify storage {ns}:temp _pap_disp.item_id set from entity @s data.display_item
execute if data entity @s data.item_model run data modify storage {ns}:temp _pap_disp.item_model set from entity @s data.item_model
execute if data storage {ns}:temp _pap_disp{{item_id:""}} run data modify storage {ns}:temp _pap_disp.item_id set value "minecraft:netherite_block"
execute if data storage {ns}:temp _pap_disp{{item_model:""}} run data modify storage {ns}:temp _pap_disp.item_model set value "{ns}:pack_a_punch"
execute if data entity @s data.yaw run data modify storage {ns}:temp _pap_disp.yaw set from entity @s data.yaw
execute positioned ^ ^ ^-0.49 positioned ~ ~-0.4 ~ run function {ns}:v{version}/zombies/display/summon_machine_display with storage {ns}:temp _pap_disp
""")

	## Mystery box: two-piece chest (base + lid). The in-game box interaction sits at ^ ^2 ^0.3
	## from the map position and the presence chest is drawn 0.9 below it (see zombies/mystery_box).
	write_versioned_function("maps/editor/displays/mystery_box_pos", f"""
# @s = mystery box marker, at @s
data modify storage {ns}:temp _ed_mb.yaw set value 0.0f
data modify storage {ns}:temp _ed_mb.yaw set from entity @s data.yaw
execute positioned ^ ^2 ^0.3 run function {ns}:v{version}/maps/editor/displays/summon_mystery_box with storage {ns}:temp _ed_mb
""")
	write_versioned_function("maps/editor/displays/summon_mystery_box", f"""
# Same models/scale as zombies/mystery_box/summon_presence_display
$execute positioned ~ ~-0.9 ~ run summon minecraft:item_display ~ ~ ~ {{Rotation:[$(yaw),0f],Tags:["{ns}.editor_display"],item_display:"fixed",billboard:"fixed",item:{{id:"minecraft:chest",count:1,components:{{"minecraft:item_model":"{ns}:mystery_box_base"}}}},transformation:{{left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],translation:[0f,0f,0f],scale:[2.4f,2.4f,2.4f]}}}}
$execute positioned ~ ~-0.9 ~ run summon minecraft:item_display ~ ~ ~ {{Rotation:[$(yaw),0f],Tags:["{ns}.editor_display"],item_display:"fixed",billboard:"fixed",item:{{id:"minecraft:chest",count:1,components:{{"minecraft:item_model":"{ns}:mystery_box_lid"}}}},transformation:{{left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],translation:[0f,0f,0f],scale:[2.4f,2.4f,2.4f]}}}}
""")

	## Power switch: block-centered lever display (same as zombies/power setup)
	write_versioned_function("maps/editor/displays/power_switch", f"""
# @s = power switch marker, at @s
data modify storage {ns}:temp _ed_ps.yaw set value 0.0f
data modify storage {ns}:temp _ed_ps.yaw set from entity @s data.yaw
execute align xyz positioned ~.5 ~.5 ~.5 run function {ns}:v{version}/maps/editor/displays/summon_power_switch with storage {ns}:temp _ed_ps
""")
	write_versioned_function("maps/editor/displays/summon_power_switch", f"""
$summon minecraft:item_display ~ ~ ~ {{Rotation:[$(yaw),0f],Tags:["{ns}.editor_display"],item_display:"fixed",billboard:"fixed",item:{{id:"minecraft:lever",count:1,components:{{"minecraft:item_model":"{ns}:power_switch"}}}},transformation:{{left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],translation:[0f,0f,0f],scale:[1f,1f,1f]}}}}
""")

	# Editor Tick (universal - shows all element types) ──────────
	# Editor particles go only to players actually in editor mode. A particle command with no viewer
	# selector is transmitted to every player on the server, so the markers were costing bandwidth
	# and client FPS for everyone in the game, not just the map maker.
	editor_viewers: str = f"@a[scores={{{ns}.mp.map_edit=1}},distance=..48]"

	particle_lines: list[str] = []
	for etype, einfo in ALL_ELEMENTS.items():
		# Elements with a real model display don't need a dust particle marker
		if einfo["save_type"] == "config" or etype in MODEL_DISPLAY_ELEMENTS:
			continue
		r, g, b = einfo["particle"]
		scale = einfo["particle_scale"]
		spread = "0.2 0.5 0.2" if einfo["save_type"] == "spawn" else "0.3 0.5 0.3"
		count = 2 if etype == "base_coordinates" else 1
		particle_lines.append(
			f'execute at @e[tag={ns}.element.{etype}] run particle dust{{color:[{r},{g},{b}],scale:{scale}}} ~ ~1 ~ {spread} 0 {count} normal {editor_viewers}'
		)

	# Markers that already draw a real model don't get the white rotation tick either
	model_excluded: str = "".join(f",tag=!{ns}.element.{etype}" for etype in MODEL_DISPLAY_ELEMENTS)

	actionbar_type_lines: list[str] = []
	for etype, einfo in ALL_ELEMENTS.items():
		if einfo["save_type"] == "config":
			continue
		actionbar_type_lines.append(
			f'execute if entity @s[tag={ns}.element.{etype}] run return run title @a[tag={ns}.check_nearest] actionbar [{{"text":"{einfo["emoji"]} ","color":"{einfo["color"]}"}},{{"text":"{einfo["name"]}"}}]'
		)

	# Show nearest element name in actionbar (runs as the nearest marker)
	write_versioned_function("maps/editor/actionbar_nearest", "\n".join(actionbar_type_lines))

	write_versioned_function("maps/editor/tick", f"""
# Only run for players in editor mode
execute unless score @s {ns}.mp.map_edit matches 1 run return fail

# Actionbar: show nearest element info (within 5 blocks). Genuinely per-player, stays here.
tag @s add {ns}.check_nearest
execute as @n[type=minecraft:marker,tag={ns}.map_element,distance=..5] run function {ns}:v{version}/maps/editor/actionbar_nearest
tag @s remove {ns}.check_nearest

# Everything else the editor draws is map-wide, not per-player, but this function runs once per
# editing player — so marker rotation syncing, the display rebuild and every particle used to be
# repeated for each of them. Do that work once per tick instead, whoever gets here first.
execute unless score #ed_global_tick {ns}.data = #total_tick {ns}.data run function {ns}:v{version}/maps/editor/global_tick
""")

	## Map-wide editor rendering: runs at most once per tick regardless of how many players edit
	write_versioned_function("maps/editor/global_tick", f"""
# Claim this tick so the remaining editors skip straight past the call above
scoreboard players operation #ed_global_tick {ns}.data = #total_tick {ns}.data

# Model displays: rebuild once per second so rotation/config edits on markers stay in sync.
# The marker rotation sync is an NBT read plus an NBT write per marker, which is far too expensive
# to run every tick — and yaw only ever changes when someone edits it, so once a second is plenty.
scoreboard players operation #ed_disp_phase {ns}.data = #total_tick {ns}.data
scoreboard players operation #ed_disp_phase {ns}.data %= #20 {ns}.data
execute if score #ed_disp_phase {ns}.data matches 0 as @e[type=minecraft:marker,tag={ns}.map_element] run data modify entity @s Rotation[0] set from entity @s data.yaw
execute if score #ed_disp_phase {ns}.data matches 0 run function {ns}:v{version}/maps/editor/refresh_displays

# Marker particles every 4 ticks: dust lingers about a second, so this looks identical to emitting
# them every tick while cutting the particle commands (and the packets they generate) by 4x.
scoreboard players operation #ed_part_phase {ns}.data = #total_tick {ns}.data
scoreboard players operation #ed_part_phase {ns}.data %= #4 {ns}.data
execute if score #ed_part_phase {ns}.data matches 0 run function {ns}:v{version}/maps/editor/particles
""")

	write_versioned_function("maps/editor/particles", f"""
# Rotation indicator, skipped for markers that already draw a real model
execute as @e[type=minecraft:marker,tag={ns}.map_element{model_excluded}] at @s positioned ^ ^ ^0.5 run particle dust{{color:[1.0,1.0,1.0],scale:0.5}} ~ ~1.69 ~ 0.1 0.1 0.1 0 5 normal {editor_viewers}

# Per-element markers
{chr(10).join(particle_lines)}
""")

	# Coord Stick ─────────────────────────────────────────────────
	# Detection in player/tick (prepend so it runs before scoreboard reset)
	write_versioned_function("player/tick", f"""
# Coord stick: detect right-click on coord stick
execute if score @s {ns}.class_menu matches 1.. if items entity @s weapon.mainhand *[custom_data~{{{ns}:{{coord_stick:true}}}}] run function {ns}:v{version}/utils/coord_stick
""", prepend=True)

	## Entry point (runs as player)
	write_versioned_function("utils/coord_stick", f"""
# Tag the player so tellraw can target them from inside the at-aimed-block context
tag @s add {ns}.coord_stick_user
function #bs.view:at_aimed_block {{run:"function {ns}:v{version}/utils/coord_stick_relative",with:{{}}}}
tag @s remove {ns}.coord_stick_user
""")

	## State machine — runs at the aimed block
	write_versioned_function("utils/coord_stick_relative", f"""
# State: 0 = first click, 1 = second click (origin already saved)
scoreboard players set #cs_state {ns}.data 0
execute if data storage {ns}:temp coord_stick.origin run scoreboard players set #cs_state {ns}.data 1

# Particle at block center
execute align xyz run particle firework ~.5 ~.5 ~.5 0.4 0.4 0.4 0.01 100 force @a[distance=..20]

# --- Second click: compute relative offset ---
execute if score #cs_state {ns}.data matches 1 summon marker run function {ns}:v{version}/utils/coord_stick_store_pos
execute if score #cs_state {ns}.data matches 1 run scoreboard players operation #cs_dest_x {ns}.data = #cs_pos_x {ns}.data
execute if score #cs_state {ns}.data matches 1 run scoreboard players operation #cs_dest_y {ns}.data = #cs_pos_y {ns}.data
execute if score #cs_state {ns}.data matches 1 run scoreboard players operation #cs_dest_z {ns}.data = #cs_pos_z {ns}.data
execute if score #cs_state {ns}.data matches 1 store result score #cs_orig_x {ns}.data run data get storage {ns}:temp coord_stick.origin[0]
execute if score #cs_state {ns}.data matches 1 store result score #cs_orig_y {ns}.data run data get storage {ns}:temp coord_stick.origin[1]
execute if score #cs_state {ns}.data matches 1 store result score #cs_orig_z {ns}.data run data get storage {ns}:temp coord_stick.origin[2]
execute if score #cs_state {ns}.data matches 1 run scoreboard players operation #cs_dest_x {ns}.data -= #cs_orig_x {ns}.data
execute if score #cs_state {ns}.data matches 1 run scoreboard players operation #cs_dest_y {ns}.data -= #cs_orig_y {ns}.data
execute if score #cs_state {ns}.data matches 1 run scoreboard players operation #cs_dest_z {ns}.data -= #cs_orig_z {ns}.data
execute if score #cs_state {ns}.data matches 1 run data modify storage {ns}:temp coord_stick.result set value {{x:0,y:0,z:0}}
execute if score #cs_state {ns}.data matches 1 store result storage {ns}:temp coord_stick.result.x int 1 run scoreboard players get #cs_dest_x {ns}.data
execute if score #cs_state {ns}.data matches 1 store result storage {ns}:temp coord_stick.result.y int 1 run scoreboard players get #cs_dest_y {ns}.data
execute if score #cs_state {ns}.data matches 1 store result storage {ns}:temp coord_stick.result.z int 1 run scoreboard players get #cs_dest_z {ns}.data
execute if score #cs_state {ns}.data matches 1 as @a[tag={ns}.coord_stick_user,limit=1] run function {ns}:v{version}/utils/coord_stick_print with storage {ns}:temp coord_stick.result
execute if score #cs_state {ns}.data matches 1 run data remove storage {ns}:temp coord_stick.result
execute if score #cs_state {ns}.data matches 1 run data remove storage {ns}:temp coord_stick.origin

# --- First click: record origin position ---
execute if score #cs_state {ns}.data matches 0 summon marker run function {ns}:v{version}/utils/coord_stick_store_pos
execute if score #cs_state {ns}.data matches 0 run data modify storage {ns}:temp coord_stick.origin set value [0,0,0]
execute if score #cs_state {ns}.data matches 0 store result storage {ns}:temp coord_stick.origin[0] int 1 run scoreboard players get #cs_pos_x {ns}.data
execute if score #cs_state {ns}.data matches 0 store result storage {ns}:temp coord_stick.origin[1] int 1 run scoreboard players get #cs_pos_y {ns}.data
execute if score #cs_state {ns}.data matches 0 store result storage {ns}:temp coord_stick.origin[2] int 1 run scoreboard players get #cs_pos_z {ns}.data
execute if score #cs_state {ns}.data matches 0 as @a[tag={ns}.coord_stick_user,limit=1] run tellraw @s [{MGS_TAG},{{"text":"First position saved! Right-click again to get the offset.","color":"yellow"}}]
""")

	## Stores current entity Pos into #cs_pos_x/y/z scores, then kills the marker
	write_versioned_function("utils/coord_stick_store_pos", f"""
execute store result score #cs_pos_x {ns}.data run data get entity @s Pos[0]
execute store result score #cs_pos_y {ns}.data run data get entity @s Pos[1]
execute store result score #cs_pos_z {ns}.data run data get entity @s Pos[2]
kill @s
""")

	## Macro print: outputs "positioned ~X ~Y ~Z" with copy-to-clipboard click event
	write_versioned_function("utils/coord_stick_print", f"""
$tellraw @s [{MGS_TAG},{{"text":"positioned ~$(x) ~$(y) ~$(z)","color":"aqua","click_event":{{"action":"copy_to_clipboard","value":"positioned ~$(x) ~$(y) ~$(z)"}},"hover_event":{{"action":"show_text","value":"Click to copy"}}}}]
""")
