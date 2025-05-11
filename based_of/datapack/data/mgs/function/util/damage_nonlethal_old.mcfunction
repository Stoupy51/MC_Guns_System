execute if score v0 V matches 1024.. run scoreboard players set v0 V 1023
scoreboard players operation v1 V = v0 V
scoreboard players operation v1 V %= 2 C
execute if score v1 V matches 1 run attribute @s minecraft:generic.max_health modifier add 420-69-42-1337-0 d0 -1 add
scoreboard players operation v0 V /= 2 C

scoreboard players operation v1 V = v0 V
scoreboard players operation v1 V %= 2 C
execute if score v1 V matches 1 run attribute @s minecraft:generic.max_health modifier add 420-69-42-1337-1 d1 -2 add
scoreboard players operation v0 V /= 2 C

scoreboard players operation v1 V = v0 V
scoreboard players operation v1 V %= 2 C
execute if score v1 V matches 1 run attribute @s minecraft:generic.max_health modifier add 420-69-42-1337-2 d2 -4 add
scoreboard players operation v0 V /= 2 C

scoreboard players operation v1 V = v0 V
scoreboard players operation v1 V %= 2 C
execute if score v1 V matches 1 run attribute @s minecraft:generic.max_health modifier add 420-69-42-1337-3 d3 -8 add
scoreboard players operation v0 V /= 2 C

scoreboard players operation v1 V = v0 V
scoreboard players operation v1 V %= 2 C
execute if score v1 V matches 1 run attribute @s minecraft:generic.max_health modifier add 420-69-42-1337-4 d4 -16 add
scoreboard players operation v0 V /= 2 C

scoreboard players operation v1 V = v0 V
scoreboard players operation v1 V %= 2 C
execute if score v1 V matches 1 run attribute @s minecraft:generic.max_health modifier add 420-69-42-1337-5 d5 -32 add
scoreboard players operation v0 V /= 2 C

scoreboard players operation v1 V = v0 V
scoreboard players operation v1 V %= 2 C
execute if score v1 V matches 1 run attribute @s minecraft:generic.max_health modifier add 420-69-42-1337-6 d6 -64 add
scoreboard players operation v0 V /= 2 C

scoreboard players operation v1 V = v0 V
scoreboard players operation v1 V %= 2 C
execute if score v1 V matches 1 run attribute @s minecraft:generic.max_health modifier add 420-69-42-1337-7 d7 -128 add
scoreboard players operation v0 V /= 2 C

scoreboard players operation v1 V = v0 V
scoreboard players operation v1 V %= 2 C
execute if score v1 V matches 1 run attribute @s minecraft:generic.max_health modifier add 420-69-42-1337-8 d8 -256 add
scoreboard players operation v0 V /= 2 C

scoreboard players operation v1 V = v0 V
scoreboard players operation v1 V %= 2 C
execute if score v1 V matches 1 run attribute @s minecraft:generic.max_health modifier add 420-69-42-1337-9 d9 -512 add

effect give @s minecraft:instant_health 1 0 true
effect give @s minecraft:instant_damage 1 30 true
scoreboard players operation @s damage *= -2 C
execute if score @s damage <= v3 V if score doImmResp V matches 0 run scoreboard players set doImmResp V 2
execute if score @s damage <= v3 V if score doImmResp V matches 2 run gamerule doImmediateRespawn true
tag @s add damaged