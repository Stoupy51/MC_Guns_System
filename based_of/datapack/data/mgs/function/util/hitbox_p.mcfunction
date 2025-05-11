#v0 10 * t, v1 1000*dx, v2 1000*dy, v3 1000*dz, v4 1000*x, v5 1000*y, v6 1000*z, v13 running_t

execute store result score v7 V run data get entity @s Pos[0] 1000
execute store result score v8 V run data get entity @s Pos[1] 1000
execute store result score v9 V run data get entity @s Pos[2] 1000

tag @s add clp
execute as @a[distance=..8] if score @s UID = @e[type=minecraft:marker,tag=clp,limit=1] UID run tag @s add clp

execute as @p[tag=clp] run function mgs:util/hitbox_bare
#auxilliary commands:



execute if entity @p[tag=clp] if score v14 V <= v15 V if score v14 V < v13 V if score v14 V matches 0.. run tag @p[tag=clp] add hit
execute if entity @p[tag=clp,tag=hit] run tag @s add hit
execute if entity @p[tag=clp,tag=hit] run scoreboard players add @p[tag=own] hits 1
execute if score enablePlayerHS V matches 1 as @p[tag=hit,tag=clp] positioned ~ ~0.975 ~ run function mgs:util/damage_reg_hs
execute if score enablePlayerHS V matches 0 as @p[tag=hit,tag=clp] positioned ~ ~0.975 ~ run function mgs:util/damage_reg
tag @e[tag=clp] remove clp

