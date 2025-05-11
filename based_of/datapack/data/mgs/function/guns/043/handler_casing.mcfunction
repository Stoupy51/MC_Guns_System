scoreboard players operation v0 V = 762x54mm S
scoreboard players operation v1 V = mosin_casing_n S
scoreboard players operation v2 V = mosin_casing_t S
scoreboard players operation v3 V = mosin_casing_b S
execute if score @s weapon matches 430..434 anchored eyes positioned ^-0.35 ^-0.2 ^0.6 run summon item ~ ~ ~ {Tags:[newc,newcc,casing],Item:{id:"minecraft:clock",Count:1b,tag:{CustomModelData:1}},PickupDelay:32767,Age:5990,Health:1}
execute if score @s weapon matches 435 anchored eyes positioned ^-0.05 ^-0.1 ^0.4 run summon item ~ ~ ~ {Tags:[newc,newcc,casing],Item:{id:"minecraft:clock",Count:1b,tag:{CustomModelData:1}},PickupDelay:32767,Age:5990,Health:1}
execute if score @s weapon matches 436..439 anchored eyes positioned ^-0.05 ^-0.2 ^0.4 run summon item ~ ~ ~ {Tags:[newc,newcc,casing],Item:{id:"minecraft:clock",Count:1b,tag:{CustomModelData:1}},PickupDelay:32767,Age:5990,Health:1}
function mgs:guns/_common/handler_casing