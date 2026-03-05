
#> mgs:v5.0.0/multiplayer/editor/pick_perk
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.0.0/player/config/process
#

# Store which perk was toggled
execute if score @s mgs.player.config matches 410 run data modify storage mgs:temp _toggle_perk set value "quick_reload"
execute if score @s mgs.player.config matches 411 run data modify storage mgs:temp _toggle_perk set value "quick_swap"
execute if score @s mgs.player.config matches 412 run data modify storage mgs:temp _toggle_perk set value "infinite_ammo"

# Toggle the selected perk (generic macro function)
function mgs:v5.0.0/multiplayer/editor/toggle_perk with storage mgs:temp
# Re-open the perks dialog to reflect updated state
function mgs:v5.0.0/multiplayer/editor/show_perks_dialog

