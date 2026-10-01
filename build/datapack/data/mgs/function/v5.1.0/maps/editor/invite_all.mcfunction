
#> mgs:v5.1.0/maps/editor/invite_all
#
# @within	string in mgs:v5.1.0/maps/editor/enter
#

# The caller must be editing.
execute unless score @s mgs.mp.map_edit matches 1 run return run tellraw @s [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"translate":"mgs.you_must_be_in_map_editor_to_invite_players","color":"red"}]

# Shares the caller's session with everyone not editing.
scoreboard players set @a mgs.mp.map_edit 1
scoreboard players operation @a[scores={mgs.mp.map_edit=1}] mgs.mp.map_idx = @s mgs.mp.map_idx
scoreboard players operation @a[scores={mgs.mp.map_edit=1}] mgs.mp.map_mode = @s mgs.mp.map_mode
scoreboard players operation @a[scores={mgs.mp.map_edit=1}] mgs.mp.map_disp = @s mgs.mp.map_disp
tag @a[scores={mgs.mp.map_edit=1}] add mgs.map_editor

# Creative, with the tools synced.
gamemode creative @a[scores={mgs.mp.map_edit=1}]
clear @a[scores={mgs.mp.map_edit=1}]
execute as @a[scores={mgs.mp.map_edit=1}] run function mgs:v5.1.0/maps/editor/give_tools

execute store result storage mgs:temp _tp.x int 1 run scoreboard players get #base_x mgs.data
execute store result storage mgs:temp _tp.y int 1 run scoreboard players get #base_y mgs.data
execute store result storage mgs:temp _tp.z int 1 run scoreboard players get #base_z mgs.data
execute as @a[scores={mgs.mp.map_edit=1}] run function mgs:v5.1.0/shared/tp_to_position with storage mgs:temp _tp

tellraw @a[scores={mgs.mp.map_edit=1}] [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"translate":"mgs.editor_session_synced_for_all_players","color":"aqua"}]

