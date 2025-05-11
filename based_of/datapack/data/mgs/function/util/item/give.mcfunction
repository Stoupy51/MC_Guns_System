execute at @s run summon minecraft:item ~ ~ ~ {PickupDelay:0s,Tags:["new"],Item:{id:"minecraft:stone",Count:1b}}
data modify entity @e[type=item,tag=new,limit=1] Item merge from storage mgs:tmp Item
data modify entity @e[type=item,tag=new,limit=1] Owner set from entity @s UUID
tag @e[type=item,tag=new] remove new