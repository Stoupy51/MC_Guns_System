
#> mgs:v5.0.1/zombies/on_stuck_zombie
#
# @executed	as @e[tag=...,limit=24,sort=random]
#
# @within	mgs:v5.0.1/zombies/stuck_zombie_check
#

# @s = stuck zombie — silently remove and re-queue for spawning
scoreboard players add #zb_to_spawn mgs.data 1
tp @s ~ -10000 ~
kill @s

