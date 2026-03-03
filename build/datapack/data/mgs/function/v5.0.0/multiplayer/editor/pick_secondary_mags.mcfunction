
#> mgs:v5.0.0/multiplayer/editor/pick_secondary_mags
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.0.0/player/config/process
#

# Store secondary mag count and deduct cost
execute if score @s mgs.player.config matches 396 run data modify storage mgs:temp editor.secondary_mag_count set value 0
execute if score @s mgs.player.config matches 397 run execute if score @s mgs.mp.edit_points matches ..0 run return run tellraw @s [{"translate": "mgs","color":"gold"},{"translate": "mgs.not_enough_points_for_1_secondary_magazines","color":"red"}]
execute if score @s mgs.player.config matches 397 run data modify storage mgs:temp editor.secondary_mag_count set value 1
execute if score @s mgs.player.config matches 397 run scoreboard players remove @s mgs.mp.edit_points 1
execute if score @s mgs.player.config matches 398 run execute if score @s mgs.mp.edit_points matches ..1 run return run tellraw @s [{"translate": "mgs","color":"gold"},{"translate": "mgs.not_enough_points_for_2_secondary_magazines","color":"red"}]
execute if score @s mgs.player.config matches 398 run data modify storage mgs:temp editor.secondary_mag_count set value 2
execute if score @s mgs.player.config matches 398 run scoreboard players remove @s mgs.mp.edit_points 2
execute if score @s mgs.player.config matches 399 run execute if score @s mgs.mp.edit_points matches ..2 run return run tellraw @s [{"translate": "mgs","color":"gold"},{"translate": "mgs.not_enough_points_for_3_secondary_magazines","color":"red"}]
execute if score @s mgs.player.config matches 399 run data modify storage mgs:temp editor.secondary_mag_count set value 3
execute if score @s mgs.player.config matches 399 run scoreboard players remove @s mgs.mp.edit_points 3
execute if score @s mgs.player.config matches 400 run execute if score @s mgs.mp.edit_points matches ..3 run return run tellraw @s [{"translate": "mgs","color":"gold"},{"translate": "mgs.not_enough_points_for_4_secondary_magazines","color":"red"}]
execute if score @s mgs.player.config matches 400 run data modify storage mgs:temp editor.secondary_mag_count set value 4
execute if score @s mgs.player.config matches 400 run scoreboard players remove @s mgs.mp.edit_points 4
execute if score @s mgs.player.config matches 401 run execute if score @s mgs.mp.edit_points matches ..4 run return run tellraw @s [{"translate": "mgs","color":"gold"},{"translate": "mgs.not_enough_points_for_5_secondary_magazines","color":"red"}]
execute if score @s mgs.player.config matches 401 run data modify storage mgs:temp editor.secondary_mag_count set value 5
execute if score @s mgs.player.config matches 401 run scoreboard players remove @s mgs.mp.edit_points 5

# Show equipment slot 1 dialog
function mgs:v5.0.0/multiplayer/editor/show_equip_slot1_dialog

