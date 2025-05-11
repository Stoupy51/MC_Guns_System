scoreboard players operation v0 V = 556x45mm S
scoreboard players operation v1 V = m249_casing_n S
scoreboard players operation v2 V = m249_casing_t S
scoreboard players operation v3 V = m249_casing_b S
execute if score @s weapon matches 530..534 anchored eyes positioned ^-0.35 ^-0.34 ^0.7 run summon item ~ ~ ~ {Tags:[newc,newcc,casing],Item:{id:"minecraft:clock",Count:1b,tag:{CustomModelData:1}},PickupDelay:32767,Age:5990,Health:1}
execute if score @s weapon matches 535 anchored eyes positioned ^0.0 ^-0.24 ^0.7 run summon item ~ ~ ~ {Tags:[newc,newcc,casing],Item:{id:"minecraft:clock",Count:1b,tag:{CustomModelData:1}},PickupDelay:32767,Age:5990,Health:1}
execute if score @s weapon matches 536..539 anchored eyes positioned ^0.0 ^-0.3 ^0.7 run summon item ~ ~ ~ {Tags:[newc,newcc,casing],Item:{id:"minecraft:clock",Count:1b,tag:{CustomModelData:1}},PickupDelay:32767,Age:5990,Health:1}
function mgs:guns/_common/handler_casing