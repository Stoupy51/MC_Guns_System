scoreboard players operation v0 V = 50ae S
scoreboard players operation v1 V = deagle_casing_n S
scoreboard players operation v2 V = deagle_casing_t S
scoreboard players operation v3 V = deagle_casing_b S
execute if score @s weapon matches 130..134 anchored eyes positioned ^-0.3 ^-0.2 ^0.5 run summon item ~ ~ ~ {Tags:[newc,newcc,casing],Item:{id:"minecraft:clock",Count:1b,tag:{CustomModelData:1}},PickupDelay:32767,Age:5990,Health:1}
execute if score @s weapon matches 135..139 anchored eyes positioned ^-0.05 ^-0.05 ^0.4 run summon item ~ ~ ~ {Tags:[newc,newcc,casing],Item:{id:"minecraft:clock",Count:1b,tag:{CustomModelData:1}},PickupDelay:32767,Age:5990,Health:1}
function mgs:guns/_common/handler_casing