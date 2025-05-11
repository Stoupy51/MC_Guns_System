scoreboard players operation v0 V = 12ga3in S
scoreboard players operation v1 V = m590_casing_n S
scoreboard players operation v2 V = m590_casing_t S
scoreboard players operation v3 V = m590_casing_b S
execute if score @s weapon matches 330..334 anchored eyes positioned ^-0.35 ^-0.27 ^0.7 run summon item ~ ~ ~ {Tags:[newc,newcc,casing],Item:{id:"minecraft:clock",Count:1b,tag:{CustomModelData:1}},PickupDelay:32767,Age:5990,Health:1}
execute if score @s weapon matches 335 anchored eyes positioned ^-0.05 ^-0.2 ^0.6 run summon item ~ ~ ~ {Tags:[newc,newcc,casing],Item:{id:"minecraft:clock",Count:1b,tag:{CustomModelData:1}},PickupDelay:32767,Age:5990,Health:1}
execute if score @s weapon matches 336..339 anchored eyes positioned ^-0.1 ^-0.25 ^0.6 run summon item ~ ~ ~ {Tags:[newc,newcc,casing],Item:{id:"minecraft:clock",Count:1b,tag:{CustomModelData:1}},PickupDelay:32767,Age:5990,Health:1}
function mgs:guns/_common/handler_casing