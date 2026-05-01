
#> mgs:v5.0.0/zombies/barriers/repair_all
#
# @executed	as @e[tag=mgs.pu_item] & at @s
#
# @within	mgs:v5.0.0/zombies/powerups/activate/carpenter
#

execute as @e[tag=mgs.barrier_display,scores={mgs.zb.barrier.state=1}] at @s run function mgs:v5.0.0/zombies/barriers/instant_repair

