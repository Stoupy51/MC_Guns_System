scoreboard players operation v0 V = 338lapua S
scoreboard players operation v1 V = m24_casing_n S
scoreboard players operation v2 V = m24_casing_t S
scoreboard players operation v3 V = m24_casing_b S
execute if score @s weapon matches 440..444 anchored eyes positioned ^-0.35 ^-0.2 ^0.6 run summon item ~ ~ ~ {Tags:[newc,newcc,casing],Item:{id:"minecraft:clock",Count:1b,tag:{CustomModelData:1}},PickupDelay:32767,Age:5990,Health:1}
execute if score @s weapon matches 445 anchored eyes positioned ^-0.05 ^-0.1 ^0.5 run summon item ~ ~ ~ {Tags:[newc,newcc,casing],Item:{id:"minecraft:clock",Count:1b,tag:{CustomModelData:1}},PickupDelay:32767,Age:5990,Health:1}
execute if score @s weapon matches 446..449 anchored eyes positioned ^-0.05 ^-0.2 ^0.4 run summon item ~ ~ ~ {Tags:[newc,newcc,casing],Item:{id:"minecraft:clock",Count:1b,tag:{CustomModelData:1}},PickupDelay:32767,Age:5990,Health:1}
function mgs:guns/_common/handler_casing