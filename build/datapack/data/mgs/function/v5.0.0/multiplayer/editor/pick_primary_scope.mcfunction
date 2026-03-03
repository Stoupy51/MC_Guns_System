
#> mgs:v5.0.0/multiplayer/editor/pick_primary_scope
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.0.0/player/config/process
#

# Store scope choice and deduct cost if non-iron
execute if score @s mgs.player.config matches 230 run data modify storage mgs:temp editor.primary_scope set value ""
execute if score @s mgs.player.config matches 230 run data modify storage mgs:temp editor.primary_scope_name set value "Iron Sights"
execute if score @s mgs.player.config matches 231 run execute if score @s mgs.mp.edit_points matches ..0 run return run tellraw @s [{"translate": "mgs","color":"gold"},{"translate": "mgs.not_enough_points_for_a_scope","color":"red"}]
execute if score @s mgs.player.config matches 231 run data modify storage mgs:temp editor.primary_scope set value "_1"
execute if score @s mgs.player.config matches 231 run data modify storage mgs:temp editor.primary_scope_name set value "Holographic"
execute if score @s mgs.player.config matches 231 run scoreboard players remove @s mgs.mp.edit_points 1
execute if score @s mgs.player.config matches 232 run execute if score @s mgs.mp.edit_points matches ..0 run return run tellraw @s [{"translate": "mgs","color":"gold"},{"translate": "mgs.not_enough_points_for_a_scope","color":"red"}]
execute if score @s mgs.player.config matches 232 run data modify storage mgs:temp editor.primary_scope set value "_2"
execute if score @s mgs.player.config matches 232 run data modify storage mgs:temp editor.primary_scope_name set value "Kobra"
execute if score @s mgs.player.config matches 232 run scoreboard players remove @s mgs.mp.edit_points 1
execute if score @s mgs.player.config matches 233 run execute if score @s mgs.mp.edit_points matches ..0 run return run tellraw @s [{"translate": "mgs","color":"gold"},{"translate": "mgs.not_enough_points_for_a_scope","color":"red"}]
execute if score @s mgs.player.config matches 233 run data modify storage mgs:temp editor.primary_scope set value "_3"
execute if score @s mgs.player.config matches 233 run data modify storage mgs:temp editor.primary_scope_name set value "ACOG Red Dot (3x Scope)"
execute if score @s mgs.player.config matches 233 run scoreboard players remove @s mgs.mp.edit_points 1
execute if score @s mgs.player.config matches 234 run execute if score @s mgs.mp.edit_points matches ..0 run return run tellraw @s [{"translate": "mgs","color":"gold"},{"translate": "mgs.not_enough_points_for_a_scope","color":"red"}]
execute if score @s mgs.player.config matches 234 run data modify storage mgs:temp editor.primary_scope set value "_4"
execute if score @s mgs.player.config matches 234 run data modify storage mgs:temp editor.primary_scope_name set value "Mk4 (4x Scope)"
execute if score @s mgs.player.config matches 234 run scoreboard players remove @s mgs.mp.edit_points 1

# Compute full weapon ID
function mgs:v5.0.0/multiplayer/editor/set_primary_full with storage mgs:temp editor

# Show primary mag count dialog
function mgs:v5.0.0/multiplayer/editor/show_primary_mags_dialog

