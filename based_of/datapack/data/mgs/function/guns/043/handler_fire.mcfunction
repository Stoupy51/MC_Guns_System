playsound mgs:mosin.fire player @s ~ ~1000000 ~ 10000000
playsound mgs:mosin.fire player @a[distance=0.01..48] ~ ~ ~ 3
function mgs:guns/_common/playsound/medlarge
function mgs:core/fire
scoreboard players remove @e[type=minecraft:marker,tag=curr] mag 1
scoreboard players remove @e[type=minecraft:marker,tag=curr] lim 1
scoreboard players add @s shots 1