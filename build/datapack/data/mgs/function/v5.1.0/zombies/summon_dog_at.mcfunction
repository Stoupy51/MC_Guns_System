
#> mgs:v5.1.0/zombies/summon_dog_at
#
# @executed	at @s
#
# @within	mgs:v5.1.0/zombies/dog_portal_strike
#

# Delivered at ground level with AI on, so no rise and no zb_rising; the strike removes the scratch tag zb_dog_new.
# step_height 1.0 as in summon_zombie_at; Wolf.applyTamingSideEffects only resets MAX_HEALTH, so a base value is safe here.
summon minecraft:wolf ~ ~ ~ {Tags:["mgs.zombie_round","mgs.zb_dog","mgs.zb_dog_new","mgs.gm_entity","mgs.nukable"],variant:"minecraft:black",PersistenceRequired:true,DeathLootTable:"minecraft:empty",Passengers:[{id:"minecraft:marker",Tags:["mgs.death_watch","mgs.gm_entity"]}],attributes:[{id:"minecraft:follow_range",base:40.0d},{id:"minecraft:step_height",base:1.0d}]}

execute as @n[tag=mgs.zb_dog_new] run function mgs:v5.1.0/zombies/types/dog

# Allied with escort traders (see escort).
team join mgs.horde @n[tag=mgs.zb_dog_new]

execute as @n[tag=mgs.zb_dog_new] run scoreboard players operation @s mgs.zb.stuck_ticks = #total_tick mgs.data
execute as @n[tag=mgs.zb_dog_new] store result score @s mgs.zb.stuck_x run data get entity @s Pos[0]
execute as @n[tag=mgs.zb_dog_new] store result score @s mgs.zb.stuck_z run data get entity @s Pos[2]
scoreboard players set @n[tag=mgs.zb_dog_new] mgs.zb.stuck_dist 4

