
#> mgs:v5.3.0/maps/editor/enter
#
# @within	mgs:v5.3.0/dialog/close_then
#			string in mgs:v5.3.0/maps/editor/menu_entry_display {idx:$(idx),mode:$(mode)}
#
# @args		mode (unknown)
#			idx (unknown)
#

# One session at a time: a second editor joins it, on its own map only.
$execute if entity @a[tag=mgs.map_editor] if data storage mgs:temp map_edit{mode:"$(mode)",idx:$(idx)} run return run function mgs:v5.3.0/players/editor_invite
execute if entity @a[tag=mgs.map_editor] run return run tellraw @s [[{"text":"","color":"gold"},"[",{"translate":"mgs","fallback":"MGS"},"] "],{"translate":"mgs.another_map_is_being_edited","fallback":"Another map is being edited: ","color":"red"},{"storage":"mgs:temp","nbt":"map_edit.map.name","interpret":true},{"translate":"mgs.join_it_or_wait_for_its_editors_to_leave","fallback":". Join it or wait for its editors to leave.","color":"red"}]

$scoreboard players set @s mgs.mp.map_idx $(idx)
$data modify storage mgs:temp map_edit.mode set value "$(mode)"

execute if data storage mgs:temp map_edit{mode:"multiplayer"} run scoreboard players set @s mgs.mp.map_mode 0
execute if data storage mgs:temp map_edit{mode:"zombies"} run scoreboard players set @s mgs.mp.map_mode 1
execute if data storage mgs:temp map_edit{mode:"missions"} run scoreboard players set @s mgs.mp.map_mode 2

function mgs:v5.3.0/maps/editor/next_session
scoreboard players set @s mgs.mp.map_edit 1
tag @s add mgs.map_editor

scoreboard players operation @s mgs.mp.map_disp = @s mgs.mp.map_mode

execute store result storage mgs:temp map_edit.idx int 1 run scoreboard players get @s mgs.mp.map_idx

function mgs:v5.3.0/maps/editor/load_map_data with storage mgs:temp map_edit
data remove storage mgs:temp map_edit.removed

# A zombies map is stored small: the markers are summoned from it whole (see map_editor/storage_format.py).
execute if score @s mgs.mp.map_mode matches 1 run data modify storage mgs:temp _inf_map set from storage mgs:temp map_edit.map
execute if score @s mgs.mp.map_mode matches 1 run function mgs:v5.3.0/maps/inflate
execute if score @s mgs.mp.map_mode matches 1 run data modify storage mgs:temp map_edit.map set from storage mgs:temp _inf_map
data remove storage mgs:temp _inf_map

gamemode creative @s
clear @s

# For the relative coordinates.
execute store result score #base_x mgs.data run data get storage mgs:temp map_edit.map.base_coordinates[0]
execute store result score #base_y mgs.data run data get storage mgs:temp map_edit.map.base_coordinates[1]
execute store result score #base_z mgs.data run data get storage mgs:temp map_edit.map.base_coordinates[2]

execute store result storage mgs:temp _tp.x int 1 run scoreboard players get #base_x mgs.data
execute store result storage mgs:temp _tp.y int 1 run scoreboard players get #base_y mgs.data
execute store result storage mgs:temp _tp.z int 1 run scoreboard players get #base_z mgs.data
data modify storage mgs:temp _tp.dimension set value "minecraft:overworld"
data modify storage mgs:temp _tp.dimension set from storage mgs:temp map_edit.map.dimension
function mgs:v5.3.0/maps/editor/tp_to_map with storage mgs:temp _tp

# The chunks within FORCE_RADIUS blocks of the base stay loaded while the map is edited: a marker in an unloaded chunk is neither summoned nor saved.
data modify storage mgs:temp map_edit.force.dimension set from storage mgs:temp _tp.dimension
execute store result storage mgs:temp map_edit.force.x1 int 1 run scoreboard players remove #base_x mgs.data 112
execute store result storage mgs:temp map_edit.force.x2 int 1 run scoreboard players add #base_x mgs.data 224
scoreboard players remove #base_x mgs.data 112
execute store result storage mgs:temp map_edit.force.z1 int 1 run scoreboard players remove #base_z mgs.data 112
execute store result storage mgs:temp map_edit.force.z2 int 1 run scoreboard players add #base_z mgs.data 224
scoreboard players remove #base_z mgs.data 112
function mgs:v5.3.0/maps/editor/force_load with storage mgs:temp map_edit.force

# The markers once those chunks have loaded; no save until then.
data modify storage mgs:temp map_edit.loading set value 1b
schedule function mgs:v5.3.0/maps/editor/summon_all 40t replace

function mgs:v5.3.0/maps/editor/give_tools

# Zombies mode only.
execute if score @s mgs.mp.map_mode matches 1 run function mgs:v5.3.0/maps/editor/init_zb_defaults

tellraw @s [[{"text":"","color":"gold"},"[",{"translate":"mgs","fallback":"MGS"},"] "],{"translate":"mgs.entered_map_editor_for","fallback":"Entered map editor for: ","color":"green"},{"text":"","color":"white"},{"storage":"mgs:temp","nbt":"map_edit.map.name","interpret":true}]
tellraw @s [[{"text":"","color":"gold"},"[",{"translate":"mgs","fallback":"MGS"},"] "],{"translate":"mgs.place_eggs_to_add_elements_destroy_egg_hotbar_9_removes_nearest_","fallback":"Place eggs to add elements. DESTROY egg (hotbar 9) removes nearest element.","color":"yellow"}]
tellraw @s [[{"text":"","color":"gold"},"[",{"translate":"mgs","fallback":"MGS"},"] "],{"translate":"mgs.need_collaborators","fallback":"Need collaborators? ","color":"gray"},[{"text": "[", "color": "aqua", "click_event": {"action": "run_command", "command": "/function mgs:v5.3.0/maps/editor/invite"}, "hover_event": {"action": "show_text", "value": "Choose who joins this editor session"}}, "Invite Players", "]"]]
tellraw @s [[{"text":"","color":"gold"},"[",{"translate":"mgs","fallback":"MGS"},"] "],{"translate":"mgs.use","fallback":"Use ","color":"gray"},[{"text": "[", "color": "green", "click_event": {"action": "suggest_command", "command": "/function mgs:v5.3.0/maps/editor/save_exit"}, "hover_event": {"action": "show_text", "value": "Save changes and exit editor"}}, "Save & Exit", "]"],{"text":" or "},[{"text": "[", "color": "red", "click_event": {"action": "suggest_command", "command": "/function mgs:v5.3.0/maps/editor/exit"}, "hover_event": {"action": "show_text", "value": "Discard changes and exit editor"}}, "Exit", "]"]]

