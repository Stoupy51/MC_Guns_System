
#> mgs:v5.0.0/maps/editor/save_point
#
# @executed	as @e[tag=...] & at @s
#
# @within	mgs:v5.0.0/maps/editor/save_exit {path:"boundaries"} [ as @e[tag=...] & at @s ]
#			mgs:v5.0.0/maps/editor/save_exit {path:"out_of_bounds"} [ as @e[tag=...] & at @s ]
#			mgs:v5.0.0/maps/editor/save_exit {path:"search_and_destroy"} [ as @e[tag=...] & at @s ]
#			mgs:v5.0.0/maps/editor/save_exit {path:"domination"} [ as @e[tag=...] & at @s ]
#
# @args		path (string)
#

# Get absolute position
execute store result score #ax mgs.data run data get entity @s Pos[0]
execute store result score #ay mgs.data run data get entity @s Pos[1]
execute store result score #az mgs.data run data get entity @s Pos[2]

# Compute relative coordinates
scoreboard players operation #ax mgs.data -= #base_x mgs.data
scoreboard players operation #ay mgs.data -= #base_y mgs.data
scoreboard players operation #az mgs.data -= #base_z mgs.data

# Build coordinate array [x, y, z]
data modify storage mgs:temp _save_coord set value [0, 0, 0]
execute store result storage mgs:temp _save_coord[0] int 1 run scoreboard players get #ax mgs.data
execute store result storage mgs:temp _save_coord[1] int 1 run scoreboard players get #ay mgs.data
execute store result storage mgs:temp _save_coord[2] int 1 run scoreboard players get #az mgs.data

# Append to the correct list
$data modify storage mgs:temp map_edit.map.$(path) append from storage mgs:temp _save_coord

