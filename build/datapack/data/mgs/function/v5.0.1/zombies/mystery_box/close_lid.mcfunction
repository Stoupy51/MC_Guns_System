
#> mgs:v5.0.1/zombies/mystery_box/close_lid
#
# @within	mgs:v5.0.1/zombies/mystery_box/show_bear_result
#			mgs:v5.0.1/zombies/mystery_box/reset
#

execute as @e[tag=mgs.mb_lid] run data merge entity @s {transformation:{left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],translation:[0f,0f,0f],scale:[2.4f,2.4f,2.4f]},start_interpolation:0,interpolation_duration:8}

