
# ruff: noqa: E501
# Map Editor for Multiplayer Maps
# Provides an in-game editor to create/edit map definitions with spawn eggs for placing elements.
# Elements are placed via spawn eggs detected by advancement (item_used_on_block).
# Markers in the world represent elements during editing; storage is written on save.

from stewbeet import Advancement, JsonDict, Mem, set_json_encoder, write_load_file, write_versioned_function

from ..helpers import MGS_TAG, btn

MAX_MAPS = 50

# ── Element Definitions ───────────────────────────────────────────
# Each element type maps to: display name, color, particle color (RGB), has_rotation, slot, egg_model
ELEMENT_TYPES: dict[str, JsonDict] = {
	# Hotbar slots (common)
	"base_coordinates":   {"name": "Base Coordinates", "color": "light_purple", "particle": "1.0 0.0 1.0", "has_rotation": False, "slot": "hotbar.0", "egg_model": "minecraft:endermite_spawn_egg"},
	"red_spawn":          {"name": "Red Spawn",        "color": "red",          "particle": "1.0 0.2 0.2", "has_rotation": True,  "slot": "hotbar.1", "egg_model": "minecraft:magma_cube_spawn_egg"},
	"blue_spawn":         {"name": "Blue Spawn",       "color": "blue",         "particle": "0.2 0.2 1.0", "has_rotation": True,  "slot": "hotbar.2", "egg_model": "minecraft:dolphin_spawn_egg"},
	"general_spawn":      {"name": "General Spawn",    "color": "yellow",       "particle": "1.0 1.0 0.2", "has_rotation": True,  "slot": "hotbar.3", "egg_model": "minecraft:blaze_spawn_egg"},
	"out_of_bounds":      {"name": "Out of Bounds",    "color": "dark_red",     "particle": "0.6 0.0 0.0", "has_rotation": False, "slot": "hotbar.4", "egg_model": "minecraft:spider_spawn_egg"},
	# Inventory slots (less common)
	"boundary":           {"name": "Boundary Corner",  "color": "gray",         "particle": "0.8 0.8 0.8", "has_rotation": False, "slot": "inventory.0", "egg_model": "minecraft:skeleton_spawn_egg"},
	"search_and_destroy": {"name": "S&D Objective",    "color": "gold",         "particle": "1.0 0.6 0.0", "has_rotation": False, "slot": "inventory.1", "egg_model": "minecraft:fox_spawn_egg"},
	"domination":         {"name": "Domination Point", "color": "green",        "particle": "0.0 1.0 0.0", "has_rotation": False, "slot": "inventory.2", "egg_model": "minecraft:creeper_spawn_egg"},
	"hardpoint":          {"name": "Hardpoint Zone",   "color": "dark_purple",  "particle": "0.5 0.0 0.5", "has_rotation": False, "slot": "inventory.3", "egg_model": "minecraft:warden_spawn_egg"},
}
# DESTROY egg is in weapon.offhand


def generate_map_editor() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	sep = '{"text":"============================================","color":"dark_gray"}'

	# ── Scoreboards ────────────────────────────────────────────────
	write_load_file(f"""
# Map editor scoreboards
scoreboard objectives add {ns}.mp.map_edit dummy
scoreboard objectives add {ns}.mp.map_idx dummy
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

	# ── Map Browser Menu ───────────────────────────────────────────
	# This function displays a list of maps with Edit/Delete buttons.
	# Since we can't iterate storage in a single tellraw, we use a recursive approach.
	write_versioned_function("maps/editor/menu", f"""
tellraw @s {sep}
tellraw @s [{{"text":"","color":"gold","bold":true}},"       🗺 ",{{"text":"Map Editor"}}," 🗺"]
tellraw @s {sep}

# Copy maps list for iteration
data modify storage {ns}:temp map_menu.list set from storage {ns}:maps multiplayer
scoreboard players set #map_menu_idx {ns}.data 0

# Show each map
execute if data storage {ns}:temp map_menu.list[0] run function {ns}:v{version}/maps/editor/menu_entry

# No maps message
execute unless data storage {ns}:maps multiplayer[0] run tellraw @s [{{"text":"  No maps created yet.","color":"gray","italic":true}}]

tellraw @s ""
tellraw @s ["  ",{btn("+ Create New Map", f"/function {ns}:v{version}/maps/editor/create", "green", "Create a new multiplayer map")}]
tellraw @s {sep}
""")

	## Menu entry (recursive - displays one map per call)
	write_versioned_function("maps/editor/menu_entry", f"""
# Read current map name and id
data modify storage {ns}:temp map_menu.current set from storage {ns}:temp map_menu.list[0]

# Flatten fields for macro (macro vars can't contain dots)
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
$tellraw @s ["  ",{{"text":"$(name)","color":"white"}},{{"text":" ($(id))","color":"gray"}},{{"text":" "}},{{"text":"[Edit]","color":"yellow","click_event":{{"action":"run_command","command":"/function {ns}:v{version}/maps/editor/enter {{idx:$(idx)}}"}},"hover_event":{{"action":"show_text","value":"Edit this map"}}}},{{"text":" "}},{{"text":"[Delete]","color":"red","click_event":{{"action":"run_command","command":"/function {ns}:v{version}/maps/editor/delete {{idx:$(idx)}}"}},"hover_event":{{"action":"show_text","value":"Delete this map"}}}}]
""")

	# ── Map Creation ───────────────────────────────────────────────
	# Build the SNBT command suggestion with properly escaped quotes
	# Since the command contains SNBT with quoted strings, we use single quotes in SNBT
	create_snbt: str = r"id:'my_map',name:'My Map',description:'A new map',base_coordinates:[0,64,0]"
	write_versioned_function("maps/editor/create", f"""
tellraw @s {sep}
tellraw @s [{{"text":"","color":"gold","bold":true}},"  📝 ",{{"text":"Create New Map"}}]
tellraw @s {sep}
tellraw @s [{{"text":"  Run this command to create a new map:","color":"yellow"}}]
tellraw @s [{{"text":"","color":"aqua","click_event":{{"action":"suggest_command","command":"/data modify storage {ns}:maps multiplayer append value {{{create_snbt}}}"}}}},"/data modify storage {ns}:maps multiplayer append value {{...}}"]
tellraw @s [{{"text":"  ⬆ Click to paste the command, then edit the id/name/description.","color":"gray","italic":true}}]
tellraw @s ""
tellraw @s ["  ",{btn("◀ Back", f"/function {ns}:v{version}/maps/editor/menu", "yellow", "Back to map list")}]
tellraw @s {sep}
""")

	# ── Delete Map ──────────────────────────────────────────────────
	write_versioned_function("maps/editor/delete", f"""
# Delete map at given index (called via /function with {{idx:N}})
$data remove storage {ns}:maps multiplayer[$(idx)]
tellraw @s [{MGS_TAG},{{"text":"Map deleted.","color":"red"}}]

# Refresh menu
function {ns}:v{version}/maps/editor/menu
""")

	# ── Enter Editor Mode ──────────────────────────────────────────
	write_versioned_function("maps/editor/enter", f"""
# Set the map index from macro argument (called via /function with {{idx:N}})
$scoreboard players set @s {ns}.mp.map_idx $(idx)

# Mark player as in editor mode
scoreboard players set @s {ns}.mp.map_edit 1
tag @s add {ns}.map_editor

# Store index for macro access
execute store result storage {ns}:temp map_edit.idx int 1 run scoreboard players get @s {ns}.mp.map_idx

# Load map data to temp
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

# Give editor tools (eggs)
function {ns}:v{version}/maps/editor/give_tools

# Announce
tellraw @s [{MGS_TAG},{{"text":"Entered map editor for: ","color":"green"}},{{"text":"","color":"white"}},{{"storage":"{ns}:temp","nbt":"map_edit.map.name"}}]
tellraw @s [{MGS_TAG},{{"text":"Place eggs to add elements. DESTROY egg (slot 9) removes nearest element.","color":"yellow"}}]
tellraw @s [{MGS_TAG},{{"text":"Use ","color":"gray"}},{btn("Save & Exit", f"/function {ns}:v{version}/maps/editor/save_exit", "green", "Save changes and exit editor")},{{"text":" or "}},{btn("Exit", f"/function {ns}:v{version}/maps/editor/exit", "red", "Discard changes and exit editor")}]
""")

	write_versioned_function("maps/editor/load_map_data", f"""
$data modify storage {ns}:temp map_edit.map set from storage {ns}:maps multiplayer[$(idx)]
""")

	# ── Summon Existing Elements ───────────────────────────────────
	# Recreate markers from the stored map data when entering editor
	write_versioned_function("maps/editor/summon_existing", f"""
# Base coordinates marker (at absolute position)
execute store result score #bx {ns}.data run data get storage {ns}:temp map_edit.map.base_coordinates[0]
execute store result score #by {ns}.data run data get storage {ns}:temp map_edit.map.base_coordinates[1]
execute store result score #bz {ns}.data run data get storage {ns}:temp map_edit.map.base_coordinates[2]
execute store result storage {ns}:temp _pos.x double 1 run scoreboard players get #bx {ns}.data
execute store result storage {ns}:temp _pos.y double 1 run scoreboard players get #by {ns}.data
execute store result storage {ns}:temp _pos.z double 1 run scoreboard players get #bz {ns}.data
function {ns}:v{version}/maps/editor/summon_base_marker with storage {ns}:temp _pos

# Summon spawn point markers (iterate each list)
data modify storage {ns}:temp _spawn_iter set from storage {ns}:temp map_edit.map.spawning_points.red
scoreboard players set #_spawn_type {ns}.data 1
execute if data storage {ns}:temp _spawn_iter[0] run function {ns}:v{version}/maps/editor/summon_spawn_iter

data modify storage {ns}:temp _spawn_iter set from storage {ns}:temp map_edit.map.spawning_points.blue
scoreboard players set #_spawn_type {ns}.data 2
execute if data storage {ns}:temp _spawn_iter[0] run function {ns}:v{version}/maps/editor/summon_spawn_iter

data modify storage {ns}:temp _spawn_iter set from storage {ns}:temp map_edit.map.spawning_points.general
scoreboard players set #_spawn_type {ns}.data 3
execute if data storage {ns}:temp _spawn_iter[0] run function {ns}:v{version}/maps/editor/summon_spawn_iter

# Summon boundary markers
data modify storage {ns}:temp _point_iter set from storage {ns}:temp map_edit.map.boundaries
scoreboard players set #_point_tag {ns}.data 1
execute if data storage {ns}:temp _point_iter[0] run function {ns}:v{version}/maps/editor/summon_point_iter

# Summon out_of_bounds markers
data modify storage {ns}:temp _point_iter set from storage {ns}:temp map_edit.map.out_of_bounds
scoreboard players set #_point_tag {ns}.data 2
execute if data storage {ns}:temp _point_iter[0] run function {ns}:v{version}/maps/editor/summon_point_iter

# Summon search_and_destroy markers
data modify storage {ns}:temp _point_iter set from storage {ns}:temp map_edit.map.search_and_destroy
scoreboard players set #_point_tag {ns}.data 3
execute if data storage {ns}:temp _point_iter[0] run function {ns}:v{version}/maps/editor/summon_point_iter

# Summon domination markers
data modify storage {ns}:temp _point_iter set from storage {ns}:temp map_edit.map.domination
scoreboard players set #_point_tag {ns}.data 4
execute if data storage {ns}:temp _point_iter[0] run function {ns}:v{version}/maps/editor/summon_point_iter

# Summon hardpoint markers
data modify storage {ns}:temp _point_iter set from storage {ns}:temp map_edit.map.hardpoint
scoreboard players set #_point_tag {ns}.data 5
execute if data storage {ns}:temp _point_iter[0] run function {ns}:v{version}/maps/editor/summon_point_iter
""")

	write_versioned_function("maps/editor/summon_base_marker", f"""
$summon minecraft:marker $(x) $(y) $(z) {{Tags:["{ns}.map_element","{ns}.element.base_coordinates"]}}
""")

	# Summon spawn point markers (iterate list of [x,y,z,yaw] relative coords)
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

# Determine tag based on type (1=red, 2=blue, 3=general)
execute if score #_spawn_type {ns}.data matches 1 run data modify storage {ns}:temp _spos.tag set value "{ns}.element.red_spawn"
execute if score #_spawn_type {ns}.data matches 2 run data modify storage {ns}:temp _spos.tag set value "{ns}.element.blue_spawn"
execute if score #_spawn_type {ns}.data matches 3 run data modify storage {ns}:temp _spos.tag set value "{ns}.element.general_spawn"

# Summon marker with yaw stored in data
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

	# Summon point markers (iterate list of [x,y,z] relative coords)
	# #_point_tag: 1=boundary, 2=out_of_bounds, 3=search_and_destroy, 4=domination
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

# Determine tag
execute if score #_point_tag {ns}.data matches 1 run data modify storage {ns}:temp _ppos.tag set value "{ns}.element.boundary"
execute if score #_point_tag {ns}.data matches 2 run data modify storage {ns}:temp _ppos.tag set value "{ns}.element.out_of_bounds"
execute if score #_point_tag {ns}.data matches 3 run data modify storage {ns}:temp _ppos.tag set value "{ns}.element.search_and_destroy"
execute if score #_point_tag {ns}.data matches 4 run data modify storage {ns}:temp _ppos.tag set value "{ns}.element.domination"
execute if score #_point_tag {ns}.data matches 5 run data modify storage {ns}:temp _ppos.tag set value "{ns}.element.hardpoint"

function {ns}:v{version}/maps/editor/summon_point_marker with storage {ns}:temp _ppos

# Advance
data remove storage {ns}:temp _point_iter[0]
execute if data storage {ns}:temp _point_iter[0] run function {ns}:v{version}/maps/editor/summon_point_iter
""")

	write_versioned_function("maps/editor/summon_point_marker", f"""
$summon minecraft:marker $(x) $(y) $(z) {{Tags:["{ns}.map_element","$(tag)"]}}
""")

	# ── Give Editor Tools ──────────────────────────────────────────
	egg_items: list[str] = []
	for etype, einfo in ELEMENT_TYPES.items():
		slot = einfo["slot"]
		name = einfo["name"]
		color = einfo["color"]
		egg_model = einfo["egg_model"]
		egg_items.append(
			f'item replace entity @s {slot} with minecraft:bat_spawn_egg'
			f'[minecraft:item_name={{"text":"{name}","color":"{color}","italic":false}},'
			f'minecraft:item_model="{egg_model}",'
			f'minecraft:custom_data={{{ns}:{{editor:true,type:"{etype}"}}}},'
			f'minecraft:entity_data={{id:"minecraft:bat",NoAI:1b,Silent:1b,Invulnerable:1b,Tags:["{ns}.new_element","{ns}.element.{etype}"]}}]'
		)

	# DESTROY egg in offhand
	destroy_cmd = (
		f'item replace entity @s weapon.offhand with minecraft:bat_spawn_egg'
		f'[minecraft:item_name={{"text":"✘ DESTROY","color":"dark_red","italic":false,"bold":true}},'
		f'minecraft:item_model="minecraft:wither_skeleton_spawn_egg",'
		f'minecraft:custom_data={{{ns}:{{editor:true,type:"destroy"}}}},'
		f'minecraft:entity_data={{id:"minecraft:bat",NoAI:1b,Silent:1b,Invulnerable:1b,Tags:["{ns}.new_element","{ns}.element.destroy"]}}]'
	)

	give_cmds = "\n".join(egg_items) + "\n" + destroy_cmd
	write_versioned_function("maps/editor/give_tools", f"""
# Give all editor egg tools
{give_cmds}
""")

	# ── On Place (Advancement Reward) ──────────────────────────────
	write_versioned_function("maps/editor/on_place", f"""
# Revoke advancement immediately so it can trigger again
advancement revoke @s only {ns}:v{version}/maps/editor/on_place

# Only process if player is in editor mode
execute unless score @s {ns}.mp.map_edit matches 1 run return fail

# Find the newly spawned bat entity (tagged by entity_data)
execute as @n[tag={ns}.new_element] at @s run function {ns}:v{version}/maps/editor/process_element
""")

	# ── Process Placed Element ─────────────────────────────────────
	# @s = the spawned bat, at its position
	write_versioned_function("maps/editor/process_element", f"""
# Determine element type from tags and dispatch

# DESTROY handler
execute if entity @s[tag={ns}.element.destroy] run function {ns}:v{version}/maps/editor/handle_destroy
execute if entity @s[tag={ns}.element.destroy] run return run kill @s

# Base coordinates handler
execute if entity @s[tag={ns}.element.base_coordinates] run function {ns}:v{version}/maps/editor/handle_base
execute if entity @s[tag={ns}.element.base_coordinates] run return run kill @s

# Spawn handlers (need rotation from nearest player)
execute if entity @s[tag={ns}.element.red_spawn] run function {ns}:v{version}/maps/editor/handle_spawn
execute if entity @s[tag={ns}.element.red_spawn] run return run kill @s

execute if entity @s[tag={ns}.element.blue_spawn] run function {ns}:v{version}/maps/editor/handle_spawn
execute if entity @s[tag={ns}.element.blue_spawn] run return run kill @s

execute if entity @s[tag={ns}.element.general_spawn] run function {ns}:v{version}/maps/editor/handle_spawn
execute if entity @s[tag={ns}.element.general_spawn] run return run kill @s

# Point-based handlers (no rotation)
execute if entity @s[tag={ns}.element.boundary] run function {ns}:v{version}/maps/editor/handle_point
execute if entity @s[tag={ns}.element.boundary] run return run kill @s

execute if entity @s[tag={ns}.element.out_of_bounds] run function {ns}:v{version}/maps/editor/handle_point
execute if entity @s[tag={ns}.element.out_of_bounds] run return run kill @s

execute if entity @s[tag={ns}.element.search_and_destroy] run function {ns}:v{version}/maps/editor/handle_point
execute if entity @s[tag={ns}.element.search_and_destroy] run return run kill @s

execute if entity @s[tag={ns}.element.domination] run function {ns}:v{version}/maps/editor/handle_point
execute if entity @s[tag={ns}.element.domination] run return run kill @s

execute if entity @s[tag={ns}.element.hardpoint] run function {ns}:v{version}/maps/editor/handle_point
execute if entity @s[tag={ns}.element.hardpoint] run return run kill @s

# Fallback: unknown type, just kill
kill @s
""")

	# ── Handle Base Coordinates ────────────────────────────────────
	# @s = spawned bat at the new base position
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

	# ── Handle Spawn Point ─────────────────────────────────────────
	# @s = spawned bat at the spawn position
	write_versioned_function("maps/editor/handle_spawn", f"""
# Get position for the permanent marker
execute store result storage {ns}:temp _pos.x double 1 run data get entity @s Pos[0]
execute store result storage {ns}:temp _pos.y double 1 run data get entity @s Pos[1]
execute store result storage {ns}:temp _pos.z double 1 run data get entity @s Pos[2]

# Determine tag from entity
execute if entity @s[tag={ns}.element.red_spawn] run data modify storage {ns}:temp _pos.tag set value "{ns}.element.red_spawn"
execute if entity @s[tag={ns}.element.blue_spawn] run data modify storage {ns}:temp _pos.tag set value "{ns}.element.blue_spawn"
execute if entity @s[tag={ns}.element.general_spawn] run data modify storage {ns}:temp _pos.tag set value "{ns}.element.general_spawn"

# Summon permanent marker
function {ns}:v{version}/maps/editor/summon_spawn_marker with storage {ns}:temp _pos

# Store the player's rotation on the marker
execute as @n[tag={ns}.new_spawn_marker] store result entity @s data.yaw float 1 run data get entity @p[tag={ns}.map_editor] Rotation[0]
tag @n[tag={ns}.new_spawn_marker] remove {ns}.new_spawn_marker

# Determine name for message
execute if entity @s[tag={ns}.element.red_spawn] run tellraw @a[tag={ns}.map_editor] [{MGS_TAG},{{"text":"Red Spawn placed!","color":"red"}}]
execute if entity @s[tag={ns}.element.blue_spawn] run tellraw @a[tag={ns}.map_editor] [{MGS_TAG},{{"text":"Blue Spawn placed!","color":"blue"}}]
execute if entity @s[tag={ns}.element.general_spawn] run tellraw @a[tag={ns}.map_editor] [{MGS_TAG},{{"text":"General Spawn placed!","color":"yellow"}}]
""")

	# ── Handle Point Element ───────────────────────────────────────
	# @s = spawned bat at the point position
	write_versioned_function("maps/editor/handle_point", f"""
# Get position for permanent marker
execute store result storage {ns}:temp _pos.x double 1 run data get entity @s Pos[0]
execute store result storage {ns}:temp _pos.y double 1 run data get entity @s Pos[1]
execute store result storage {ns}:temp _pos.z double 1 run data get entity @s Pos[2]

# Determine tag
execute if entity @s[tag={ns}.element.boundary] run data modify storage {ns}:temp _pos.tag set value "{ns}.element.boundary"
execute if entity @s[tag={ns}.element.out_of_bounds] run data modify storage {ns}:temp _pos.tag set value "{ns}.element.out_of_bounds"
execute if entity @s[tag={ns}.element.search_and_destroy] run data modify storage {ns}:temp _pos.tag set value "{ns}.element.search_and_destroy"
execute if entity @s[tag={ns}.element.domination] run data modify storage {ns}:temp _pos.tag set value "{ns}.element.domination"
execute if entity @s[tag={ns}.element.hardpoint] run data modify storage {ns}:temp _pos.tag set value "{ns}.element.hardpoint"

# Summon permanent marker & Apply rotation (for visual debug)
function {ns}:v{version}/maps/editor/summon_point_marker with storage {ns}:temp _pos

# Messages
execute if entity @s[tag={ns}.element.boundary] run tellraw @a[tag={ns}.map_editor] [{MGS_TAG},{{"text":"Boundary corner placed!","color":"gray"}}]
execute if entity @s[tag={ns}.element.out_of_bounds] run tellraw @a[tag={ns}.map_editor] [{MGS_TAG},{{"text":"Out of Bounds marker placed!","color":"dark_red"}}]
execute if entity @s[tag={ns}.element.search_and_destroy] run tellraw @a[tag={ns}.map_editor] [{MGS_TAG},{{"text":"S&D Objective placed!","color":"gold"}}]
execute if entity @s[tag={ns}.element.domination] run tellraw @a[tag={ns}.map_editor] [{MGS_TAG},{{"text":"Domination Point placed!","color":"green"}}]
execute if entity @s[tag={ns}.element.hardpoint] run tellraw @a[tag={ns}.map_editor] [{MGS_TAG},{{"text":"Hardpoint Zone placed!","color":"dark_purple"}}]
""")

	# ── Handle DESTROY ─────────────────────────────────────────────
	# @s = spawned destroy bat, at its position
	write_versioned_function("maps/editor/handle_destroy", f"""
# Find the nearest map element marker (not a destroy bat, not the bat itself)
# We search from the destroy bat's position
execute positioned as @s as @n[tag={ns}.map_element,distance=..10] run function {ns}:v{version}/maps/editor/destroy_element
execute positioned as @s unless entity @n[tag={ns}.map_element,distance=..10] run tellraw @a[tag={ns}.map_editor] [{MGS_TAG},{{"text":"No element found within 10 blocks!","color":"red"}}]
""")

	write_versioned_function("maps/editor/destroy_element", f"""
# @s = the map_element marker to destroy
# Announce what was removed
execute if entity @s[tag={ns}.element.base_coordinates] run tellraw @a[tag={ns}.map_editor] [{MGS_TAG},{{"text":"Base Coordinates removed!","color":"light_purple"}}]
execute if entity @s[tag={ns}.element.red_spawn] run tellraw @a[tag={ns}.map_editor] [{MGS_TAG},{{"text":"Red Spawn removed!","color":"red"}}]
execute if entity @s[tag={ns}.element.blue_spawn] run tellraw @a[tag={ns}.map_editor] [{MGS_TAG},{{"text":"Blue Spawn removed!","color":"blue"}}]
execute if entity @s[tag={ns}.element.general_spawn] run tellraw @a[tag={ns}.map_editor] [{MGS_TAG},{{"text":"General Spawn removed!","color":"yellow"}}]
execute if entity @s[tag={ns}.element.boundary] run tellraw @a[tag={ns}.map_editor] [{MGS_TAG},{{"text":"Boundary corner removed!","color":"gray"}}]
execute if entity @s[tag={ns}.element.out_of_bounds] run tellraw @a[tag={ns}.map_editor] [{MGS_TAG},{{"text":"Out of Bounds removed!","color":"dark_red"}}]
execute if entity @s[tag={ns}.element.search_and_destroy] run tellraw @a[tag={ns}.map_editor] [{MGS_TAG},{{"text":"S&D Objective removed!","color":"gold"}}]
execute if entity @s[tag={ns}.element.domination] run tellraw @a[tag={ns}.map_editor] [{MGS_TAG},{{"text":"Domination Point removed!","color":"green"}}]
execute if entity @s[tag={ns}.element.hardpoint] run tellraw @a[tag={ns}.map_editor] [{MGS_TAG},{{"text":"Hardpoint Zone removed!","color":"dark_purple"}}]

# Kill the marker
kill @s
""")

	# ── Save and Exit Editor ───────────────────────────────────────
	write_versioned_function("maps/editor/save_exit", f"""
# Only process if in editor mode
execute unless score @s {ns}.mp.map_edit matches 1 run return fail

# Initialize save data with existing map info (keep id, name, description, scripts)
execute store result storage {ns}:temp map_edit.idx int 1 run scoreboard players get @s {ns}.mp.map_idx
function {ns}:v{version}/maps/editor/load_map_data with storage {ns}:temp map_edit

# Rebuild base_coordinates from marker
execute as @n[tag={ns}.map_element,tag={ns}.element.base_coordinates] at @s run function {ns}:v{version}/maps/editor/save_base

# Load base scores for relative computation
execute store result score #base_x {ns}.data run data get storage {ns}:temp map_edit.map.base_coordinates[0]
execute store result score #base_y {ns}.data run data get storage {ns}:temp map_edit.map.base_coordinates[1]
execute store result score #base_z {ns}.data run data get storage {ns}:temp map_edit.map.base_coordinates[2]

# Reset all lists
data modify storage {ns}:temp map_edit.map.boundaries set value []
data modify storage {ns}:temp map_edit.map.spawning_points.red set value []
data modify storage {ns}:temp map_edit.map.spawning_points.blue set value []
data modify storage {ns}:temp map_edit.map.spawning_points.general set value []
data modify storage {ns}:temp map_edit.map.out_of_bounds set value []
data modify storage {ns}:temp map_edit.map.search_and_destroy set value []
data modify storage {ns}:temp map_edit.map.domination set value []
data modify storage {ns}:temp map_edit.map.hardpoint set value []

# Iterate all markers and rebuild lists
execute as @e[tag={ns}.map_element,tag={ns}.element.red_spawn] at @s run function {ns}:v{version}/maps/editor/save_spawn {{path:"red"}}
execute as @e[tag={ns}.map_element,tag={ns}.element.blue_spawn] at @s run function {ns}:v{version}/maps/editor/save_spawn {{path:"blue"}}
execute as @e[tag={ns}.map_element,tag={ns}.element.general_spawn] at @s run function {ns}:v{version}/maps/editor/save_spawn {{path:"general"}}
execute as @e[tag={ns}.map_element,tag={ns}.element.boundary] at @s run function {ns}:v{version}/maps/editor/save_point {{path:"boundaries"}}
execute as @e[tag={ns}.map_element,tag={ns}.element.out_of_bounds] at @s run function {ns}:v{version}/maps/editor/save_point {{path:"out_of_bounds"}}
execute as @e[tag={ns}.map_element,tag={ns}.element.search_and_destroy] at @s run function {ns}:v{version}/maps/editor/save_point {{path:"search_and_destroy"}}
execute as @e[tag={ns}.map_element,tag={ns}.element.domination] at @s run function {ns}:v{version}/maps/editor/save_point {{path:"domination"}}
execute as @e[tag={ns}.map_element,tag={ns}.element.hardpoint] at @s run function {ns}:v{version}/maps/editor/save_point {{path:"hardpoint"}}

# Write back to storage
function {ns}:v{version}/maps/editor/write_back with storage {ns}:temp map_edit

# Cleanup and exit
function {ns}:v{version}/maps/editor/cleanup
tellraw @s [{MGS_TAG},{{"text":"Map saved!","color":"green"}}]
""")

	## Save base coordinates from marker
	write_versioned_function("maps/editor/save_base", f"""
# @s = base_coordinates marker, at its position
execute store result storage {ns}:temp map_edit.map.base_coordinates[0] int 1 run data get entity @s Pos[0]
execute store result storage {ns}:temp map_edit.map.base_coordinates[1] int 1 run data get entity @s Pos[1]
execute store result storage {ns}:temp map_edit.map.base_coordinates[2] int 1 run data get entity @s Pos[2]
""")

	## Save a spawn point (macro: path = red/blue/general)
	# @s = marker entity, at its position
	write_versioned_function("maps/editor/save_spawn", f"""
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

	## Save a point element (macro: path = boundaries/out_of_bounds/search_and_destroy/domination)
	# @s = marker entity, at its position
	write_versioned_function("maps/editor/save_point", f"""
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

	## Write map back to storage at the correct index
	write_versioned_function("maps/editor/write_back", f"""
$data modify storage {ns}:maps multiplayer[$(idx)] set from storage {ns}:temp map_edit.map
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

	# ── Editor Tick ────────────────────────────────────────────────
	# Called each tick for players in editor mode, shows particles at elements
	# and actionbar text when near an element
	write_versioned_function("maps/editor/tick", f"""
# Only run for players in editor mode
execute unless score @s {ns}.mp.map_edit matches 1 run return fail

# Show particles at each element type & their yaw
execute as @e[tag={ns}.map_element] run data modify entity @s Rotation[0] set from entity @s data.yaw
execute as @e[tag={ns}.map_element] at @s positioned ^ ^ ^0.5 run particle dust{{color:[1.0,1.0,1.0],scale:0.5}} ~ ~1.69 ~ 0.1 0.1 0.1 0 5
execute at @e[tag={ns}.map_element,tag={ns}.element.base_coordinates] run particle dust{{color:[1.0,0.0,1.0],scale:1.5}} ~ ~1 ~ 0.3 0.5 0.3 0 5
execute at @e[tag={ns}.map_element,tag={ns}.element.red_spawn] run particle dust{{color:[1.0,0.2,0.2],scale:1.0}} ~ ~1 ~ 0.2 0.5 0.2 0 3
execute at @e[tag={ns}.map_element,tag={ns}.element.blue_spawn] run particle dust{{color:[0.2,0.2,1.0],scale:1.0}} ~ ~1 ~ 0.2 0.5 0.2 0 3
execute at @e[tag={ns}.map_element,tag={ns}.element.general_spawn] run particle dust{{color:[1.0,1.0,0.2],scale:1.0}} ~ ~1 ~ 0.2 0.5 0.2 0 3
execute at @e[tag={ns}.map_element,tag={ns}.element.boundary] run particle dust{{color:[0.8,0.8,0.8],scale:1.0}} ~ ~1 ~ 0.3 0.5 0.3 0 3
execute at @e[tag={ns}.map_element,tag={ns}.element.out_of_bounds] run particle dust{{color:[0.6,0.0,0.0],scale:1.0}} ~ ~1 ~ 0.3 0.5 0.3 0 3
execute at @e[tag={ns}.map_element,tag={ns}.element.search_and_destroy] run particle dust{{color:[1.0,0.6,0.0],scale:1.0}} ~ ~1 ~ 0.3 0.5 0.3 0 3
execute at @e[tag={ns}.map_element,tag={ns}.element.domination] run particle dust{{color:[0.0,1.0,0.0],scale:1.0}} ~ ~1 ~ 0.3 0.5 0.3 0 3
execute at @e[tag={ns}.map_element,tag={ns}.element.hardpoint] run particle dust{{color:[0.5,0.0,0.5],scale:1.0}} ~ ~1 ~ 0.3 0.5 0.3 0 3

# Actionbar: show info when near an element (within 5 blocks)
execute if entity @e[tag={ns}.map_element,tag={ns}.element.base_coordinates,distance=..5] run return run title @s actionbar [{{"text":"⬟ Base Coordinates","color":"light_purple"}}]
execute if entity @e[tag={ns}.map_element,tag={ns}.element.boundary,distance=..5] run return run title @s actionbar [{{"text":"◻ Boundary Corner","color":"gray"}}]
execute if entity @e[tag={ns}.map_element,tag={ns}.element.out_of_bounds,distance=..5] run return run title @s actionbar [{{"text":"☠ Out of Bounds","color":"dark_red"}}]
execute if entity @e[tag={ns}.map_element,tag={ns}.element.search_and_destroy,distance=..5] run return run title @s actionbar [{{"text":"💣 S&D Objective","color":"gold"}}]
execute if entity @e[tag={ns}.map_element,tag={ns}.element.domination,distance=..5] run return run title @s actionbar [{{"text":"🏴 Domination Point","color":"green"}}]
execute if entity @e[tag={ns}.map_element,tag={ns}.element.hardpoint,distance=..5] run return run title @s actionbar [{{"text":"⚡ Hardpoint Zone","color":"dark_purple"}}]
execute if entity @e[tag={ns}.map_element,tag={ns}.element.red_spawn,distance=..5] run return run title @s actionbar [{{"text":"● Red Spawn","color":"red"}}]
execute if entity @e[tag={ns}.map_element,tag={ns}.element.blue_spawn,distance=..5] run return run title @s actionbar [{{"text":"● Blue Spawn","color":"blue"}}]
execute if entity @e[tag={ns}.map_element,tag={ns}.element.general_spawn,distance=..5] run return run title @s actionbar [{{"text":"● General Spawn","color":"yellow"}}]
""")

