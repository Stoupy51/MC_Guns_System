
#> mgs:v5.1.0/multiplayer/editor/pick_perk
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.1.0/player/config/process
#

execute if score @s mgs.player.config matches 410 run data modify storage mgs:temp _toggle_perk set value "quick_reload"
execute if score @s mgs.player.config matches 411 run data modify storage mgs:temp _toggle_perk set value "quick_swap"
execute if score @s mgs.player.config matches 412 run data modify storage mgs:temp _toggle_perk set value "juggernaut"
execute if score @s mgs.player.config matches 413 run data modify storage mgs:temp _toggle_perk set value "scavenger"
execute if score @s mgs.player.config matches 414 run data modify storage mgs:temp _toggle_perk set value "flak_jacket"
execute if score @s mgs.player.config matches 415 run data modify storage mgs:temp _toggle_perk set value "tracker"
execute if score @s mgs.player.config matches 416 run data modify storage mgs:temp _toggle_perk set value "tactical_mask"
execute if score @s mgs.player.config matches 417 run data modify storage mgs:temp _toggle_perk set value "overkill"
execute if score @s mgs.player.config matches 418 run data modify storage mgs:temp _toggle_perk set value "quick_fix"

function mgs:v5.1.0/multiplayer/editor/toggle_perk with storage mgs:temp

# Overkill changes what the secondary slot holds, so toggling it clears the secondary.
execute if data storage mgs:temp {_toggle_perk:"overkill"} run function mgs:v5.1.0/multiplayer/editor/clear_secondary

function mgs:v5.1.0/multiplayer/editor/show_perks_dialog

