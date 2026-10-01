
#> mgs:v5.1.0/maps/editor/summon_spawn_iter
#
# @within	mgs:v5.1.0/maps/editor/summon_existing/multiplayer
#			mgs:v5.1.0/maps/editor/summon_existing/missions
#			mgs:v5.1.0/maps/editor/summon_spawn_iter
#

execute store result score #rx mgs.data run data get storage mgs:temp _spawn_iter[0][0]
execute store result score #ry mgs.data run data get storage mgs:temp _spawn_iter[0][1]
execute store result score #rz mgs.data run data get storage mgs:temp _spawn_iter[0][2]

scoreboard players operation #rx mgs.data += #base_x mgs.data
scoreboard players operation #ry mgs.data += #base_y mgs.data
scoreboard players operation #rz mgs.data += #base_z mgs.data

data modify storage mgs:temp _spawn_rot.yaw set from storage mgs:temp _spawn_iter[0][3]

execute store result storage mgs:temp _spos.x double 1 run scoreboard players get #rx mgs.data
execute store result storage mgs:temp _spos.y double 1 run scoreboard players get #ry mgs.data
execute store result storage mgs:temp _spos.z double 1 run scoreboard players get #rz mgs.data

data modify storage mgs:temp _spos.tag set from storage mgs:temp _spawn_iter_tag

function mgs:v5.1.0/maps/editor/summon_spawn_marker with storage mgs:temp _spos

execute as @n[tag=mgs.new_spawn_marker] run data modify entity @s data.yaw set from storage mgs:temp _spawn_rot.yaw
tag @e[tag=mgs.new_spawn_marker] remove mgs.new_spawn_marker

data remove storage mgs:temp _spawn_iter[0]
execute if data storage mgs:temp _spawn_iter[0] run function mgs:v5.1.0/maps/editor/summon_spawn_iter

