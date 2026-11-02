
#> mgs:v5.3.0/players/editor_invite
#
# @executed	as @a
#
# @within	string in mgs:v5.3.0/players/row_editor
#			mgs:v5.3.0/maps/editor/invite_all [ as @a ]
#

execute if score @s mgs.mp.map_edit matches 1 run return fail
execute unless entity @a[tag=mgs.map_editor] run return fail

scoreboard players operation @s mgs.mp.map_idx = @a[tag=mgs.map_editor,limit=1] mgs.mp.map_idx
scoreboard players operation @s mgs.mp.map_mode = @a[tag=mgs.map_editor,limit=1] mgs.mp.map_mode
scoreboard players operation @s mgs.mp.map_disp = @a[tag=mgs.map_editor,limit=1] mgs.mp.map_disp
scoreboard players set @s mgs.mp.map_edit 1
tag @s add mgs.map_editor

gamemode creative @s
clear @s
function mgs:v5.3.0/maps/editor/give_tools

execute store result storage mgs:temp _tp.x int 1 run scoreboard players get #base_x mgs.data
execute store result storage mgs:temp _tp.y int 1 run scoreboard players get #base_y mgs.data
execute store result storage mgs:temp _tp.z int 1 run scoreboard players get #base_z mgs.data
data modify storage mgs:temp _tp.dimension set value "minecraft:overworld"
data modify storage mgs:temp _tp.dimension set from storage mgs:temp map_edit.map.dimension
function mgs:v5.3.0/maps/editor/tp_to_map with storage mgs:temp _tp

tellraw @a[tag=mgs.map_editor] [[{"text":"","color":"gold"},"[",{"translate":"mgs","fallback":"MGS"},"] "],{"selector":"@s","color":"white"},[{"text":" ","color":"aqua"}, {"translate":"mgs.joined_the_editor_session_of","fallback":"joined the editor session of "}],{"storage":"mgs:temp","nbt":"map_edit.map.name","interpret":true}]

