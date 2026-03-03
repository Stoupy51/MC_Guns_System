
#> mgs:v5.0.0/multiplayer/editor/pick_primary_scope
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.0.0/player/config/process
#

# Store scope choice
execute if score @s mgs.player.config matches 230 run data modify storage mgs:temp editor.primary_scope set value ""
execute if score @s mgs.player.config matches 230 run data modify storage mgs:temp editor.primary_scope_name set value "Iron Sights"
execute if score @s mgs.player.config matches 231 run data modify storage mgs:temp editor.primary_scope set value "_1"
execute if score @s mgs.player.config matches 231 run data modify storage mgs:temp editor.primary_scope_name set value "Holographic"
execute if score @s mgs.player.config matches 232 run data modify storage mgs:temp editor.primary_scope set value "_2"
execute if score @s mgs.player.config matches 232 run data modify storage mgs:temp editor.primary_scope_name set value "Kobra"
execute if score @s mgs.player.config matches 233 run data modify storage mgs:temp editor.primary_scope set value "_3"
execute if score @s mgs.player.config matches 233 run data modify storage mgs:temp editor.primary_scope_name set value "ACOG Red Dot (3x Scope)"
execute if score @s mgs.player.config matches 234 run data modify storage mgs:temp editor.primary_scope set value "_4"
execute if score @s mgs.player.config matches 234 run data modify storage mgs:temp editor.primary_scope_name set value "Mk4 (4x Scope)"

# Compute full weapon ID: base + scope suffix (e.g. "ak47" + "_3" = "ak47_3")
function mgs:v5.0.0/multiplayer/editor/set_primary_full with storage mgs:temp editor

# Show secondary weapon dialog
function mgs:v5.0.0/multiplayer/editor/show_secondary_dialog

