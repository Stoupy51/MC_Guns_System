
#> mgs:v5.4.1/zombies/barricades/repair_all
#
# @within	mgs:v5.4.1/dialog/close_then
#			mgs:v5.4.1/zombies/powerups/activate/carpenter
#

execute as @e[type=minecraft:block_display,tag=mgs.barricade_display,scores={mgs.zb.barricade.state=1}] at @s run function mgs:v5.4.1/zombies/barricades/instant_repair

