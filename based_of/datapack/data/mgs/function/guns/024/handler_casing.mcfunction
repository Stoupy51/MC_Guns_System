scoreboard players operation v0 V = 762x25mm S
scoreboard players operation v1 V = ppsh41_casing_n S
scoreboard players operation v2 V = ppsh41_casing_t S
scoreboard players operation v3 V = ppsh41_casing_b S
execute if score @s weapon matches 240..244 anchored eyes positioned ^-0.38 ^-0.2 ^0.7 run summon item ~ ~ ~ {Tags:[newc,newcc,casing],Item:{id:"minecraft:clock",Count:1b,tag:{CustomModelData:1}},PickupDelay:32767,Age:5990,Health:1}
execute if score @s weapon matches 245..249 anchored eyes positioned ^0.0 ^0.0 ^0.5 run summon item ~ ~ ~ {Tags:[newc,newcc,casing],Item:{id:"minecraft:clock",Count:1b,tag:{CustomModelData:1}},PickupDelay:32767,Age:5990,Health:1}
function mgs:guns/_common/handler_casing