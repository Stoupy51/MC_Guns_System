
#> mgs:v5.1.0/maps/editor/enter
#
# @within	string in mgs:v5.1.0/maps/editor/menu_entry_display {idx:$(idx),mode:$(mode)}
#
# @args		idx (unknown)
#			mode (unknown)
#

$scoreboard players set @s mgs.mp.map_idx $(idx)
$data modify storage mgs:temp map_edit.mode set value "$(mode)"

execute if data storage mgs:temp map_edit{mode:"multiplayer"} run scoreboard players set @s mgs.mp.map_mode 0
execute if data storage mgs:temp map_edit{mode:"zombies"} run scoreboard players set @s mgs.mp.map_mode 1
execute if data storage mgs:temp map_edit{mode:"missions"} run scoreboard players set @s mgs.mp.map_mode 2

scoreboard players set @s mgs.mp.map_edit 1
tag @s add mgs.map_editor

scoreboard players operation @s mgs.mp.map_disp = @s mgs.mp.map_mode

execute store result storage mgs:temp map_edit.idx int 1 run scoreboard players get @s mgs.mp.map_idx

function mgs:v5.1.0/maps/editor/load_map_data with storage mgs:temp map_edit

gamemode creative @s
clear @s

# For the relative coordinates.
execute store result score #base_x mgs.data run data get storage mgs:temp map_edit.map.base_coordinates[0]
execute store result score #base_y mgs.data run data get storage mgs:temp map_edit.map.base_coordinates[1]
execute store result score #base_z mgs.data run data get storage mgs:temp map_edit.map.base_coordinates[2]

execute store result storage mgs:temp _tp.x int 1 run scoreboard players get #base_x mgs.data
execute store result storage mgs:temp _tp.y int 1 run scoreboard players get #base_y mgs.data
execute store result storage mgs:temp _tp.z int 1 run scoreboard players get #base_z mgs.data
function mgs:v5.1.0/shared/tp_to_position with storage mgs:temp _tp

# Then their model displays.
function mgs:v5.1.0/maps/editor/summon_existing
function mgs:v5.1.0/maps/editor/refresh_displays

function mgs:v5.1.0/maps/editor/give_tools

# Zombies mode only.
execute if score @s mgs.mp.map_mode matches 1 run function mgs:v5.1.0/maps/editor/init_zb_defaults

tellraw @s [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"translate":"mgs.entered_map_editor_for","color":"green"},{"text":"","color":"white"},{"storage":"mgs:temp","nbt":"map_edit.map.name","interpret":true}]
tellraw @s [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"translate":"mgs.place_eggs_to_add_elements_destroy_egg_hotbar_9_removes_nearest_","color":"yellow"}]
tellraw @s [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"translate":"mgs.need_collaborators","color":"gray"},[{"text": "[", "color": "aqua", "click_event": {"action": "suggest_command", "command": "/function mgs:v5.1.0/maps/editor/invite_all"}, "hover_event": {"action": "show_text", "value": "Put all online players into this editor session"}}, "Invite All Players", "]"]]
tellraw @s [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"translate":"mgs.use","color":"gray"},[{"text": "[", "color": "green", "click_event": {"action": "suggest_command", "command": "/function mgs:v5.1.0/maps/editor/save_exit"}, "hover_event": {"action": "show_text", "value": "Save changes and exit editor"}}, "Save & Exit", "]"],{"text":" or "},[{"text": "[", "color": "red", "click_event": {"action": "suggest_command", "command": "/function mgs:v5.1.0/maps/editor/exit"}, "hover_event": {"action": "show_text", "value": "Discard changes and exit editor"}}, "Exit", "]"]]

