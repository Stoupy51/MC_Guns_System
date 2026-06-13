
#> mgs:v5.0.1/zombies/mystery_box/open_lid
#
# @executed	as @n[tag=mgs.mb_new]
#
# @within	mgs:v5.0.1/zombies/mystery_box/try_use
#

execute as @e[tag=mgs.mb_lid] run data merge entity @s {transformation:{left_rotation:[-0.766f,0f,0f,0.643f],right_rotation:[0f,0f,0f,1f],translation:[0f,0.415f,-0.652f],scale:[2.4f,2.4f,2.4f]},start_interpolation:0,interpolation_duration:8}

