
#> mgs:v5.1.0/zombies/mystery_box/move_anim_transition
#
# @within	mgs:v5.1.0/zombies/mystery_box/move_anim_tick
#

function mgs:v5.1.0/zombies/mystery_box/move_active_position

# Before placing the chest, or it would spawn at the hidden -512 offset.
function mgs:v5.1.0/zombies/mystery_box/sync_interaction_visibility

# The arriving chest must not land on a grayed crate; refresh_disabled rebuilds the set on landing.
execute as @n[tag=mgs.mystery_box_active] at @s run kill @e[tag=mgs.mb_disabled,distance=..3]

# Height 0.7 + descent: 35 ticks x 0.18 + 34 ticks x 0.06 = 8.34 blocks.
execute as @n[tag=mgs.mystery_box_active] at @s positioned ~ ~7.54 ~ run summon minecraft:item_display ~ ~ ~ {Tags:["mgs.mb_presence","mgs.mb_base","mgs.gm_entity"],item_display:"fixed",billboard:"fixed",item:{id:"minecraft:chest",count:1,components:{"minecraft:item_model":"mgs:mystery_box_base"}},transformation:{left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],translation:[0f,0f,0f],scale:[2.4f,2.4f,2.4f]},teleport_duration:5}
execute as @n[tag=mgs.mystery_box_active] at @s positioned ~ ~7.54 ~ run summon minecraft:item_display ~ ~ ~ {Tags:["mgs.mb_presence","mgs.mb_lid","mgs.gm_entity"],item_display:"fixed",billboard:"fixed",item:{id:"minecraft:chest",count:1,components:{"minecraft:item_model":"mgs:mystery_box_lid"}},transformation:{left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],translation:[0f,0f,0f],scale:[2.4f,2.4f,2.4f]},teleport_duration:5}
execute as @n[tag=mgs.mystery_box_active] at @s as @e[tag=mgs.mb_presence,tag=!mgs.mb_temp] run data modify entity @s Rotation set from entity @n[tag=mgs.mystery_box_active] Rotation

execute at @n[tag=mgs.mystery_box_active] run particle minecraft:end_rod ~ ~3 ~ 0.1 2 0.1 0.05 20 force @a[distance=..64]
execute as @n[tag=mgs.mystery_box_active] at @s run playsound mgs:zombies/mystery_box/poof ambient @a[scores={mgs.zb.in_game=1}] ~ ~ ~ 1.0 1.0

