
#> mgs:v5.4.2/zombies/bonus/nuke_loop
#
# @within	mgs:v5.4.2/dialog/close_then
#			mgs:zombies/bonus/nuke
#			mgs:v5.4.2/zombies/bonus/nuke_loop 1t [ scheduled ]
#

execute as @n[tag=mgs.nuked,sort=random] at @s run function mgs:v5.4.2/zombies/bonus/nuke_damage_one

execute if entity @e[tag=mgs.nuked] run schedule function mgs:v5.4.2/zombies/bonus/nuke_loop 1t

