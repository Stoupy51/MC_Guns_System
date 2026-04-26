
#> mgs:v5.0.0/zombies/summon_zombie_at
#
# @executed	as @n[tag=mgs.zb_near,sort=random] & at @s
#
# @within	mgs:v5.0.0/zombies/do_spawn_zombie with storage mgs:temp _zpos
#
# @args		type (unknown)
#			level (unknown)
#

# Summon zombie 2 blocks underground with NoAI (rise animation in progress)
summon minecraft:zombie ~ ~-2 ~ {Tags:["mgs.zombie_round","mgs.gm_entity","mgs.nukable","mgs.zb_rising"],CanPickUpLoot:false,PersistenceRequired:true,DeathLootTable:"minecraft:empty",NoAI:1b}

# Apply type-specific scaling (health, speed, rise timer)
$execute as @n[tag=mgs.zombie_round,tag=!mgs.zb_scaled] run function mgs:v5.0.0/zombies/types/$(type) {level:"$(level)"}

