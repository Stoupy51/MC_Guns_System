
# ruff: noqa: E501
# Map Editor - Generic for Multiplayer, Missions, and Zombies maps
# Provides an in-game editor with mode switching for placing map elements.
# Elements are placed via spawn eggs detected by advancement (item_used_on_block).
# Markers in the world represent elements during editing; storage is written on save.

from stewbeet import Advancement, JsonDict, Mem, set_json_encoder, write_load_file, write_versioned_function

from .helpers import MGS_TAG, btn

MAX_MAPS = 50

# ── Element Definitions ───────────────────────────────────────────
# All element types across all modes. Each has display properties, save info, and egg model.
# save_type: "base" (single, handled specially), "spawn" (list of [x,y,z,yaw]), "point" (list of [x,y,z])
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
}

# ── Mode Definitions ──────────────────────────────────────────────
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
		},
	},
	"zombies": {
		"name": "Zombies",
		"color": "dark_green",
		"storage_key": "zombies",
		"slots": {
			"base_coordinates": "hotbar.0",
		},
	},
	"missions": {
		"name": "Missions",
		"color": "aqua",
		"storage_key": "missions",
		"slots": {
			"base_coordinates": "hotbar.0",
		},
	},
}

MODE_LIST: list[str] = list(EDITOR_MODES.keys())


def generate_map_editor() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	sep = '{"text":"============================================","color":"dark_gray"}'

	# ── Scoreboards & Storage Init ─────────────────────────────────
	write_load_file(f"""
# Map editor scoreboards
scoreboard objectives add {ns}.mp.map_edit dummy
scoreboard objectives add {ns}.mp.map_idx dummy
scoreboard objectives add {ns}.mp.map_mode dummy
""")

	storage_init_lines = "\n".join(
		f'execute unless data storage {ns}:maps {mode_info["storage_key"]} run data modify storage {ns}:maps {mode_info["storage_key"]} set value []'
		for mode_info in EDITOR_MODES.values()
	)
	write_load_file(f"""
# Initialize maps storage for all modes
{storage_init_lines}
""")

	# ── Advancement for egg placement detection ─────────────────────
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

	# ── Mode tab buttons (used in all list views) ──────────────────
	mode_tabs = ",".join(
		btn(mode_info["name"], f"/function {ns}:v{version}/maps/editor/list/{mode_key}", mode_info["color"], f"View {mode_info['name']} maps")
		for mode_key, mode_info in EDITOR_MODES.items()
	)

	# ── Menu Entry Point ───────────────────────────────────────────
	write_versioned_function("maps/editor/menu", f"""
# Default: show multiplayer maps
function {ns}:v{version}/maps/editor/list/multiplayer
""")

	# ── Per-Mode Map List ──────────────────────────────────────────
	for mode_key, mode_info in EDITOR_MODES.items():
		sk = mode_info["storage_key"]
		create_btn = btn("+ Create New Map", f"/function {ns}:v{version}/maps/editor/create/{mode_key}", "green", f"Create a new {mode_info['name']} map")

		write_versioned_function(f"maps/editor/list/{mode_key}", f"""
tellraw @s {sep}
tellraw @s [{{"text":"","color":"gold","bold":true}},"       🗺 ",{{"text":"Map Editor"}}," 🗺"]
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
execute unless data storage {ns}:maps {sk}[0] run tellraw @s [{{"text":"  No maps created yet.","color":"gray","italic":true}}]

tellraw @s ""
tellraw @s ["  ",{create_btn}]
tellraw @s {sep}
""")

	# ── Menu Entry (recursive - one map per call) ──────────────────
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
$tellraw @s ["  ",{{"text":"$(name)","color":"white"}},{{"text":" ($(id))","color":"gray"}},{{"text":" "}},[{{"text":"[","color":"yellow","click_event":{{"action":"run_command","command":"/function {ns}:v{version}/maps/editor/enter {{idx:$(idx),mode:$(mode)}}"}},"hover_event":{{"action":"show_text","value":"Edit this map"}}}},{{"text":"Edit"}},"]"],{{"text":" "}},[{{"text":"[","color":"red","click_event":{{"action":"run_command","command":"/function {ns}:v{version}/maps/editor/delete {{idx:$(idx),mode:$(mode)}}"}},"hover_event":{{"action":"show_text","value":"Delete this map"}}}},{{"text":"Delete"}},"]"]]
""")

	# ── Map Creation (per mode) ────────────────────────────────────
	for mode_key, mode_info in EDITOR_MODES.items():
		sk = mode_info["storage_key"]
		create_snbt = r"id:'my_map',name:'My Map',description:'A new map',base_coordinates:[0,64,0]"
		back_btn = btn("◀ Back", f"/function {ns}:v{version}/maps/editor/list/{mode_key}", "yellow", "Back to map list")

		write_versioned_function(f"maps/editor/create/{mode_key}", f"""
tellraw @s {sep}
tellraw @s [{{"text":"","color":"gold","bold":true}},"  📝 ",{{"text":"Create New {mode_info['name']} Map"}}]
tellraw @s {sep}
tellraw @s [{{"text":"  Run this command to create a new map:","color":"yellow"}}]
tellraw @s [{{"text":"","color":"aqua","click_event":{{"action":"suggest_command","command":"/data modify storage {ns}:maps {sk} append value {{{create_snbt}}}"}}}},"/data modify storage {ns}:maps {sk} append value {{...}}"]
tellraw @s [{{"text":"  ⬆ Click to paste the command, then edit the id/name/description.","color":"gray","italic":true}}]
tellraw @s ""
tellraw @s ["  ",{back_btn}]
tellraw @s {sep}
""")

	# ── Delete Map (macro with mode) ───────────────────────────────
	write_versioned_function("maps/editor/delete", f"""
$data remove storage {ns}:maps $(mode)[$(idx)]
tellraw @s [{MGS_TAG},{{"text":"Map deleted.","color":"red"}}]

# Refresh menu for the same mode
$function {ns}:v{version}/maps/editor/list/$(mode)
""")

	# ── Enter Editor Mode (macro with mode+idx) ────────────────────
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

# Summon markers for existing elements
function {ns}:v{version}/maps/editor/summon_existing

# Give editor tools (dispatch by mode)
function {ns}:v{version}/maps/editor/give_tools

# Announce
tellraw @s [{MGS_TAG},{{"text":"Entered map editor for: ","color":"green"}},{{"text":"","color":"white"}},{{"storage":"{ns}:temp","nbt":"map_edit.map.name"}}]
tellraw @s [{MGS_TAG},{{"text":"Place eggs to add elements. DESTROY egg (hotbar 9) removes nearest element.","color":"yellow"}}]
tellraw @s [{MGS_TAG},{{"text":"Use ","color":"gray"}},{btn("Save & Exit", f"/function {ns}:v{version}/maps/editor/save_exit", "green", "Save changes and exit editor")},{{"text":" or "}},{btn("Exit", f"/function {ns}:v{version}/maps/editor/exit", "red", "Discard changes and exit editor")}]
""")

	write_versioned_function("maps/editor/load_map_data", f"""
$data modify storage {ns}:temp map_edit.map set from storage {ns}:maps $(mode)[$(idx)]
""")

	# ── Summon Existing Elements ───────────────────────────────────
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

# Mode-specific elements
{summon_dispatch}
""")

	# Per-mode summon functions
	for mode_key, mode_info in EDITOR_MODES.items():
		summon_lines: list[str] = []
		for etype in mode_info["slots"]:
			einfo = ALL_ELEMENTS[etype]
			if einfo["save_type"] == "base":
				continue  # handled in parent
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

		write_versioned_function(
			f"maps/editor/summon_existing/{mode_key}",
			"\n".join(summon_lines) if summon_lines else "# No mode-specific elements to summon"
		)

	# ── Summon helpers (shared) ────────────────────────────────────
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

	# ── Give Editor Tools (dispatch by mode score) ─────────────────
	destroy_cmd = (
		f'item replace entity @s hotbar.8 with minecraft:bat_spawn_egg'
		f'[minecraft:item_name={{"text":"✘ DESTROY","color":"dark_red","italic":false,"bold":true}},'
		f'minecraft:item_model="minecraft:wither_skeleton_spawn_egg",'
		f'minecraft:custom_data={{{ns}:{{editor:true,type:"destroy"}}}},'
		f'minecraft:entity_data={{id:"minecraft:bat",NoAI:1b,Silent:1b,Invulnerable:1b,Tags:["{ns}.new_element","{ns}.element.destroy"]}}]'
	)

	give_dispatch = "\n".join(
		f'execute if score @s {ns}.mp.map_mode matches {i} run function {ns}:v{version}/maps/editor/give_tools/{mk}'
		for i, mk in enumerate(MODE_LIST)
	)

	write_versioned_function("maps/editor/give_tools", f"""
# Destroy egg (always in hotbar.8)
{destroy_cmd}

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
		write_versioned_function(
			f"maps/editor/give_tools/{mode_key}",
			"\n".join(egg_cmds) if egg_cmds else "# No eggs for this mode"
		)

	# ── On Place (Advancement Reward) ──────────────────────────────
	write_versioned_function("maps/editor/on_place", f"""
# Revoke advancement immediately so it can trigger again
advancement revoke @s only {ns}:v{version}/maps/editor/on_place

# Only process if player is in editor mode
execute unless score @s {ns}.mp.map_edit matches 1 run return fail

# Find the newly spawned bat entity (tagged by entity_data)
execute as @n[tag={ns}.new_element] at @s run function {ns}:v{version}/maps/editor/process_element
""")

	# ── Process Placed Element (universal - handles all types) ─────
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
		else:
			continue
		process_lines.append(f'execute if entity @s[tag={ns}.element.{etype}] run function {ns}:v{version}/maps/editor/{handler}')
		process_lines.append(f'execute if entity @s[tag={ns}.element.{etype}] run return run kill @s')
		process_lines.append("")

	process_lines.append("# Fallback: unknown type")
	process_lines.append("kill @s")

	write_versioned_function("maps/editor/process_element", "\n".join(process_lines))

	# ── Handle Base Coordinates ────────────────────────────────────
	write_versioned_function("maps/editor/handle_base", f"""
# Kill any existing base marker
kill @e[tag={ns}.map_element,tag={ns}.element.base_coordinates]

# Get position
execute store result score #base_x {ns}.data run data get entity @s Pos[0]
execute store result score #base_y {ns}.data run data get entity @s Pos[1]
execute store result score #base_z {ns}.data run data get entity @s Pos[2]

# Summon permanent marker
execute store result storage {ns}:temp _pos.x double 1 run scoreboard players get #base_x {ns}.data
execute store result storage {ns}:temp _pos.y double 1 run scoreboard players get #base_y {ns}.data
execute store result storage {ns}:temp _pos.z double 1 run scoreboard players get #base_z {ns}.data
function {ns}:v{version}/maps/editor/summon_base_marker with storage {ns}:temp _pos

# Announce
execute as @a[tag={ns}.map_editor] run tellraw @s [{MGS_TAG},{{"text":"Base coordinates set!","color":"light_purple"}}]
""")

	# ── Handle Spawn Point (universal) ─────────────────────────────
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

# Store the player's rotation on the marker
execute as @n[tag={ns}.new_spawn_marker] store result entity @s data.yaw float 1 run data get entity @p[tag={ns}.map_editor] Rotation[0]
tag @n[tag={ns}.new_spawn_marker] remove {ns}.new_spawn_marker

# Announce
{spawn_msg_lines}
""")

	# ── Handle Point Element (universal) ───────────────────────────
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

	# ── Handle DESTROY ─────────────────────────────────────────────
	write_versioned_function("maps/editor/handle_destroy", f"""
# Find the nearest map element marker (within 10 blocks)
execute positioned as @s as @n[tag={ns}.map_element,distance=..10] run function {ns}:v{version}/maps/editor/destroy_element
execute positioned as @s unless entity @n[tag={ns}.map_element,distance=..10] run tellraw @a[tag={ns}.map_editor] [{MGS_TAG},{{"text":"No element found within 10 blocks!","color":"red"}}]
""")

	# ── Destroy Element (universal) ────────────────────────────────
	destroy_msg_lines = "\n".join(
		f'execute if entity @s[tag={ns}.element.{etype}] run tellraw @a[tag={ns}.map_editor] [{MGS_TAG},{{"text":"{einfo["name"]} removed!","color":"{einfo["color"]}"}}]'
		for etype, einfo in ALL_ELEMENTS.items()
	)

	write_versioned_function("maps/editor/destroy_element", f"""
# @s = the map_element marker to destroy
# Announce what was removed
{destroy_msg_lines}

# Kill the marker
kill @s
""")

	# ── Save and Exit Editor ───────────────────────────────────────
	save_dispatch = "\n".join(
		f'execute if score @s {ns}.mp.map_mode matches {i} run function {ns}:v{version}/maps/editor/save_lists/{mk}'
		for i, mk in enumerate(MODE_LIST)
	)

	write_versioned_function("maps/editor/save_exit", f"""
# Only process if in editor mode
execute unless score @s {ns}.mp.map_edit matches 1 run return fail

# Reload map data (preserves metadata like id, name, description, scripts)
execute store result storage {ns}:temp map_edit.idx int 1 run scoreboard players get @s {ns}.mp.map_idx
function {ns}:v{version}/maps/editor/load_map_data with storage {ns}:temp map_edit

# Rebuild base_coordinates from marker
execute as @n[tag={ns}.map_element,tag={ns}.element.base_coordinates] at @s run function {ns}:v{version}/maps/editor/save_base

# Load base scores for relative computation
execute store result score #base_x {ns}.data run data get storage {ns}:temp map_edit.map.base_coordinates[0]
execute store result score #base_y {ns}.data run data get storage {ns}:temp map_edit.map.base_coordinates[1]
execute store result score #base_z {ns}.data run data get storage {ns}:temp map_edit.map.base_coordinates[2]

# Save mode-specific lists (reset + rebuild from markers)
{save_dispatch}

# Write back to storage
function {ns}:v{version}/maps/editor/write_back with storage {ns}:temp map_edit

# Cleanup and exit
function {ns}:v{version}/maps/editor/cleanup
tellraw @s [{MGS_TAG},{{"text":"Map saved!","color":"green"}}]
""")

	# Per-mode save lists functions
	for mode_key, mode_info in EDITOR_MODES.items():
		reset_lines: list[str] = []
		rebuild_lines: list[str] = []
		for etype in mode_info["slots"]:
			einfo = ALL_ELEMENTS[etype]
			if einfo["save_type"] == "base":
				continue  # handled by save_base

			save_path = einfo["save_path"]
			if einfo["save_type"] == "spawn":
				reset_lines.append(f'data modify storage {ns}:temp map_edit.map.{save_path} set value []')
				path_suffix = save_path.split(".")[-1]
				rebuild_lines.append(f'execute as @e[tag={ns}.map_element,tag={ns}.element.{etype}] at @s run function {ns}:v{version}/maps/editor/save_spawn {{path:"{path_suffix}"}}')
			elif einfo["save_type"] == "point":
				reset_lines.append(f'data modify storage {ns}:temp map_edit.map.{save_path} set value []')
				rebuild_lines.append(f'execute as @e[tag={ns}.map_element,tag={ns}.element.{etype}] at @s run function {ns}:v{version}/maps/editor/save_point {{path:"{save_path}"}}')

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

	## Write map back to storage at the correct index and mode
	write_versioned_function("maps/editor/write_back", f"""
$data modify storage {ns}:maps $(mode)[$(idx)] set from storage {ns}:temp map_edit.map
""")

	# ── Exit Without Saving ────────────────────────────────────────
	write_versioned_function("maps/editor/exit", f"""
execute unless score @s {ns}.mp.map_edit matches 1 run return fail
function {ns}:v{version}/maps/editor/cleanup
tellraw @s [{MGS_TAG},{{"text":"Exited map editor (changes discarded).","color":"red"}}]
""")

	# ── Cleanup (shared by save_exit and exit) ─────────────────────
	write_versioned_function("maps/editor/cleanup", f"""
# Kill all editor markers
kill @e[tag={ns}.map_element]

# Reset editor state
scoreboard players set @s {ns}.mp.map_edit 0
tag @s remove {ns}.map_editor

# Clear editor tools
clear @s
""")

	# ── Editor Tick (universal - shows all element types) ──────────
	particle_lines: list[str] = []
	for etype, einfo in ALL_ELEMENTS.items():
		r, g, b = einfo["particle"]
		scale = einfo["particle_scale"]
		spread = "0.2 0.5 0.2" if einfo["save_type"] == "spawn" else "0.3 0.5 0.3"
		count = 5 if etype == "base_coordinates" else 3
		particle_lines.append(
			f'execute at @e[tag={ns}.map_element,tag={ns}.element.{etype}] run particle dust{{color:[{r},{g},{b}],scale:{scale}}} ~ ~1 ~ {spread} 0 {count}'
		)

	actionbar_lines: list[str] = []
	for etype, einfo in ALL_ELEMENTS.items():
		actionbar_lines.append(
			f'execute if entity @e[tag={ns}.map_element,tag={ns}.element.{etype},distance=..5] run return run title @s actionbar [{{"text":"{einfo["emoji"]} ","color":"{einfo["color"]}"}},{{"text":"{einfo["name"]}"}}]'
		)

	write_versioned_function("maps/editor/tick", f"""
# Only run for players in editor mode
execute unless score @s {ns}.mp.map_edit matches 1 run return fail

# Show rotation indicator for all markers
execute as @e[tag={ns}.map_element] run data modify entity @s Rotation[0] set from entity @s data.yaw
execute as @e[tag={ns}.map_element] at @s positioned ^ ^ ^0.5 run particle dust{{color:[1.0,1.0,1.0],scale:0.5}} ~ ~1.69 ~ 0.1 0.1 0.1 0 5

# Per-element particles
{chr(10).join(particle_lines)}

# Actionbar: show info when near an element (within 5 blocks)
{chr(10).join(actionbar_lines)}
""")
