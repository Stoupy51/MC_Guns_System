scoreboard players operation v0 V = 9x19mm S
scoreboard players operation v1 V = glock17_casing_n S
scoreboard players operation v2 V = glock17_casing_t S
scoreboard players operation v3 V = glock17_casing_b S
execute if score @s weapon matches 150..154 anchored eyes positioned ^-0.35 ^-0.27 ^0.5 run summon item ~ ~ ~ {Tags:[newc,newcc,casing],Item:{id:"minecraft:clock",Count:1b,tag:{CustomModelData:1}},PickupDelay:32767,Age:5990,Health:1}
execute if score @s weapon matches 155..159 anchored eyes positioned ^-0.05 ^0.0 ^0.4 run summon item ~ ~ ~ {Tags:[newc,newcc,casing],Item:{id:"minecraft:clock",Count:1b,tag:{CustomModelData:1}},PickupDelay:32767,Age:5990,Health:1}
function mgs:guns/_common/handler_casing