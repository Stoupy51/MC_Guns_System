
#> mgs:v5.3.0/zombies/mystery_box/move_anim_transition
#
# @within	mgs:v5.3.0/zombies/mystery_box/move_anim_tick
#

function mgs:v5.3.0/zombies/mystery_box/move_active_position

# Before placing the chest, or it would spawn at the hidden -512 offset.
function mgs:v5.3.0/zombies/mystery_box/sync_interaction_visibility

# The arriving chest must not land on a grayed crate; refresh_disabled rebuilds the set on landing.
execute as @n[tag=mgs.mystery_box_active] at @s run kill @e[tag=mgs.mb_disabled,distance=..3]

execute as @n[tag=mgs.mystery_box_active] at @s positioned ~ ~-0.9 ~ run function mgs:v5.3.0/zombies/mystery_box/summon_descending
execute as @e[tag=mgs.mb_presence,tag=!mgs.mb_temp] run data merge entity @s {teleport_duration:5}

execute at @n[tag=mgs.mystery_box_active] run particle minecraft:end_rod ~ ~3 ~ 0.1 2 0.1 0.05 20 force @a[distance=..64]
execute as @n[tag=mgs.mystery_box_active] at @s run playsound mgs:zombies/mystery_box/poof ambient @a[scores={mgs.zb.in_game=1}] ~ ~ ~ 1.0 1.0

