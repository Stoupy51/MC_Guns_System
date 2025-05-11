# v0 fill  v1 max

data modify storage mgs:tmp Item merge value {id:"minecraft:clock",Count:1b,tag:{Ammo:1,Mag:1,HideFlags:36}}
execute store result storage mgs:tmp Item.tag.Cap int 1 run scoreboard players get v1 V
execute store result storage mgs:tmp Item.tag.UID int 1 run scoreboard players get _uid_ptr UID
execute store result storage mgs:tmp Item.tag.Damage int 1 run scoreboard players get v0 V
scoreboard players add _uid_ptr UID 1
execute if score v0 V matches 0 store result score v2 V run data get storage mgs:tmp Item.tag.CustomModelData
execute if score v0 V matches 0 run scoreboard players add v2 V 5
execute if score v0 V matches 0 store result storage mgs:tmp Item.tag.CustomModelData int 1 run scoreboard players get v2 V
execute in overworld run item modify block 0 -64 0 container.1 mgs:gen_mag
data modify storage mgs:tmp Item.tag.display.Lore append from block 0 -64 0 Items[{Slot:1b}].tag.display.Lore[0]