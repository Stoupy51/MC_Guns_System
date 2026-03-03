
#> mgs:v5.0.0/multiplayer/editor/append_perk_line
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.0.0/multiplayer/editor/append_perks_to_confirm
#			mgs:v5.0.0/multiplayer/editor/append_perk_line_macro
#

execute unless data storage mgs:temp _perk_iter[0] run return 0
data modify storage mgs:temp _perk_val set from storage mgs:temp _perk_iter[0]
data remove storage mgs:temp _perk_iter[0]
function mgs:v5.0.0/multiplayer/editor/append_perk_line_macro with storage mgs:temp

