# v0 scope type -> 0:none 1:holo 2:kobra 3:acog 4:mk4 5:pso1 6:pu
# v1 success out -1:no-wep 0:failed 1:success

scoreboard players set v2 V 0
scoreboard players set v1 V -1
execute if data storage mgs:tmp Item.tag.Gun run scoreboard players set v1 V 1
execute if score v1 V matches 1 store result score v2 V run data get storage mgs:tmp Item.tag.CustomModelData
execute if score v1 V matches 1 run function mgs:guns/_common/attach_h
execute if score v1 V matches 1 store result storage mgs:tmp Item.tag.CustomModelData int 1 run scoreboard players get v2 V
execute if score v1 V matches 1 store result storage mgs:tmp Item.tag.Attachment int 1 run scoreboard players get v0 V
execute if score v1 V matches 0 run tellraw @s {"text":"Selected weapon does not support this attachment!","color":"red"}
execute if score v1 V matches -1 run tellraw @s {"text":"No weapon selected!","color":"red"}