
#> mgs:v5.3.0/zombies/mystery_box/display_float
#
# @executed	as @e[tag=...] & at @s
#
# @within	mgs:v5.3.0/zombies/mystery_box/spin_tick_one
#

execute if score @s mgs.mb.roll matches 0 run data merge entity @s {transformation:{left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],translation:[0f,0.2f,0f],scale:[0.4f,0.4f,0.4f]},start_interpolation:0,interpolation_duration:200}
execute if score @s mgs.mb.roll matches 1 run data merge entity @s {transformation:{left_rotation:[0f,0f,0.7071f,0.7071f],right_rotation:[0f,0f,0f,1f],translation:[-0.2f,0f,0f],scale:[0.4f,0.4f,0.4f]},start_interpolation:0,interpolation_duration:200}
execute if score @s mgs.mb.roll matches 2 run data merge entity @s {transformation:{left_rotation:[0f,0f,1f,0f],right_rotation:[0f,0f,0f,1f],translation:[0f,-0.2f,0f],scale:[0.4f,0.4f,0.4f]},start_interpolation:0,interpolation_duration:200}
execute if score @s mgs.mb.roll matches 3 run data merge entity @s {transformation:{left_rotation:[0f,0f,0.7071f,-0.7071f],right_rotation:[0f,0f,0f,1f],translation:[0.2f,0f,0f],scale:[0.4f,0.4f,0.4f]},start_interpolation:0,interpolation_duration:200}

