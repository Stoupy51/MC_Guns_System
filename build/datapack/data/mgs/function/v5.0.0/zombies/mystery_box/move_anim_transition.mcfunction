
#> mgs:v5.0.0/zombies/mystery_box/move_anim_transition
#
# @within	mgs:v5.0.0/zombies/mystery_box/move_anim_tick
#

# Pick new active position
function mgs:v5.0.0/zombies/mystery_box/move_active_position

# Spawn new chest display above the new active position (height = 0.7 + descent total)
# Fast: 35t * 0.18 = 6.3 blocks, Slow: 34t * 0.06 = 2.04 blocks, Total = 8.34
execute as @n[tag=mgs.mystery_box_active] at @s positioned ~ ~9.04 ~ run summon minecraft:item_display ~ ~ ~ {Tags:["mgs.mb_presence","mgs.gm_entity"],item_display:"fixed",billboard:"fixed",item:{id:"minecraft:chest",count:1},transformation:{left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],translation:[0f,0f,0f],scale:[0.85f,0.85f,0.85f]},teleport_duration:5}
execute as @n[tag=mgs.mystery_box_active] at @s as @n[tag=mgs.mb_presence] run data modify entity @s Rotation set from entity @n[tag=mgs.mystery_box_active] Rotation

# Light beam particles at new location
execute at @n[tag=mgs.mystery_box_active] run particle minecraft:end_rod ~ ~3 ~ 0.1 2 0.1 0.05 20 force
execute as @n[tag=mgs.mystery_box_active] at @s run function mgs:v5.0.0/zombies/feedback/sound_box_poof

