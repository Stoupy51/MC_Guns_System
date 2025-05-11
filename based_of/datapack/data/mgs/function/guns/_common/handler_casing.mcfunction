# v0 : variant, v1 : nv, v2 : tv, v3 : bv
execute unless entity @e[type=minecraft:marker,tag=lv] run summon minecraft:marker ~ 0 ~ {Tags:[lv,ini],Duration:20}
tp @e[type=minecraft:marker,tag=lv] @s
scoreboard players operation rand V %= 40 C
scoreboard players operation rand V -= 20 C
scoreboard players operation v2 V += rand V
execute as @e[type=minecraft:marker,tag=lv] at @s run function mgs:core/look_vectors
scoreboard players add v0 V 11000
data modify storage mgs:tmp data set value {Item:{tag:{}},Motion:[0.0,0.0,0.0]}
execute store result storage mgs:tmp data.Item.tag.CustomModelData int 1 run scoreboard players get v0 V
execute store result storage mgs:tmp data.Motion[0] double 0.001 run scoreboard players get v7 V
execute store result storage mgs:tmp data.Motion[1] double 0.001 run scoreboard players get v8 V
execute store result storage mgs:tmp data.Motion[2] double 0.001 run scoreboard players get v9 V
data modify entity @e[type=minecraft:item,tag=newcc,tag=casing,limit=1] {} merge from storage mgs:tmp data
tag @e[type=minecraft:item,tag=newcc] remove newcc