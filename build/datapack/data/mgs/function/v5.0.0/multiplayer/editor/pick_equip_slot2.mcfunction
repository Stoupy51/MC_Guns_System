
#> mgs:v5.0.0/multiplayer/editor/pick_equip_slot2
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.0.0/player/config/process
#

# Store slot 2 grenade and deduct cost
execute if score @s mgs.player.config matches 470 run data modify storage mgs:temp editor.equip_slot2 set value ""
execute if score @s mgs.player.config matches 471 run execute if score @s mgs.mp.edit_points matches ..0 run return run tellraw @s [[{"text":"","color":"gold"},"[",{"translate": "mgs"},"] "],{"translate": "mgs.not_enough_points_for_a_grenade","color":"red"}]
execute if score @s mgs.player.config matches 471 run data modify storage mgs:temp editor.equip_slot2 set value "frag_grenade"
execute if score @s mgs.player.config matches 471 run scoreboard players remove @s mgs.mp.edit_points 1
execute if score @s mgs.player.config matches 472 run execute if score @s mgs.mp.edit_points matches ..0 run return run tellraw @s [[{"text":"","color":"gold"},"[",{"translate": "mgs"},"] "],{"translate": "mgs.not_enough_points_for_a_grenade","color":"red"}]
execute if score @s mgs.player.config matches 472 run data modify storage mgs:temp editor.equip_slot2 set value "semtex"
execute if score @s mgs.player.config matches 472 run scoreboard players remove @s mgs.mp.edit_points 1
execute if score @s mgs.player.config matches 473 run execute if score @s mgs.mp.edit_points matches ..0 run return run tellraw @s [[{"text":"","color":"gold"},"[",{"translate": "mgs"},"] "],{"translate": "mgs.not_enough_points_for_a_grenade","color":"red"}]
execute if score @s mgs.player.config matches 473 run data modify storage mgs:temp editor.equip_slot2 set value "flash_grenade"
execute if score @s mgs.player.config matches 473 run scoreboard players remove @s mgs.mp.edit_points 1
execute if score @s mgs.player.config matches 474 run execute if score @s mgs.mp.edit_points matches ..0 run return run tellraw @s [[{"text":"","color":"gold"},"[",{"translate": "mgs"},"] "],{"translate": "mgs.not_enough_points_for_a_grenade","color":"red"}]
execute if score @s mgs.player.config matches 474 run data modify storage mgs:temp editor.equip_slot2 set value "smoke_grenade"
execute if score @s mgs.player.config matches 474 run scoreboard players remove @s mgs.mp.edit_points 1

# Clear perks list (fresh start)
data modify storage mgs:temp editor.perks set value []
# Show perks dialog
function mgs:v5.0.0/multiplayer/editor/show_perks_dialog

