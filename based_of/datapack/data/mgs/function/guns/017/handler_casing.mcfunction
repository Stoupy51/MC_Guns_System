scoreboard players operation v0 V = 32acp S
scoreboard players operation v1 V = vz61_casing_n S
scoreboard players operation v2 V = vz61_casing_t S
scoreboard players operation v3 V = vz61_casing_b S
execute if score @s weapon matches 170..174 anchored eyes positioned ^-0.23 ^-0.1 ^0.5 run summon item ~ ~ ~ {Tags:[newc,newcc,casing],Item:{id:"minecraft:clock",Count:1b,tag:{CustomModelData:1}},PickupDelay:32767,Age:5990,Health:1}
execute if score @s weapon matches 175..179 anchored eyes positioned ^0 ^0.05 ^0.4 run summon item ~ ~ ~ {Tags:[newc,newcc,casing],Item:{id:"minecraft:clock",Count:1b,tag:{CustomModelData:1}},PickupDelay:32767,Age:5990,Health:1}
function mgs:guns/_common/handler_casing