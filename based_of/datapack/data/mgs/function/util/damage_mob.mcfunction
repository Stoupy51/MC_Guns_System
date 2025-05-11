execute if entity @s[type=!#mgs:mob_ex] run scoreboard players operation v1 V = @s hit_by

scoreboard players operation @s[type=#mgs:mob_boss] damage /= 2 C
execute store result score v0 V run data get entity @s Health
execute if entity @s[type=minecraft:ender_dragon] run function mgs:util/damage_dragon
execute if score v0 V <= @s damage run kill @s
execute if entity @s[type=#mgs:mob_angry] run function mgs:util/damage_angry
scoreboard players operation v0 V -= @s damage
scoreboard players set @s damage 0
execute store result entity @s Health float 1 run scoreboard players get v0 V
data merge entity @s {ActiveEffects:[{Id: 6b, Duration: 1, ShowParticles: 0b, Amplifier:30b},{Id: 7b, Duration: 1, ShowParticles: 0b, Amplifier:30b}]}

execute if score v0 V matches ..0 as @a if score @s UID = v1 V run scoreboard players add @s mobkills 1
execute if score v0 V matches ..0 as @a if score @s UID = v1 V run scoreboard players add @s mobgunkills 1