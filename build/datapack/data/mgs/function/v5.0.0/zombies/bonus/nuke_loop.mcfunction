
#> mgs:v5.0.0/zombies/bonus/nuke_loop
#
# @executed	as @a[tag=mgs.pu_collecting,scores={mgs.zb.in_game=1},gamemode=!spectator]
#
# @within	mgs:zombies/bonus/nuke
#			mgs:v5.0.0/zombies/bonus/nuke_loop 1t [ scheduled ]
#

# Find one nuked entity and process it
execute as @n[tag=mgs.nuked,sort=random] at @s run function mgs:v5.0.0/zombies/bonus/nuke_damage_one

# Continue loop if more nuked entities exist
execute if entity @e[tag=mgs.nuked] run schedule function mgs:v5.0.0/zombies/bonus/nuke_loop 1t

# Clean up when all nuked entities are processed
execute unless entity @e[tag=mgs.nuked] run tag @a[tag=mgs.nuke_activator] remove mgs.nuke_activator

