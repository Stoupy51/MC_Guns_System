scoreboard players operation v0 V = 45acp S
scoreboard players operation v1 V = mac10_casing_n S
scoreboard players operation v2 V = mac10_casing_t S
scoreboard players operation v3 V = mac10_casing_b S
execute if score @s weapon matches 220..224 anchored eyes positioned ^-0.4 ^-0.35 ^0.7 run summon item ~ ~ ~ {Tags:[newc,newcc,casing],Item:{id:"minecraft:clock",Count:1b,tag:{CustomModelData:1}},PickupDelay:32767,Age:5990,Health:1}
execute if score @s weapon matches 225..229 anchored eyes positioned ^-0.1 ^-0.15 ^0.5 run summon item ~ ~ ~ {Tags:[newc,newcc,casing],Item:{id:"minecraft:clock",Count:1b,tag:{CustomModelData:1}},PickupDelay:32767,Age:5990,Health:1}
function mgs:guns/_common/handler_casing