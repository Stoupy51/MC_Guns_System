
#> mgs:v5.4.0/utils/coord_stick_store_pos
#
# @within	mgs:v5.4.0/dialog/close_then
#			mgs:v5.4.0/maps/editor/form/box_corner
#			mgs:v5.4.0/utils/coord_stick_relative
#

execute store result score #cs_pos_x mgs.data run data get entity @s Pos[0]
execute store result score #cs_pos_y mgs.data run data get entity @s Pos[1]
execute store result score #cs_pos_z mgs.data run data get entity @s Pos[2]
kill @s

