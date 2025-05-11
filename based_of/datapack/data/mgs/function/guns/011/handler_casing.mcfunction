scoreboard players operation v0 V = 45acp S
scoreboard players operation v1 V = m1911_casing_n S
scoreboard players operation v2 V = m1911_casing_t S
scoreboard players operation v3 V = m1911_casing_b S
execute if score @s weapon matches 110..114 anchored eyes positioned ^-0.33 ^-0.25 ^0.5 run summon item ~ ~ ~ {Tags:[newc,newcc,casing],Item:{id:"minecraft:clock",Count:1b,tag:{CustomModelData:1}},PickupDelay:32767,Age:5990,Health:1}
execute if score @s weapon matches 115..119 anchored eyes positioned ^-0.05 ^-0.05 ^0.4 run summon item ~ ~ ~ {Tags:[newc,newcc,casing],Item:{id:"minecraft:clock",Count:1b,tag:{CustomModelData:1}},PickupDelay:32767,Age:5990,Health:1}
function mgs:guns/_common/handler_casing