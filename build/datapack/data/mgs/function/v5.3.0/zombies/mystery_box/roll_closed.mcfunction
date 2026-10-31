
#> mgs:v5.3.0/zombies/mystery_box/roll_closed
#
# @executed	as @n[tag=mgs.mb_part_new]
#
# @within	mgs:v5.3.0/zombies/mystery_box/summon_part [ as @n[tag=mgs.mb_part_new] ]
#

execute if score @s mgs.mb.roll matches 1 run return run data merge entity @s {transformation:{left_rotation:[0f,0f,0.7071f,0.7071f],right_rotation:[0f,0f,0f,1f],translation:[0f,0f,0f],scale:[2.4f,2.4f,2.4f]}}
execute if score @s mgs.mb.roll matches 2 run return run data merge entity @s {transformation:{left_rotation:[0f,0f,1f,0f],right_rotation:[0f,0f,0f,1f],translation:[0f,0f,0f],scale:[2.4f,2.4f,2.4f]}}
execute if score @s mgs.mb.roll matches 3 run return run data merge entity @s {transformation:{left_rotation:[0f,0f,0.7071f,-0.7071f],right_rotation:[0f,0f,0f,1f],translation:[0f,0f,0f],scale:[2.4f,2.4f,2.4f]}}

