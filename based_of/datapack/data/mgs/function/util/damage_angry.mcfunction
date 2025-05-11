scoreboard players operation v2 V = aggro_time S
scoreboard players operation v2 V -= @s d
scoreboard players operation v3 V = @s hit_by
execute as @a if score @s UID = v3 V run tag @s add angeryat
execute if score v2 V matches ..-1 run scoreboard players set v2 V 0
execute as @s[type=#mgs:mob_angry_default] run function mgs:util/damage_angry_default
execute as @s[type=#mgs:mob_angry_memories] run function mgs:util/damage_angry_memories
execute as @s[type=minecraft:villager] run function mgs:util/damage_angry_villager
tag @a[tag=angeryat] remove angeryat