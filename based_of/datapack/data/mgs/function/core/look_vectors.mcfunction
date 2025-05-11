# v1 : nv, v2 : tv, v3 : bv
execute store result score v4 V run data get entity @s Pos[0] 1000
execute store result score v5 V run data get entity @s Pos[1] 1000
execute store result score v6 V run data get entity @s Pos[2] 1000
tp @s ^ ^1 ^
execute store result score v7 V run data get entity @s Pos[0] 1000
execute store result score v8 V run data get entity @s Pos[1] 1000
execute store result score v9 V run data get entity @s Pos[2] 1000
scoreboard players operation v7 V -= v4 V
scoreboard players operation v8 V -= v5 V
scoreboard players operation v9 V -= v6 V
scoreboard players operation v7 V *= v1 V
scoreboard players operation v8 V *= v1 V
scoreboard players operation v9 V *= v1 V
tp @s ^ ^ ^1
execute store result score v10 V run data get entity @s Pos[0] 1000
execute store result score v11 V run data get entity @s Pos[1] 1000
execute store result score v12 V run data get entity @s Pos[2] 1000
scoreboard players operation v10 V -= v4 V
scoreboard players operation v11 V -= v5 V
scoreboard players operation v12 V -= v6 V
scoreboard players operation v10 V *= v2 V
scoreboard players operation v11 V *= v2 V
scoreboard players operation v12 V *= v2 V
tp @s ^1 ^ ^
execute store result score v13 V run data get entity @s Pos[0] 1000
execute store result score v14 V run data get entity @s Pos[2] 1000
scoreboard players operation v13 V -= v4 V
scoreboard players operation v14 V -= v6 V
scoreboard players operation v13 V *= v3 V
scoreboard players operation v14 V *= v3 V

scoreboard players operation v7 V += v10 V
scoreboard players operation v8 V += v11 V
scoreboard players operation v9 V += v12 V
scoreboard players operation v7 V += v13 V
scoreboard players operation v9 V += v14 V
scoreboard players operation v7 V /= 1000 C
scoreboard players operation v8 V /= 1000 C
scoreboard players operation v9 V /= 1000 C