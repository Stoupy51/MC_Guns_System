
#> mgs:v5.3.0/zombies/mystery_box/display_rest
#
# @executed	as @n[tag=mgs.mb_display_new]
#
# @within	mgs:v5.3.0/zombies/mystery_box/spawn_display [ as @n[tag=mgs.mb_display_new] ]
#

execute if score @s mgs.mb.roll matches 0 run data merge entity @s {transformation:{left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],translation:[0f,-0.6f,0f],scale:[0.4f,0.4f,0.4f]}}
execute if score @s mgs.mb.roll matches 1 run data merge entity @s {transformation:{left_rotation:[0f,0f,0.7071f,0.7071f],right_rotation:[0f,0f,0f,1f],translation:[0.6f,0f,0f],scale:[0.4f,0.4f,0.4f]}}
execute if score @s mgs.mb.roll matches 2 run data merge entity @s {transformation:{left_rotation:[0f,0f,1f,0f],right_rotation:[0f,0f,0f,1f],translation:[0f,0.6f,0f],scale:[0.4f,0.4f,0.4f]}}
execute if score @s mgs.mb.roll matches 3 run data merge entity @s {transformation:{left_rotation:[0f,0f,0.7071f,-0.7071f],right_rotation:[0f,0f,0f,1f],translation:[-0.6f,0f,0f],scale:[0.4f,0.4f,0.4f]}}

