
#> mgs:v5.1.0/zombies/mystery_box/close_lid
#
# @executed	as @e[tag=...] & at @s
#
# @within	mgs:v5.1.0/zombies/mystery_box/show_bear_result
#			mgs:v5.1.0/zombies/mystery_box/collect
#			mgs:v5.1.0/zombies/mystery_box/reset_one
#

data merge entity @n[tag=mgs.mb_lid,distance=..4] {transformation:{left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],translation:[0f,0f,0f],scale:[2.4f,2.4f,2.4f]},start_interpolation:0,interpolation_duration:8}

