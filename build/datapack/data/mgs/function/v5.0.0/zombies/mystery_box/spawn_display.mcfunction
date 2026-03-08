
#> mgs:v5.0.0/zombies/mystery_box/spawn_display
#
# @executed	at @n[tag=mgs.mystery_box_active]
#
# @within	mgs:v5.0.0/zombies/mystery_box/try_use [ at @n[tag=mgs.mystery_box_active] ]
#

# Spawn item display at box level with initial small scale
summon minecraft:item_display ~ ~0.5 ~ {Tags:["mgs.mb_display","mgs.gm_entity"],item:{id:"minecraft:nether_star",count:1},transformation:{left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],translation:[0f,0f,0f],scale:[0.5f,0.5f,0.5f]},billboard:"center",interpolation_duration:10}

# Float up: set target transformation and trigger interpolation
data merge entity @n[tag=mgs.mb_display] {transformation:{translation:[0f,0.8f,0f],scale:[0.7f,0.7f,0.7f]},start_interpolation:0}

