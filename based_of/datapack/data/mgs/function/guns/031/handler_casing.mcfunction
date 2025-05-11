scoreboard players operation v0 V = 12ga275in S
scoreboard players operation v1 V = spas12_casing_n S
scoreboard players operation v2 V = spas12_casing_t S
scoreboard players operation v3 V = spas12_casing_b S
execute if score @s weapon matches 310..314 anchored eyes positioned ^-0.35 ^-0.3 ^0.7 run summon item ~ ~ ~ {Tags:[newc,newcc,casing],Item:{id:"minecraft:clock",Count:1b,tag:{CustomModelData:1}},PickupDelay:32767,Age:5990,Health:1}
execute if score @s weapon matches 315 anchored eyes positioned ^-0.1 ^-0.15 ^0.6 run summon item ~ ~ ~ {Tags:[newc,newcc,casing],Item:{id:"minecraft:clock",Count:1b,tag:{CustomModelData:1}},PickupDelay:32767,Age:5990,Health:1}
execute if score @s weapon matches 316..319 anchored eyes positioned ^-0.1 ^-0.3 ^0.6 run summon item ~ ~ ~ {Tags:[newc,newcc,casing],Item:{id:"minecraft:clock",Count:1b,tag:{CustomModelData:1}},PickupDelay:32767,Age:5990,Health:1}
function mgs:guns/_common/handler_casing