
#> mgs:v5.4.2/maps/editor/form/box_first
#
# @within	mgs:v5.4.2/dialog/close_then
#			mgs:v5.4.2/maps/editor/form/box_corner
#

data modify storage mgs:temp coord_stick.abox set value [0,0,0]
execute store result storage mgs:temp coord_stick.abox[0] int 1 run scoreboard players get #cs_pos_x mgs.data
execute store result storage mgs:temp coord_stick.abox[1] int 1 run scoreboard players get #cs_pos_y mgs.data
execute store result storage mgs:temp coord_stick.abox[2] int 1 run scoreboard players get #cs_pos_z mgs.data
tellraw @a[tag=mgs.coord_stick_user] [[{"text":"","color":"gold"},"[",{"translate":"mgs","fallback":"MGS"},"] "],{"translate":"mgs.first_corner_saved_now_the_opposite_one","fallback":"First corner saved: now the opposite one.","color":"yellow"}]

