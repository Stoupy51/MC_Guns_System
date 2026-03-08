
#> mgs:v5.0.0/zombies/mystery_box/spawn_display
#
# @executed	at @e[tag=mgs.mystery_box_active,limit=1]
#
# @within	mgs:v5.0.0/zombies/mystery_box/try_use [ at @e[tag=mgs.mystery_box_active,limit=1] ]
#

# Spawn item display above the box
summon minecraft:item_display ~ ~1.5 ~ {Tags:["mgs.mb_display","mgs.gm_entity"],item:{id:"minecraft:nether_star",count:1},transformation:{left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],translation:[0f,0f,0f],scale:[0.7f,0.7f,0.7f]},billboard:"center"}

