# v12 reduction, v13 kick, v14 spread 0.01deg, v15 damage

execute anchored eyes positioned ^ ^ ^-1 run summon minecraft:marker ~ ~ ~ {Tags:[tf,slow]}
scoreboard players operation @e[type=minecraft:marker,tag=tf] UID = @s UID

execute store result score v9 V run data get entity @s Rotation[0] 1000000
execute store result score v10 V run data get entity @s Rotation[1] 1000000

function mgs:util/quick_random

execute if score enableRecoil V matches 1.. run scoreboard players operation @s kickdir = rand V
execute if score enableRecoil V matches 1.. run scoreboard players operation @s kickdir %= 5 C
execute if score enableRecoil V matches 1.. run scoreboard players operation @s kick = v13 V

scoreboard players remove rand V 5000
scoreboard players operation rand V *= v14 V
scoreboard players operation v9 V += rand V

function mgs:util/quick_random
scoreboard players remove rand V 5000
scoreboard players operation rand V *= v14 V
scoreboard players operation v10 V += rand V

scoreboard players operation v11 V = slow_bullet_ticks S

execute as @e[type=minecraft:marker,tag=tf] run function mgs:core/fire_helper
