scoreboard players operation v0 V = 556x45mm S
scoreboard players operation v1 V = famas_casing_n S
scoreboard players operation v2 V = famas_casing_t S
scoreboard players operation v3 V = famas_casing_b S
execute if score @s weapon matches 70..74 anchored eyes positioned ^-0.45 ^-0.35 ^0.3 run summon item ~ ~ ~ {Tags:[newc,newcc,casing],Item:{id:"minecraft:clock",Count:1b,tag:{CustomModelData:1}},PickupDelay:32767,Age:5990,Health:1}
execute if score @s weapon matches 75..79 anchored eyes positioned ^-0.05 ^-0.3 ^0.3 run summon item ~ ~ ~ {Tags:[newc,newcc,casing],Item:{id:"minecraft:clock",Count:1b,tag:{CustomModelData:1}},PickupDelay:32767,Age:5990,Health:1}
function mgs:guns/_common/handler_casing