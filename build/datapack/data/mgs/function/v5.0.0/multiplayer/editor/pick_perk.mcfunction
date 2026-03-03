
#> mgs:v5.0.0/multiplayer/editor/pick_perk
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.0.0/player/config/process
#

# Toggle the selected perk
execute if score @s mgs.player.config matches 410 run function mgs:v5.0.0/multiplayer/editor/toggle_perk_0
execute if score @s mgs.player.config matches 411 run function mgs:v5.0.0/multiplayer/editor/toggle_perk_1
execute if score @s mgs.player.config matches 412 run function mgs:v5.0.0/multiplayer/editor/toggle_perk_2

# Re-open the perks dialog to reflect updated state
function mgs:v5.0.0/multiplayer/editor/show_perks_dialog

