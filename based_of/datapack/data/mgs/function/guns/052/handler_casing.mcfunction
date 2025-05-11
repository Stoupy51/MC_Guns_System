scoreboard players operation v0 V = 762x39mm S
scoreboard players operation v1 V = rpk_casing_n S
scoreboard players operation v2 V = rpk_casing_t S
scoreboard players operation v3 V = rpk_casing_b S
execute if score @s weapon matches 520..524 anchored eyes positioned ^-0.35 ^-0.28 ^0.7 run summon item ~ ~ ~ {Tags:[newc,newcc,casing],Item:{id:"minecraft:clock",Count:1b,tag:{CustomModelData:1}},PickupDelay:32767,Age:5990,Health:1}
execute if score @s weapon matches 525 anchored eyes positioned ^-0.05 ^-0.2 ^0.5 run summon item ~ ~ ~ {Tags:[newc,newcc,casing],Item:{id:"minecraft:clock",Count:1b,tag:{CustomModelData:1}},PickupDelay:32767,Age:5990,Health:1}
execute if score @s weapon matches 526..529 anchored eyes positioned ^-0.05 ^-0.25 ^0.5 run summon item ~ ~ ~ {Tags:[newc,newcc,casing],Item:{id:"minecraft:clock",Count:1b,tag:{CustomModelData:1}},PickupDelay:32767,Age:5990,Health:1}
function mgs:guns/_common/handler_casing