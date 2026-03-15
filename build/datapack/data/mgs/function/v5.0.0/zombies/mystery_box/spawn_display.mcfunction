
#> mgs:v5.0.0/zombies/mystery_box/spawn_display
#
# @executed	at @n[tag=mgs.mystery_box_active]
#
# @within	mgs:v5.0.0/zombies/mystery_box/try_use [ at @n[tag=mgs.mystery_box_active] ]
#

# Spawn item display at box level with small scale
summon minecraft:item_display ~ ~0.5 ~ {Tags:["mgs.mb_display","mgs.gm_entity","mgs.mb_display_new"],item:{id:"minecraft:nether_star",count:1,components:{"minecraft:item_model":"air"}},transformation:{left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],translation:[0f,0f,0f],scale:[0.5f,0.5f,0.5f]},billboard:"fixed"}

# Apply interpolation a few ticks later to avoid same-tick spawn interpolation glitches.
schedule function mgs:v5.0.0/zombies/mystery_box/spawn_display_finalize 5t append

