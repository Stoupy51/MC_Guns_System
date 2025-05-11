scoreboard players operation v0 V = 762x54mm S
scoreboard players operation v1 V = svd_casing_n S
scoreboard players operation v2 V = svd_casing_t S
scoreboard players operation v3 V = svd_casing_b S
execute if score @s weapon matches 410..414 anchored eyes positioned ^-0.3 ^-0.27 ^0.7 run summon item ~ ~ ~ {Tags:[newc,newcc,casing],Item:{id:"minecraft:clock",Count:1b,tag:{CustomModelData:1}},PickupDelay:32767,Age:5990,Health:1}
execute if score @s weapon matches 415 anchored eyes positioned ^-0.05 ^-0.17 ^0.65 run summon item ~ ~ ~ {Tags:[newc,newcc,casing],Item:{id:"minecraft:clock",Count:1b,tag:{CustomModelData:1}},PickupDelay:32767,Age:5990,Health:1}
execute if score @s weapon matches 416..419 anchored eyes positioned ^-0.05 ^-0.25 ^0.5 run summon item ~ ~ ~ {Tags:[newc,newcc,casing],Item:{id:"minecraft:clock",Count:1b,tag:{CustomModelData:1}},PickupDelay:32767,Age:5990,Health:1}
function mgs:guns/_common/handler_casing