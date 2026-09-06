
#> mgs:v5.1.0/zombies/bonus/nuke_loop
#
# @executed	at @s
#
# @within	mgs:zombies/bonus/nuke
#			mgs:v5.1.0/zombies/bonus/nuke_loop 1t [ scheduled ]
#

# Find one nuked entity and process it
execute as @n[tag=mgs.nuked,sort=random] at @s run function mgs:v5.1.0/zombies/bonus/nuke_damage_one

# Continue loop if more nuked entities exist
execute if entity @e[tag=mgs.nuked] run schedule function mgs:v5.1.0/zombies/bonus/nuke_loop 1t

## sourceMappingURL=nuke_loop.mcfunction.map
