scoreboard players operation v0 V = 9x19mm S
scoreboard players operation v1 V = sten_casing_n S
scoreboard players operation v2 V = sten_casing_t S
scoreboard players operation v3 V = sten_casing_b S
execute if score @s weapon matches 250..254 anchored eyes positioned ^-0.38 ^-0.35 ^0.7 run summon item ~ ~ ~ {Tags:[newc,newcc,casing],Item:{id:"minecraft:clock",Count:1b,tag:{CustomModelData:1}},PickupDelay:32767,Age:5990,Health:1}
execute if score @s weapon matches 255..259 anchored eyes positioned ^-0.1 ^-0.12 ^0.5 run summon item ~ ~ ~ {Tags:[newc,newcc,casing],Item:{id:"minecraft:clock",Count:1b,tag:{CustomModelData:1}},PickupDelay:32767,Age:5990,Health:1}
function mgs:guns/_common/handler_casing