
#> mgs:v5.0.0/multiplayer/editor/pick_secondary_scope
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.0.0/player/config/process
#

# Store secondary scope and deduct cost
execute if score @s mgs.player.config matches 260 run data modify storage mgs:temp editor.secondary_scope set value ""
execute if score @s mgs.player.config matches 260 run data modify storage mgs:temp editor.secondary_scope_name set value "Iron Sights"
execute if score @s mgs.player.config matches 260 run data modify storage mgs:temp editor.secondary_scope set value ""
execute if score @s mgs.player.config matches 260 run data modify storage mgs:temp editor.secondary_scope_name set value "Iron Sights"
execute if score @s mgs.player.config matches 261 run data modify storage mgs:temp editor.secondary_scope set value "_1"
execute if score @s mgs.player.config matches 261 run data modify storage mgs:temp editor.secondary_scope_name set value "Holographic"
execute if score @s mgs.player.config matches 261 run execute if score @s mgs.mp.edit_points matches ..0 run return run tellraw @s [{"translate": "mgs","color":"gold"},{"translate": "mgs.not_enough_points_for_a_scope","color":"red"}]
execute if score @s mgs.player.config matches 261 run data modify storage mgs:temp editor.secondary_scope set value "_1"
execute if score @s mgs.player.config matches 261 run data modify storage mgs:temp editor.secondary_scope_name set value "Holographic"
execute if score @s mgs.player.config matches 261 run scoreboard players remove @s mgs.mp.edit_points 1
execute if score @s mgs.player.config matches 262 run data modify storage mgs:temp editor.secondary_scope set value "_2"
execute if score @s mgs.player.config matches 262 run data modify storage mgs:temp editor.secondary_scope_name set value "Kobra"
execute if score @s mgs.player.config matches 262 run execute if score @s mgs.mp.edit_points matches ..0 run return run tellraw @s [{"translate": "mgs","color":"gold"},{"translate": "mgs.not_enough_points_for_a_scope","color":"red"}]
execute if score @s mgs.player.config matches 262 run data modify storage mgs:temp editor.secondary_scope set value "_2"
execute if score @s mgs.player.config matches 262 run data modify storage mgs:temp editor.secondary_scope_name set value "Kobra"
execute if score @s mgs.player.config matches 262 run scoreboard players remove @s mgs.mp.edit_points 1
execute if score @s mgs.player.config matches 263 run data modify storage mgs:temp editor.secondary_scope set value "_3"
execute if score @s mgs.player.config matches 263 run data modify storage mgs:temp editor.secondary_scope_name set value "ACOG Red Dot (3x Scope)"
execute if score @s mgs.player.config matches 263 run execute if score @s mgs.mp.edit_points matches ..0 run return run tellraw @s [{"translate": "mgs","color":"gold"},{"translate": "mgs.not_enough_points_for_a_scope","color":"red"}]
execute if score @s mgs.player.config matches 263 run data modify storage mgs:temp editor.secondary_scope set value "_3"
execute if score @s mgs.player.config matches 263 run data modify storage mgs:temp editor.secondary_scope_name set value "ACOG Red Dot (3x Scope)"
execute if score @s mgs.player.config matches 263 run scoreboard players remove @s mgs.mp.edit_points 1
execute if score @s mgs.player.config matches 264 run data modify storage mgs:temp editor.secondary_scope set value "_4"
execute if score @s mgs.player.config matches 264 run data modify storage mgs:temp editor.secondary_scope_name set value "Mk4 (4x Scope)"
execute if score @s mgs.player.config matches 264 run execute if score @s mgs.mp.edit_points matches ..0 run return run tellraw @s [{"translate": "mgs","color":"gold"},{"translate": "mgs.not_enough_points_for_a_scope","color":"red"}]
execute if score @s mgs.player.config matches 264 run data modify storage mgs:temp editor.secondary_scope set value "_4"
execute if score @s mgs.player.config matches 264 run data modify storage mgs:temp editor.secondary_scope_name set value "Mk4 (4x Scope)"
execute if score @s mgs.player.config matches 264 run scoreboard players remove @s mgs.mp.edit_points 1

# Compute full secondary ID
function mgs:v5.0.0/multiplayer/editor/set_secondary_full with storage mgs:temp editor

# Show secondary mag count dialog
function mgs:v5.0.0/multiplayer/editor/show_secondary_mags_dialog

