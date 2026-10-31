
#> mgs:v5.3.0/maps/editor/spawn_box
#
# @executed	as @e[type=minecraft:marker,tag=mgs.map_element]
#
# @within	mgs:v5.3.0/maps/editor/spawn_shapes
#

tag @s add mgs.ed_box
execute store result score #ed_x1 mgs.data run data get entity @s data.activation_box[0]
scoreboard players operation #ed_x1 mgs.data += #ed_x mgs.data
execute store result score #ed_x2 mgs.data run data get entity @s data.activation_box[3]
scoreboard players operation #ed_x2 mgs.data += #ed_x1 mgs.data
scoreboard players add #ed_x2 mgs.data 1
execute store result entity @s data._ed.box.x1 int 1 run scoreboard players get #ed_x1 mgs.data
execute store result entity @s data._ed.box.x2 int 1 run scoreboard players get #ed_x2 mgs.data
execute store result score #ed_y1 mgs.data run data get entity @s data.activation_box[1]
scoreboard players operation #ed_y1 mgs.data += #ed_y mgs.data
execute store result score #ed_y2 mgs.data run data get entity @s data.activation_box[4]
scoreboard players operation #ed_y2 mgs.data += #ed_y1 mgs.data
scoreboard players add #ed_y2 mgs.data 1
execute store result entity @s data._ed.box.y1 int 1 run scoreboard players get #ed_y1 mgs.data
execute store result entity @s data._ed.box.y2 int 1 run scoreboard players get #ed_y2 mgs.data
execute store result score #ed_z1 mgs.data run data get entity @s data.activation_box[2]
scoreboard players operation #ed_z1 mgs.data += #ed_z mgs.data
execute store result score #ed_z2 mgs.data run data get entity @s data.activation_box[5]
scoreboard players operation #ed_z2 mgs.data += #ed_z1 mgs.data
scoreboard players add #ed_z2 mgs.data 1
execute store result entity @s data._ed.box.z1 int 1 run scoreboard players get #ed_z1 mgs.data
execute store result entity @s data._ed.box.z2 int 1 run scoreboard players get #ed_z2 mgs.data

