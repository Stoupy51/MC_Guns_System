
#> mgs:v5.0.0/multiplayer/editor/pick_secondary_scope
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.0.0/player/config/process
#

# Store secondary scope choice
execute if score @s mgs.player.config matches 260 run data modify storage mgs:temp editor.secondary_scope set value ""
execute if score @s mgs.player.config matches 260 run data modify storage mgs:temp editor.secondary_scope_name set value "Iron Sights"
execute if score @s mgs.player.config matches 261 run data modify storage mgs:temp editor.secondary_scope set value "_1"
execute if score @s mgs.player.config matches 261 run data modify storage mgs:temp editor.secondary_scope_name set value "Holographic"
execute if score @s mgs.player.config matches 262 run data modify storage mgs:temp editor.secondary_scope set value "_2"
execute if score @s mgs.player.config matches 262 run data modify storage mgs:temp editor.secondary_scope_name set value "Kobra"
execute if score @s mgs.player.config matches 263 run data modify storage mgs:temp editor.secondary_scope set value "_3"
execute if score @s mgs.player.config matches 263 run data modify storage mgs:temp editor.secondary_scope_name set value "ACOG Red Dot (3x Scope)"
execute if score @s mgs.player.config matches 264 run data modify storage mgs:temp editor.secondary_scope set value "_4"
execute if score @s mgs.player.config matches 264 run data modify storage mgs:temp editor.secondary_scope_name set value "Mk4 (4x Scope)"

# Compute full secondary weapon ID
function mgs:v5.0.0/multiplayer/editor/set_secondary_full with storage mgs:temp editor

# Show equipment dialog
function mgs:v5.0.0/multiplayer/editor/show_equipment_dialog

