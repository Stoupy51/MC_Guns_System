
#> mgs:v5.1.0/zombies/barricades/repair_all
#
# @executed	at @s
#
# @within	mgs:v5.1.0/zombies/powerups/activate/carpenter
#

execute as @e[type=minecraft:block_display,tag=mgs.barricade_display,scores={mgs.zb.barricade.state=1}] at @s run function mgs:v5.1.0/zombies/barricades/instant_repair

