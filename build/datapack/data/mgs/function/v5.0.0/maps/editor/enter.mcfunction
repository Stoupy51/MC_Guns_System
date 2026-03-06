
#> mgs:v5.0.0/maps/editor/enter
#
# @within	mgs:v5.0.0/maps/editor/menu_entry_display {idx:$(idx)}"},"hover_event":{"action":"show_text","value":"Edit this map"}},{"text":" "},{"text":"[Delete]","color":"red","click_event":{"action":"run_command","command":"/function mgs:v5.0.0/maps/editor/delete {idx:$(idx)}"},"hover_event":{"action":"show_text","value":"Delete this map"}}]
#
# @args		idx (unknown)
#

# Set the map index from macro argument (called via /function with {idx:N})
$scoreboard players set @s mgs.mp.map_idx $(idx)

# Mark player as in editor mode
scoreboard players set @s mgs.mp.map_edit 1
tag @s add mgs.map_editor

# Store index for macro access
execute store result storage mgs:temp map_edit.idx int 1 run scoreboard players get @s mgs.mp.map_idx

# Load map data to temp
function mgs:v5.0.0/maps/editor/load_map_data with storage mgs:temp map_edit

# Switch to creative, clear inventory
gamemode creative @s
clear @s

# Load base_coordinates into scores for relative computation
execute store result score #base_x mgs.data run data get storage mgs:temp map_edit.map.base_coordinates[0]
execute store result score #base_y mgs.data run data get storage mgs:temp map_edit.map.base_coordinates[1]
execute store result score #base_z mgs.data run data get storage mgs:temp map_edit.map.base_coordinates[2]

# Summon markers for existing elements
function mgs:v5.0.0/maps/editor/summon_existing

# Give editor tools (eggs)
function mgs:v5.0.0/maps/editor/give_tools

# Announce
tellraw @s [[{"text":"","color":"gold"},"[",{"translate": "mgs"},"] "],{"translate": "mgs.entered_map_editor_for","color":"green"},{"text":"","color":"white"},{"storage":"mgs:temp","nbt":"map_edit.map.name"}]
tellraw @s [[{"text":"","color":"gold"},"[",{"translate": "mgs"},"] "],{"translate": "mgs.place_eggs_to_add_elements_destroy_egg_slot_9_removes_nearest_el","color":"yellow"}]
tellraw @s [[{"text":"","color":"gold"},"[",{"translate": "mgs"},"] "],{"translate": "mgs.use","color":"gray"},[{"text": "[", "color": "green", "click_event": {"action": "run_command", "command": "/function mgs:v5.0.0/maps/editor/save_exit"}, "hover_event": {"action": "show_text", "value": "Save changes and exit editor"}}, "Save & Exit", "]"],{"text":" or "},[{"text": "[", "color": "red", "click_event": {"action": "run_command", "command": "/function mgs:v5.0.0/maps/editor/exit"}, "hover_event": {"action": "show_text", "value": "Discard changes and exit editor"}}, "Exit", "]"]]

