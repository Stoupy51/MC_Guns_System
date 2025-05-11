summon minecraft:marker ~ ~ ~ {Tags:["lp"]}
scoreboard players operation @e[type=minecraft:marker,tag=lp,tag=!ini] UID = @s UID
scoreboard players operation @e[type=minecraft:marker,tag=lp,tag=!ini] timestamp = time V
scoreboard players add @e[type=minecraft:marker,tag=lp,tag=!ini] timestamp 3
tag @e[type=minecraft:marker,tag=lp,tag=!ini] add ini