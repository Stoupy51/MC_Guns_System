""" Editor scoreboards and storage, the placement advancement and the map list per mode. """
# ruff: noqa: E501
# Imports
from stewbeet import Advancement, JsonDict, Mem, set_json_encoder, write_load_file, write_versioned_function

from ..helpers import MGS_TAG
from ..helpers.dialogs import Dialogs
from ..map_editor_defs import EDITOR_MODES
from .shared import SEP


# Functions
def write_editor_menu() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	# Scoreboards & Storage Init.
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
		f'execute unless data storage {ns}:maps {mode_info.storage_key} run data modify storage {ns}:maps {mode_info.storage_key} set value []'
		for mode_info in EDITOR_MODES.values()
	)
	write_load_file(f"""
# Initialize maps storage for all modes
{storage_init_lines}
""")

	# Advancement for egg placement detection.
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

	# Mode tab buttons (used in all list views).
	mode_tabs = ",".join(
		Dialogs.btn(mode_info.name, f"/function {ns}:v{version}/maps/editor/list/{mode_key}", mode_info.color, f"View {mode_info.name} maps")
		for mode_key, mode_info in EDITOR_MODES.items()
	)

	# Menu Entry Point.
	write_versioned_function("maps/editor/menu", f"""
# Default: show multiplayer maps
function {ns}:v{version}/maps/editor/list/multiplayer
""")

	# Per-Mode Map List.
	for mode_key, mode_info in EDITOR_MODES.items():
		sk = mode_info.storage_key
		create_btn = Dialogs.btn("+ Create New Map", f"/function {ns}:v{version}/maps/editor/create/{mode_key}", "green", f"Create a new {mode_info.name} map")

		write_versioned_function(f"maps/editor/list/{mode_key}", f"""
tellraw @s {SEP}
tellraw @s ["","       🗺 ",[{{"text":"","color":"gold","bold":true}},{{"text":"Map Editor"}}]," 🗺"]
tellraw @s {SEP}
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
tellraw @s {SEP}
""")

	# Menu Entry (recursive - one map per call).
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

	# Map Creation (per mode).
	for mode_key, mode_info in EDITOR_MODES.items():
		sk = mode_info.storage_key
		create_snbt = r"id:'my_map',name:'My Map',description:'A new map',base_coordinates:[0,64,0],start_commands:[],respawn_commands:[]"
		back_btn = Dialogs.btn("◀ Back", f"/function {ns}:v{version}/maps/editor/list/{mode_key}", "yellow", "Back to map list")

		write_versioned_function(f"maps/editor/create/{mode_key}", f"""
tellraw @s {SEP}
tellraw @s ["","  📝 ",[{{"text":"","color":"gold","bold":true}},{{"text":"Create New {mode_info.name} Map"}}]]
tellraw @s {SEP}
tellraw @s {{"text":"Run this command to create a new map:","color":"yellow"}}
tellraw @s [{{"text":"","color":"aqua","click_event":{{"action":"suggest_command","command":"/data modify storage {ns}:maps {sk} append value {{{create_snbt}}}"}}}},"/data modify storage {ns}:maps {sk} append value {{...}}"]
tellraw @s ["  ",{{"text":"⬆ Click to paste the command, then edit the id/name/description.","color":"gray","italic":true}}]
tellraw @s ""
tellraw @s ["  ",{back_btn}]
tellraw @s {SEP}
""")

	# Delete Map (macro with mode).
	write_versioned_function("maps/editor/delete", f"""
$data remove storage {ns}:maps $(mode)[$(idx)]
tellraw @s [{MGS_TAG},{{"text":"Map deleted.","color":"red"}}]

# Refresh menu for the same mode
$function {ns}:v{version}/maps/editor/list/$(mode)
""")

