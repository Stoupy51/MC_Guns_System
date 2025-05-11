execute if score v0 V <= @s damage run tag @s add dead
scoreboard players operation @s[tag=dead] damage = v0 V
scoreboard players remove @s[tag=dead] damage 1
execute at @s[tag=dead] run summon minecraft:tnt ~ ~ ~
execute at @s[tag=dead] run tag @a[distance=..512] add dragon_gun_kill