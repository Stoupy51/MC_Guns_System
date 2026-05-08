
#> mgs:v5.0.1/utils/coord_stick_store_pos
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.0.1/utils/coord_stick_relative
#

execute store result score #cs_pos_x mgs.data run data get entity @s Pos[0]
execute store result score #cs_pos_y mgs.data run data get entity @s Pos[1]
execute store result score #cs_pos_z mgs.data run data get entity @s Pos[2]
kill @s

