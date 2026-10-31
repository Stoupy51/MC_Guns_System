
#> mgs:v5.3.0/maps/editor/spawn_shapes
#
# @within	mgs:v5.3.0/maps/editor/refresh_marker
#

tag @s remove mgs.ed_box
tag @s remove mgs.ed_walk
execute store result score #ed_x mgs.data run data get entity @s Pos[0]
execute store result score #ed_y mgs.data run data get entity @s Pos[1]
execute store result score #ed_z mgs.data run data get entity @s Pos[2]
execute if data entity @s data.activation_box[5] run function mgs:v5.3.0/maps/editor/spawn_box
execute if data entity @s data.walk_to[2] run function mgs:v5.3.0/maps/editor/spawn_walk

