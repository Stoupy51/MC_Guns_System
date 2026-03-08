
#> mgs:v5.0.0/zombies/summon_zombie_at
#
# @executed	as @n[tag=mgs.zb_near,sort=random] & at @s
#
# @within	mgs:v5.0.0/zombies/do_spawn_zombie with storage mgs:temp _zpos
#
# @args		x (unknown)
#			y (unknown)
#			z (unknown)
#			level (unknown)
#

# Summon a regular zombie (not armed)
$summon minecraft:zombie $(x) $(y) $(z) {Tags:["mgs.zombie_round","mgs.gm_entity","mgs.nukable"],CanPickUpLoot:false,PersistenceRequired:true,DeathLootTable:"minecraft:empty"}

# Scale health based on round level
$execute as @n[tag=mgs.zombie_round,tag=!mgs.zb_scaled] run function mgs:v5.0.0/zombies/scale_zombie {level:"$(level)"}

