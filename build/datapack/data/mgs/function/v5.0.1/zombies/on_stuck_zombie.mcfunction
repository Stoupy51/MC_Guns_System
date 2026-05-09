
#> mgs:v5.0.1/zombies/on_stuck_zombie
#
# @executed	as @e[tag=...,limit=24,sort=random] & at @s
#
# @within	mgs:v5.0.1/zombies/stuck_zombie_check
#

# @s = stuck zombie — silently remove and re-queue for spawning
# Kill the death_watch rider first so on_zombie_dying never fires (no powerup drop)
scoreboard players add #zb_to_spawn mgs.data 1
execute on passengers run kill @s
kill @s

