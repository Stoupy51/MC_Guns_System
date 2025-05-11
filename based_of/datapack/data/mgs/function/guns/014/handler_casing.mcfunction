scoreboard players operation v0 V = 9x18mm S
scoreboard players operation v1 V = makarov_casing_n S
scoreboard players operation v2 V = makarov_casing_t S
scoreboard players operation v3 V = makarov_casing_b S
execute if score @s weapon matches 140..144 anchored eyes positioned ^-0.3 ^-0.25 ^0.5 run summon item ~ ~ ~ {Tags:[newc,newcc,casing],Item:{id:"minecraft:clock",Count:1b,tag:{CustomModelData:1}},PickupDelay:32767,Age:5990,Health:1}
execute if score @s weapon matches 145..149 anchored eyes positioned ^-0.05 ^-0.05 ^0.4 run summon item ~ ~ ~ {Tags:[newc,newcc,casing],Item:{id:"minecraft:clock",Count:1b,tag:{CustomModelData:1}},PickupDelay:32767,Age:5990,Health:1}
function mgs:guns/_common/handler_casing