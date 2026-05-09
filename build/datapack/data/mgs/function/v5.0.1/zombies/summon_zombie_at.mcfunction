
#> mgs:v5.0.1/zombies/summon_zombie_at
#
# @executed	as @n[tag=mgs.zb_near,sort=random] & at @s
#
# @within	mgs:v5.0.1/zombies/do_spawn_zombie with storage mgs:temp _zpos
#
# @args		type (unknown)
#			level (unknown)
#

# Summon zombie 2 blocks underground with NoAI (rise animation in progress)
# Attach a marker passenger so death can be intercepted before vanilla event 60 (poof particles).
summon minecraft:zombie ~ ~-2 ~ {Tags:["mgs.zombie_round","mgs.gm_entity","mgs.nukable","mgs.zb_rising"],CanPickUpLoot:false,PersistenceRequired:true,DeathLootTable:"minecraft:empty",NoAI:1b,Passengers:[{id:"minecraft:marker",Tags:["mgs.death_watch","mgs.gm_entity"]}]}

# Apply type-specific scaling (health, speed, rise timer)
$execute as @n[tag=mgs.zombie_round,tag=!mgs.zb_scaled] run function mgs:v5.0.1/zombies/types/$(type) {level:"$(level)"}

# Initialize stuck detection scores (timestamp + XZ snapshot at spawn position)
execute as @n[tag=mgs.zombie_round,tag=mgs.zb_rising] run scoreboard players operation @s mgs.zb.stuck_ticks = #total_tick mgs.data
execute as @n[tag=mgs.zombie_round,tag=mgs.zb_rising] store result score @s mgs.zb.stuck_x run data get entity @s Pos[0]
execute as @n[tag=mgs.zombie_round,tag=mgs.zb_rising] store result score @s mgs.zb.stuck_z run data get entity @s Pos[2]

