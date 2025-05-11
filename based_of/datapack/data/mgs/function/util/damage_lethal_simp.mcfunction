scoreboard players operation v10 V = @s hit_by
scoreboard players operation v11 V = @s UID

kill @s
execute as @e[type=minecraft:marker,tag=lp] if score @s UID = v11 V run kill @s
tag @s add dead

execute as @a if score @s UID = v10 V run scoreboard players add @s kills 1
execute as @a if score @s UID = v10 V run scoreboard players add @s gunkills 1