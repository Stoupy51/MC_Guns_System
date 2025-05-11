scoreboard players operation v0 V = 556x45mm S
scoreboard players operation v1 V = aug_casing_n S
scoreboard players operation v2 V = aug_casing_t S
scoreboard players operation v3 V = aug_casing_b S
execute if score @s weapon matches 40..44 anchored eyes positioned ^-0.45 ^-0.4 ^0.4 run summon item ~ ~ ~ {Tags:[newc,newcc,casing],Item:{id:"minecraft:clock",Count:1b,tag:{CustomModelData:1}},PickupDelay:32767,Age:5990,Health:1}
execute if score @s weapon matches 45..49 anchored eyes positioned ^-0.05 ^-0.3 ^0.3 run summon item ~ ~ ~ {Tags:[newc,newcc,casing],Item:{id:"minecraft:clock",Count:1b,tag:{CustomModelData:1}},PickupDelay:32767,Age:5990,Health:1}
function mgs:guns/_common/handler_casing