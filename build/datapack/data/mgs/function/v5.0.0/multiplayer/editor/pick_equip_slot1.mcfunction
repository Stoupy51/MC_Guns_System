
#> mgs:v5.0.0/multiplayer/editor/pick_equip_slot1
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.0.0/player/config/process
#

# Store slot 1 grenade and deduct cost
execute if score @s mgs.player.config matches 460 run data modify storage mgs:temp editor.equip_slot1 set value ""
execute if score @s mgs.player.config matches 461 run execute if score @s mgs.mp.edit_points matches ..0 run return run tellraw @s [[{"text":"","color":"gold"},"[",{"translate": "mgs"},"] "],{"translate": "mgs.not_enough_points_for_a_grenade","color":"red"}]
execute if score @s mgs.player.config matches 461 run data modify storage mgs:temp editor.equip_slot1 set value "frag_grenade"
execute if score @s mgs.player.config matches 461 run scoreboard players remove @s mgs.mp.edit_points 1
execute if score @s mgs.player.config matches 462 run execute if score @s mgs.mp.edit_points matches ..0 run return run tellraw @s [[{"text":"","color":"gold"},"[",{"translate": "mgs"},"] "],{"translate": "mgs.not_enough_points_for_a_grenade","color":"red"}]
execute if score @s mgs.player.config matches 462 run data modify storage mgs:temp editor.equip_slot1 set value "semtex"
execute if score @s mgs.player.config matches 462 run scoreboard players remove @s mgs.mp.edit_points 1
execute if score @s mgs.player.config matches 463 run execute if score @s mgs.mp.edit_points matches ..0 run return run tellraw @s [[{"text":"","color":"gold"},"[",{"translate": "mgs"},"] "],{"translate": "mgs.not_enough_points_for_a_grenade","color":"red"}]
execute if score @s mgs.player.config matches 463 run data modify storage mgs:temp editor.equip_slot1 set value "flash_grenade"
execute if score @s mgs.player.config matches 463 run scoreboard players remove @s mgs.mp.edit_points 1
execute if score @s mgs.player.config matches 464 run execute if score @s mgs.mp.edit_points matches ..0 run return run tellraw @s [[{"text":"","color":"gold"},"[",{"translate": "mgs"},"] "],{"translate": "mgs.not_enough_points_for_a_grenade","color":"red"}]
execute if score @s mgs.player.config matches 464 run data modify storage mgs:temp editor.equip_slot1 set value "smoke_grenade"
execute if score @s mgs.player.config matches 464 run scoreboard players remove @s mgs.mp.edit_points 1

# Show equipment slot 2 dialog
function mgs:v5.0.0/multiplayer/editor/show_equip_slot2_dialog

