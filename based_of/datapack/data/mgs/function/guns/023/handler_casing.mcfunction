scoreboard players operation v0 V = 46x30mm S
scoreboard players operation v1 V = mp7_casing_n S
scoreboard players operation v2 V = mp7_casing_t S
scoreboard players operation v3 V = mp7_casing_b S
execute if score @s weapon matches 230..234 anchored eyes positioned ^-0.45 ^-0.40 ^0.7 run summon item ~ ~ ~ {Tags:[newc,newcc,casing],Item:{id:"minecraft:clock",Count:1b,tag:{CustomModelData:1}},PickupDelay:32767,Age:5990,Health:1}
execute if score @s weapon matches 235 anchored eyes positioned ^-0.05 ^-0.35 ^0.5 run summon item ~ ~ ~ {Tags:[newc,newcc,casing],Item:{id:"minecraft:clock",Count:1b,tag:{CustomModelData:1}},PickupDelay:32767,Age:5990,Health:1}
execute if score @s weapon matches 236..239 anchored eyes positioned ^-0.05 ^-0.4 ^0.5 run summon item ~ ~ ~ {Tags:[newc,newcc,casing],Item:{id:"minecraft:clock",Count:1b,tag:{CustomModelData:1}},PickupDelay:32767,Age:5990,Health:1}
function mgs:guns/_common/handler_casing