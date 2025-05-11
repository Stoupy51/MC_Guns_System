#v1 1000*dx, v2 1000*dy, v3 1000*dz, v4 1000*x, v5 1000*y, v6 1000*z, v13 running_t, v14 : sub block distance
scoreboard players operation @s d = @e[type=minecraft:marker,tag=cbp] d
scoreboard players operation @s d += v14 V
execute store result score v7 V run data get entity @e[type=minecraft:marker,tag=clp,limit=1] Pos[1] -1000
scoreboard players operation v7 V -= @s h
scoreboard players operation v7 V += v5 V
scoreboard players operation v8 V = v2 V
scoreboard players operation v8 V *= v14 V
scoreboard players operation v8 V /= 10 C
scoreboard players operation v7 V += v8 V
execute if score v7 V matches -400.. run particle block redstone_block ~ ~ ~ 0.3 0.3 0.3 1 10 force
execute if score v7 V matches -400.. run scoreboard players add @p[tag=own] headshots 1
execute if score v7 V matches -400.. run tag @s add hs
execute if score v7 V matches ..-501 run particle block redstone_block ~ ~ ~ 0.3 0.3 0.3 1 5 force
execute if score v7 V matches ..-501 run tag @s remove hs

scoreboard players operation v8 V = @e[type=minecraft:marker,tag=cbp] damage
execute store result score v9 V run attribute @s minecraft:generic.armor_toughness get
scoreboard players operation v9 V /= 2 C
scoreboard players operation v8 V -= v9 V
scoreboard players operation v9 V = max_armor S
scoreboard players operation v9 V *= -2 C
execute store result score v10 V run attribute @s minecraft:generic.armor get
scoreboard players operation v10 V += v9 V
scoreboard players operation v8 V *= v10 V
scoreboard players operation v8 V /= v9 V
scoreboard players operation v9 V = v8 V
execute if score v7 V matches -400.. run scoreboard players operation v9 V *= 2 C
execute if score v7 V matches -400.. run scoreboard players add v9 V 1
execute if score v9 V matches 1.. run scoreboard players operation @s damage += v9 V
scoreboard players operation v8 V -= @e[type=minecraft:marker,tag=cbp] decay
execute if score v8 V matches ..-1 run scoreboard players set v8 V 0
scoreboard players operation @e[type=minecraft:marker,tag=cbp] damage = v8 V