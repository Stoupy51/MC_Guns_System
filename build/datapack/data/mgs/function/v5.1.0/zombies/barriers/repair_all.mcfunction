
#> mgs:v5.1.0/zombies/barriers/repair_all
#
# @executed	as the player & at current position
#
# @within	mgs:v5.1.0/zombies/powerups/activate/carpenter
#

execute as @e[type=minecraft:block_display,tag=mgs.barrier_display,scores={mgs.zb.barrier.state=1}] at @s run function mgs:v5.1.0/zombies/barriers/instant_repair

