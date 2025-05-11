summon minecraft:snowball ~ ~ ~ {Item:{id:"minecraft:clock",Count:1b,tag:{CustomModelData:1}},Motion:[0.1,0.0,0.0],Tags:[activator]}
summon minecraft:snowball ~ ~ ~ {Item:{id:"minecraft:clock",Count:1b,tag:{CustomModelData:1}},Motion:[0.0,0.0,0.1],Tags:[activator]}
execute as @e[type=minecraft:snowball,tag=activator] run data modify entity @s Owner set from entity @p[tag=own] UUID