# v14 : sub block distance
particle block redstone_block ~ ~ ~ 0.3 0.3 0.3 1 8 force
scoreboard players operation @s d = @e[type=minecraft:marker,tag=cbp] d
scoreboard players operation @s d += v14 V
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
execute if score v8 V matches 1.. run scoreboard players operation @s damage += v8 V
scoreboard players operation v8 V -= @e[type=minecraft:marker,tag=cbp] decay
execute if score v8 V matches ..-1 run scoreboard players set v8 V 0
scoreboard players operation @e[type=minecraft:marker,tag=cbp] damage = v8 V