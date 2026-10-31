
#> mgs:v5.3.0/maps/editor/spawn_walk
#
# @within	mgs:v5.3.0/maps/editor/spawn_shapes
#

tag @s add mgs.ed_walk
execute store result score #ed_wx mgs.data run data get entity @s data.walk_to[0]
scoreboard players operation #ed_wx mgs.data += #ed_x mgs.data
scoreboard players operation #ed_wx mgs.data *= #10 mgs.data
execute store result entity @s data._ed.walk.x double 0.1 run scoreboard players add #ed_wx mgs.data 5
scoreboard players operation #ed_x mgs.data *= #10 mgs.data
execute store result entity @s data._ed.walk.from_x double 0.1 run scoreboard players add #ed_x mgs.data 5
execute store result score #ed_wy mgs.data run data get entity @s data.walk_to[1]
scoreboard players operation #ed_wy mgs.data += #ed_y mgs.data
scoreboard players operation #ed_wy mgs.data *= #10 mgs.data
execute store result entity @s data._ed.walk.y double 0.1 run scoreboard players add #ed_wy mgs.data 5
scoreboard players operation #ed_y mgs.data *= #10 mgs.data
execute store result entity @s data._ed.walk.from_y double 0.1 run scoreboard players add #ed_y mgs.data 5
execute store result score #ed_wz mgs.data run data get entity @s data.walk_to[2]
scoreboard players operation #ed_wz mgs.data += #ed_z mgs.data
scoreboard players operation #ed_wz mgs.data *= #10 mgs.data
execute store result entity @s data._ed.walk.z double 0.1 run scoreboard players add #ed_wz mgs.data 5
scoreboard players operation #ed_z mgs.data *= #10 mgs.data
execute store result entity @s data._ed.walk.from_z double 0.1 run scoreboard players add #ed_z mgs.data 5

