
#> mgs:v5.3.0/zombies/mystery_box/lid_close
#
# @executed	as @n[tag=mgs.mb_lid,distance=..4]
#
# @within	mgs:v5.3.0/zombies/mystery_box/close_lid [ as @n[tag=mgs.mb_lid,distance=..4] ]
#

execute if score @s mgs.mb.roll matches 0 run data merge entity @s {transformation:{left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],translation:[0f,0f,0f],scale:[2.4f,2.4f,2.4f]},start_interpolation:0,interpolation_duration:8}
execute if score @s mgs.mb.roll matches 1 run data merge entity @s {transformation:{left_rotation:[0f,0f,0.7071f,0.7071f],right_rotation:[0f,0f,0f,1f],translation:[0f,0f,0f],scale:[2.4f,2.4f,2.4f]},start_interpolation:0,interpolation_duration:8}
execute if score @s mgs.mb.roll matches 2 run data merge entity @s {transformation:{left_rotation:[0f,0f,1f,0f],right_rotation:[0f,0f,0f,1f],translation:[0f,0f,0f],scale:[2.4f,2.4f,2.4f]},start_interpolation:0,interpolation_duration:8}
execute if score @s mgs.mb.roll matches 3 run data merge entity @s {transformation:{left_rotation:[0f,0f,0.7071f,-0.7071f],right_rotation:[0f,0f,0f,1f],translation:[0f,0f,0f],scale:[2.4f,2.4f,2.4f]},start_interpolation:0,interpolation_duration:8}

