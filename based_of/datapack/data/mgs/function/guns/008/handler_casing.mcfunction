scoreboard players operation v0 V = 762x51mm S
scoreboard players operation v1 V = scar17_casing_n S
scoreboard players operation v2 V = scar17_casing_t S
scoreboard players operation v3 V = scar17_casing_b S
execute if score @s weapon matches 80..84 anchored eyes positioned ^-0.32 ^-0.3 ^0.7 run summon item ~ ~ ~ {Tags:[newc,newcc,casing],Item:{id:"minecraft:clock",Count:1b,tag:{CustomModelData:1}},PickupDelay:32767,Age:5990,Health:1}
execute if score @s weapon matches 85..89 anchored eyes positioned ^-0.05 ^-0.25 ^0.5 run summon item ~ ~ ~ {Tags:[newc,newcc,casing],Item:{id:"minecraft:clock",Count:1b,tag:{CustomModelData:1}},PickupDelay:32767,Age:5990,Health:1}
function mgs:guns/_common/handler_casing