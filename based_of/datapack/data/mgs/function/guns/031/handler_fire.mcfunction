execute if entity @e[type=minecraft:marker,tag=curr,scores={selector=1}] run playsound mgs:spas12.fire_s player @s ~ ~1000000 ~ 10000000
execute if entity @e[type=minecraft:marker,tag=curr,scores={selector=0}] run playsound mgs:spas12.fire player @s ~ ~1000000 ~ 10000000
playsound mgs:spas12.fire player @a[distance=0.01..48] ~ ~ ~ 3
function mgs:guns/_common/playsound/large
function mgs:core/fire_slow
function mgs:core/fire_slow
function mgs:core/fire_slow
execute if score enableCasing V matches 1.. if entity @e[type=minecraft:marker,tag=curr,scores={selector=1}] run function mgs:guns/031/handler_casing
scoreboard players remove @e[type=minecraft:marker,tag=curr] mag 1
scoreboard players remove @e[type=minecraft:marker,tag=curr] lim 1
scoreboard players add @s shots 1