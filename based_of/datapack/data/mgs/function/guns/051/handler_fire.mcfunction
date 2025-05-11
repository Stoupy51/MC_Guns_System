playsound mgs:rpg7.fire player @s ~ ~1000000 ~ 10000000
playsound mgs:rpg7.fire player @a[distance=0.01..48] ~ ~ ~ 3
function mgs:guns/_common/playsound/rocket_crack
function mgs:core/fire_rocket
particle minecraft:cloud ^ ^ ^1.0 0.1 0.1 0.1 0.6 5 force
scoreboard players remove @e[type=minecraft:marker,tag=curr] mag 1
scoreboard players remove @e[type=minecraft:marker,tag=curr] lim 1
scoreboard players add @s shots 1