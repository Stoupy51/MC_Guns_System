scoreboard players set v15 V 0
scoreboard players set v13 V 10
execute if block ~ ~ ~ #mgs:air if block ~ ~-1 ~ #mgs:air if block ~ ~1 ~ #mgs:air if block ~1 ~ ~ #mgs:air if block ~-1 ~ ~ #mgs:air if block ~ ~ ~1 #mgs:air if block ~ ~ ~-1 #mgs:air run scoreboard players set v15 V 1
execute if score v15 V matches 0 if block ~ ~ ~ #mgs:activate align xyz positioned ~0.5 ~0.5 ~0.5 run function mgs:core/activate_blocks
execute if score v15 V matches 0 if block ~ ~ ~ #mgs:solid run scoreboard players set v15 V 3
execute if score v15 V matches 3 run scoreboard players set v13 V 0
execute if score v15 V matches 0 run function mgs:util/collide
execute if score v15 V matches 3.. run scoreboard players set v0 V 0
execute if score v15 V matches 2 run scoreboard players operation @s damage -= @s decay
execute if entity @s[scores={damage=..0}] run scoreboard players set v0 V 0
execute if score v15 V matches 3.. run particle crit ~ ~ ~ 0 0 0 1 3 force @a
execute if entity @p[distance=..16,tag=!dead] run function mgs:core/bullet_player_inter
execute if score @s damage matches 1.. positioned ~-1 ~-1 ~-1 as @e[dx=1,dy=1,dz=1,type=!#mgs:mob_ex,tag=!hit] positioned ~1 ~1 ~1 run function mgs:util/hitbox_m

scoreboard players operation v4 V += v1 V
scoreboard players operation v5 V += v2 V
scoreboard players operation v6 V += v3 V
scoreboard players operation @s d += v13 V