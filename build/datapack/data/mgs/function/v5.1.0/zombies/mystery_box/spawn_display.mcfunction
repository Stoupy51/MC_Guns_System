
#> mgs:v5.1.0/zombies/mystery_box/spawn_display
#
# @executed	at @n[tag=bs.interaction.target]
#
# @within	mgs:v5.1.0/zombies/mystery_box/try_use
#

summon minecraft:item_display ~ ~-1.5 ~ {Tags:["mgs.mb_display","mgs.gm_entity","mgs.mb_display_new"],item_display:"fixed",item:{id:"minecraft:nether_star",count:1,components:{"minecraft:item_model":"air"}},transformation:{left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],translation:[0f,0f,0f],scale:[0.4f,0.4f,0.4f]},billboard:"fixed"}
tp @n[tag=mgs.mb_display_new] ~ ~-1.5 ~ ~ ~

