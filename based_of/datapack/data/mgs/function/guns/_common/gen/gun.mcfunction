# v0 damage  v1 firerate  v2 spread  v3 capacity  v4 reload

data modify storage mgs:tmp Item merge value {id:"minecraft:carrot_on_a_stick",Count:1b,tag:{Gun:1,Fresh:1,Attachment:0,Unbreakable:1b,HideFlags:36}}
scoreboard players set v6 V 1200
scoreboard players operation v6 V *= v3 V
scoreboard players operation v1 V *= v3 V
scoreboard players operation v1 V += v4 V
scoreboard players operation v6 V /= v1 V
scoreboard players set v5 V 6
scoreboard players operation v5 V *= v2 V
scoreboard players operation v5 V /= 10 C
execute in overworld run item modify block 0 -64 0 container.1 mgs:gen_gun
data modify storage mgs:tmp Item.tag.display.Lore set from block 0 -64 0 Items[{Slot:1b}].tag.display.Lore