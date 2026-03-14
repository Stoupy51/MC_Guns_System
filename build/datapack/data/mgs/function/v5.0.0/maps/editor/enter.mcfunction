
#> mgs:v5.0.0/maps/editor/enter
#
# @within	mgs:v5.0.0/maps/editor/menu_entry_display {idx:$(idx),mode:$(mode)}"},"hover_event":{"action":"show_text","value":"Edit this map"}},{"translate":"mgs.edit"},"]"]," ",[{"text":"[","color":"red","click_event":{"action":"run_command","command":"/function mgs:v5.0.0/maps/editor/delete {idx:$(idx),mode:$(mode)}"},"hover_event":{"action":"show_text","value":"Delete this map"}},{"translate":"mgs.delete"},"]"]]
#
# @args		idx (unknown)
#			mode (unknown)
#

# Store mode and index
$scoreboard players set @s mgs.mp.map_idx $(idx)
$data modify storage mgs:temp map_edit.mode set value "$(mode)"

# Set mode score from mode string
execute if data storage mgs:temp map_edit{mode:"multiplayer"} run scoreboard players set @s mgs.mp.map_mode 0
execute if data storage mgs:temp map_edit{mode:"zombies"} run scoreboard players set @s mgs.mp.map_mode 1
execute if data storage mgs:temp map_edit{mode:"missions"} run scoreboard players set @s mgs.mp.map_mode 2

# Mark player as in editor mode
scoreboard players set @s mgs.mp.map_edit 1
tag @s add mgs.map_editor

# Set display mode to match save mode
scoreboard players operation @s mgs.mp.map_disp = @s mgs.mp.map_mode

# Store index for macro access
execute store result storage mgs:temp map_edit.idx int 1 run scoreboard players get @s mgs.mp.map_idx

# Load map data
function mgs:v5.0.0/maps/editor/load_map_data with storage mgs:temp map_edit

# Switch to creative, clear inventory
gamemode creative @s
clear @s

# Load base_coordinates into scores for relative computation
execute store result score #base_x mgs.data run data get storage mgs:temp map_edit.map.base_coordinates[0]
execute store result score #base_y mgs.data run data get storage mgs:temp map_edit.map.base_coordinates[1]
execute store result score #base_z mgs.data run data get storage mgs:temp map_edit.map.base_coordinates[2]

# Teleport to base coordinates
execute store result storage mgs:temp _tp.x int 1 run scoreboard players get #base_x mgs.data
execute store result storage mgs:temp _tp.y int 1 run scoreboard players get #base_y mgs.data
execute store result storage mgs:temp _tp.z int 1 run scoreboard players get #base_z mgs.data
function mgs:v5.0.0/missions/tp_to_base with storage mgs:temp _tp

# Summon markers for existing elements
function mgs:v5.0.0/maps/editor/summon_existing

# Give editor tools (dispatch by mode)
function mgs:v5.0.0/maps/editor/give_tools

# Initialize zombies element defaults (only for zombies mode)
execute if score @s mgs.mp.map_mode matches 1 run function mgs:v5.0.0/maps/editor/init_zb_defaults

# Announce
tellraw @s [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"translate":"mgs.entered_map_editor_for","color":"green"},{"text":"","color":"white"},{"storage":"mgs:temp","nbt":"map_edit.map.name"}]
tellraw @s [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"translate":"mgs.place_eggs_to_add_elements_destroy_egg_hotbar_9_removes_nearest_","color":"yellow"}]
tellraw @s [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"translate":"mgs.use","color":"gray"},[{"text": "[", "color": "green", "click_event": {"action": "run_command", "command": "/function mgs:v5.0.0/maps/editor/save_exit"}, "hover_event": {"action": "show_text", "value": "Save changes and exit editor"}}, "Save & Exit", "]"],{"text":" or "},[{"text": "[", "color": "red", "click_event": {"action": "run_command", "command": "/function mgs:v5.0.0/maps/editor/exit"}, "hover_event": {"action": "show_text", "value": "Discard changes and exit editor"}}, "Exit", "]"]]

