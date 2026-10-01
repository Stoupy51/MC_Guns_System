
#> mgs:v5.1.0/zombies/bonus/nuke_loop
#
# @executed	at @s
#
# @within	mgs:zombies/bonus/nuke
#			mgs:v5.1.0/zombies/bonus/nuke_loop 1t [ scheduled ]
#

execute as @n[tag=mgs.nuked,sort=random] at @s run function mgs:v5.1.0/zombies/bonus/nuke_damage_one

execute if entity @e[tag=mgs.nuked] run schedule function mgs:v5.1.0/zombies/bonus/nuke_loop 1t

