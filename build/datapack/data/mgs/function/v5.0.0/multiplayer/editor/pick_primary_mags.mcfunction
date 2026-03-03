
#> mgs:v5.0.0/multiplayer/editor/pick_primary_mags
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.0.0/player/config/process
#

# Validate and store primary mag count and deduct cost
execute if score @s mgs.player.config matches 391 run execute if score @s mgs.mp.edit_points matches ..0 run return run tellraw @s [{"translate": "mgs","color":"gold"},{"translate": "mgs.not_enough_points_for_1_magazines","color":"red"}]
execute if score @s mgs.player.config matches 391 run data modify storage mgs:temp editor.primary_mag_count set value 1
execute if score @s mgs.player.config matches 391 run scoreboard players remove @s mgs.mp.edit_points 1
execute if score @s mgs.player.config matches 392 run execute if score @s mgs.mp.edit_points matches ..1 run return run tellraw @s [{"translate": "mgs","color":"gold"},{"translate": "mgs.not_enough_points_for_2_magazines","color":"red"}]
execute if score @s mgs.player.config matches 392 run data modify storage mgs:temp editor.primary_mag_count set value 2
execute if score @s mgs.player.config matches 392 run scoreboard players remove @s mgs.mp.edit_points 2
execute if score @s mgs.player.config matches 393 run execute if score @s mgs.mp.edit_points matches ..2 run return run tellraw @s [{"translate": "mgs","color":"gold"},{"translate": "mgs.not_enough_points_for_3_magazines","color":"red"}]
execute if score @s mgs.player.config matches 393 run data modify storage mgs:temp editor.primary_mag_count set value 3
execute if score @s mgs.player.config matches 393 run scoreboard players remove @s mgs.mp.edit_points 3
execute if score @s mgs.player.config matches 394 run execute if score @s mgs.mp.edit_points matches ..3 run return run tellraw @s [{"translate": "mgs","color":"gold"},{"translate": "mgs.not_enough_points_for_4_magazines","color":"red"}]
execute if score @s mgs.player.config matches 394 run data modify storage mgs:temp editor.primary_mag_count set value 4
execute if score @s mgs.player.config matches 394 run scoreboard players remove @s mgs.mp.edit_points 4
execute if score @s mgs.player.config matches 395 run execute if score @s mgs.mp.edit_points matches ..4 run return run tellraw @s [{"translate": "mgs","color":"gold"},{"translate": "mgs.not_enough_points_for_5_magazines","color":"red"}]
execute if score @s mgs.player.config matches 395 run data modify storage mgs:temp editor.primary_mag_count set value 5
execute if score @s mgs.player.config matches 395 run scoreboard players remove @s mgs.mp.edit_points 5

# Show secondary weapon dialog
function mgs:v5.0.0/multiplayer/editor/show_secondary_dialog

