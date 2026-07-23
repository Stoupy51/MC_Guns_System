
#> mgs:v5.1.0/zombies/wunderfizz/move_start
#
# @executed	as @n[tag=mgs.wf_active] & at @s
#
# @within	mgs:v5.1.0/zombies/wunderfizz/land_bear [ as @n[tag=mgs.wf_active] & at @s ]
#

execute positioned ~ ~-1.5 ~ run summon minecraft:item_display ~ ~ ~ {Tags:["mgs.wf_bear","mgs.gm_entity","mgs.wf_bear_new"],item_display:"fixed",billboard:"fixed",transformation:{left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],translation:[0f,0f,0f],scale:[0.75f,0.75f,0.75f]}}
loot replace entity @n[tag=mgs.wf_bear_new] contents loot mgs:zombies/roaming_bear
data merge entity @n[tag=mgs.wf_bear_new] {teleport_duration:2}
tag @e[tag=mgs.wf_bear_new] remove mgs.wf_bear_new
scoreboard players set #wf_move_timer mgs.data 100

