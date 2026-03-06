
#> mgs:v5.0.0/maps/editor/save_spawn
#
# @executed	as @e[tag=...] & at @s
#
# @within	mgs:v5.0.0/maps/editor/save_lists/multiplayer {path:"red"} [ as @e[tag=...] & at @s ]
#			mgs:v5.0.0/maps/editor/save_lists/multiplayer {path:"blue"} [ as @e[tag=...] & at @s ]
#			mgs:v5.0.0/maps/editor/save_lists/multiplayer {path:"general"} [ as @e[tag=...] & at @s ]
#
# @args		path (string)
#

# @s = marker entity, at its position
# Get absolute position
execute store result score #ax mgs.data run data get entity @s Pos[0]
execute store result score #ay mgs.data run data get entity @s Pos[1]
execute store result score #az mgs.data run data get entity @s Pos[2]

# Compute relative coordinates
scoreboard players operation #ax mgs.data -= #base_x mgs.data
scoreboard players operation #ay mgs.data -= #base_y mgs.data
scoreboard players operation #az mgs.data -= #base_z mgs.data

# Build coordinate array [x, y, z, yaw]
data modify storage mgs:temp _save_coord set value [0, 0, 0, 0.0f]
execute store result storage mgs:temp _save_coord[0] int 1 run scoreboard players get #ax mgs.data
execute store result storage mgs:temp _save_coord[1] int 1 run scoreboard players get #ay mgs.data
execute store result storage mgs:temp _save_coord[2] int 1 run scoreboard players get #az mgs.data
data modify storage mgs:temp _save_coord[3] set from entity @s data.yaw

# Append to the correct list
$data modify storage mgs:temp map_edit.map.spawning_points.$(path) append from storage mgs:temp _save_coord

