
#> mgs:v5.0.0/player/apply_flash_if_can_see
#
# @executed	at @s & anchored eyes & positioned ^ ^ ^0.001 & as @a[distance=..16]
#
# @within	mgs:v5.0.0/player/fire_weapon [ at @s & anchored eyes & positioned ^ ^ ^0.001 & as @a[distance=..16] ]
#

scoreboard players set #can_see mgs.data 0
execute if entity @s[tag=mgs.ticking] run scoreboard players set #can_see mgs.data 1
execute if score #can_see mgs.data matches 0 store result score #can_see mgs.data run function #bs.view:can_see_ata {with:{}}
execute if score #can_see mgs.data matches 1 run particle minecraft:dust{color:[0.02,0.0,0.0],scale:0.01} ~ ~ ~ 0 0 0 0 1 force @s

