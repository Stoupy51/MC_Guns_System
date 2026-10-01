
#> mgs:v5.1.0/maps/editor/summon_zb_object_iter
#
# @within	mgs:v5.1.0/maps/editor/summon_existing/zombies
#			mgs:v5.1.0/maps/editor/summon_zb_object_iter
#

execute store result score #rx mgs.data run data get storage mgs:temp _zb_iter[0].pos[0]
execute store result score #ry mgs.data run data get storage mgs:temp _zb_iter[0].pos[1]
execute store result score #rz mgs.data run data get storage mgs:temp _zb_iter[0].pos[2]

scoreboard players operation #rx mgs.data += #base_x mgs.data
scoreboard players operation #ry mgs.data += #base_y mgs.data
scoreboard players operation #rz mgs.data += #base_z mgs.data

execute store result storage mgs:temp _zbpos.x double 1 run scoreboard players get #rx mgs.data
execute store result storage mgs:temp _zbpos.y double 1 run scoreboard players get #ry mgs.data
execute store result storage mgs:temp _zbpos.z double 1 run scoreboard players get #rz mgs.data

data modify storage mgs:temp _zbpos.tag set from storage mgs:temp _zb_iter_tag

function mgs:v5.1.0/maps/editor/summon_zb_marker with storage mgs:temp _zbpos

execute as @n[tag=mgs.new_zb_marker] run data modify entity @s data set from storage mgs:temp _zb_iter[0]

# Fields older maps lack, which the config UI would show as blank rows.
execute as @n[tag=mgs.new_zb_marker] run function mgs:v5.1.0/maps/editor/backfill_zb_defaults

# The entity Rotation is synced too, for model displays.
execute if data storage mgs:temp _zb_iter[0].rotation as @n[tag=mgs.new_zb_marker] run data modify entity @s data.yaw set from storage mgs:temp _zb_iter[0].rotation[0]
execute as @n[tag=mgs.new_zb_marker] run data modify entity @s Rotation[0] set from entity @s data.yaw

tag @e[tag=mgs.new_zb_marker] remove mgs.new_zb_marker

data remove storage mgs:temp _zb_iter[0]
execute if data storage mgs:temp _zb_iter[0] run function mgs:v5.1.0/maps/editor/summon_zb_object_iter

