
#> mgs:v5.4.1/zombies/mob/preset
#
# @within	mgs:v5.4.1/dialog/close_then
#			mgs:v5.4.1/zombies/mob/setup
#

execute if entity @s[type=minecraft:zombie] run return run function mgs:v5.4.1/zombies/mob/preset/zombie
execute if entity @s[type=minecraft:wolf] run return run function mgs:v5.4.1/zombies/mob/preset/wolf

