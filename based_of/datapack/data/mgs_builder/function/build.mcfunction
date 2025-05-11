execute if score builderGun V matches 0 run data remove storage mgs:tmp Item 
execute if score builderGun V matches 01..10 run function mgs_builder:sub_build/1-10
execute if score builderGun V matches 11..20 run function mgs_builder:sub_build/11-20
execute if score builderGun V matches 21..30 run function mgs_builder:sub_build/21-30
execute if score builderGun V matches 31..40 run function mgs_builder:sub_build/31-40
execute if score builderGun V matches 41..50 run function mgs_builder:sub_build/41-50
execute if score builderGun V matches 51..60 run function mgs_builder:sub_build/51-60

scoreboard players operation v0 V = builderAtt V
function mgs:guns/_common/attach
execute if score v1 V matches 1 if score builderLim V < max_ammo_limit S store result storage mgs:tmp Item.tag.Limit int 1 run scoreboard players get builderLim V
execute if score v1 V matches 1 if score builderFill V matches 1.. store result storage mgs:tmp Item.tag.Fill int 1 run scoreboard players get builderFill V
execute if score v1 V matches 1 run function mgs_builder:sub_build/resolve_slot

scoreboard players set builderGun V 0
scoreboard players set builderAtt V 0
scoreboard players set builderLim V 2147483647
scoreboard players set builderFill V 0
scoreboard players set builderSlot V 0