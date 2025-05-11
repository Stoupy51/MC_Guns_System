scoreboard players set v15 V 0
scoreboard players set v13 V 10
execute if block ~ ~ ~ #mgs:air if block ~ ~-1 ~ #mgs:air if block ~ ~1 ~ #mgs:air if block ~1 ~ ~ #mgs:air if block ~-1 ~ ~ #mgs:air if block ~ ~ ~1 #mgs:air if block ~ ~ ~-1 #mgs:air run scoreboard players set v15 V 3
execute if score v15 V matches 0 if block ~ ~ ~ #mgs:solid run scoreboard players set v15 V 2
execute if score v15 V matches 2 run scoreboard players set v13 V 0
execute if score v15 V matches 0 run function mgs:util/collide
execute if score v15 V matches 2 run scoreboard players set v0 V 0
execute if score v15 V matches 1 run scoreboard players remove @s damage 1
execute if entity @p[distance=..16,tag=!dead] run function mgs:core/rocket_player_inter
execute positioned ~-1 ~-1 ~-1 as @e[dx=1,dy=1,dz=1,type=!#mgs:mob_ex,tag=!hit] positioned ~1 ~1 ~1 run function mgs:util/hitbox_m
execute if entity @e[tag=hit] run scoreboard players remove @s damage 1
execute if entity @s[scores={damage=..0}] run scoreboard players set v0 V 0
scoreboard players operation v4 V += v1 V
scoreboard players operation v5 V += v2 V
scoreboard players operation v6 V += v3 V
particle minecraft:cloud ~ ~ ~ 0 0 0 0.05 1 force
tp @s ^ ^ ^1.0