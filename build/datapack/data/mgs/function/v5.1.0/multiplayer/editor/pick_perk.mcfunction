
#> mgs:v5.1.0/multiplayer/editor/pick_perk
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.1.0/player/config/process
#

# Store which perk was toggled
execute if score @s mgs.player.config matches 410 run data modify storage mgs:temp _toggle_perk set value "quick_reload"
execute if score @s mgs.player.config matches 411 run data modify storage mgs:temp _toggle_perk set value "quick_swap"
execute if score @s mgs.player.config matches 412 run data modify storage mgs:temp _toggle_perk set value "juggernaut"
execute if score @s mgs.player.config matches 413 run data modify storage mgs:temp _toggle_perk set value "scavenger"
execute if score @s mgs.player.config matches 414 run data modify storage mgs:temp _toggle_perk set value "flak_jacket"
execute if score @s mgs.player.config matches 415 run data modify storage mgs:temp _toggle_perk set value "tracker"
execute if score @s mgs.player.config matches 416 run data modify storage mgs:temp _toggle_perk set value "tactical_mask"
execute if score @s mgs.player.config matches 417 run data modify storage mgs:temp _toggle_perk set value "overkill"
execute if score @s mgs.player.config matches 418 run data modify storage mgs:temp _toggle_perk set value "quick_fix"

# Toggle the selected perk (generic macro function)
function mgs:v5.1.0/multiplayer/editor/toggle_perk with storage mgs:temp

# Overkill changes what the secondary slot means (pistol vs primary), so toggling it
# always clears the current secondary to avoid an invalid combination
execute if data storage mgs:temp {_toggle_perk:"overkill"} run function mgs:v5.1.0/multiplayer/editor/clear_secondary

# Re-open the perks dialog to reflect updated state
function mgs:v5.1.0/multiplayer/editor/show_perks_dialog

