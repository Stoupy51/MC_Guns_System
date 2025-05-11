scoreboard players operation v0 V = 50bmg S
scoreboard players operation v1 V = m82_casing_n S
scoreboard players operation v2 V = m82_casing_t S
scoreboard players operation v3 V = m82_casing_b S
execute if score @s weapon matches 420..424 anchored eyes positioned ^-0.28 ^-0.3 ^0.7 run summon item ~ ~ ~ {Tags:[newc,newcc,casing],Item:{id:"minecraft:clock",Count:1b,tag:{CustomModelData:1}},PickupDelay:32767,Age:5990,Health:1}
execute if score @s weapon matches 425 anchored eyes positioned ^-0.1 ^-0.2 ^0.6 run summon item ~ ~ ~ {Tags:[newc,newcc,casing],Item:{id:"minecraft:clock",Count:1b,tag:{CustomModelData:1}},PickupDelay:32767,Age:5990,Health:1}
execute if score @s weapon matches 426..427 anchored eyes positioned ^-0.1 ^-0.25 ^0.6 run summon item ~ ~ ~ {Tags:[newc,newcc,casing],Item:{id:"minecraft:clock",Count:1b,tag:{CustomModelData:1}},PickupDelay:32767,Age:5990,Health:1}
execute if score @s weapon matches 428..429 anchored eyes positioned ^-0.1 ^-0.35 ^0.6 run summon item ~ ~ ~ {Tags:[newc,newcc,casing],Item:{id:"minecraft:clock",Count:1b,tag:{CustomModelData:1}},PickupDelay:32767,Age:5990,Health:1}
function mgs:guns/_common/handler_casing