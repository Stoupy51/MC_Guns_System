
#> mgs:v5.0.0/multiplayer/editor/rebuild_perks_1
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.0.0/multiplayer/editor/remove_perk_1
#			mgs:v5.0.0/multiplayer/editor/rebuild_perks_1
#

execute unless data storage mgs:temp _remove_iter[0] run return 0
data modify storage mgs:temp _perk_val set from storage mgs:temp _remove_iter[0]
data remove storage mgs:temp _remove_iter[0]
# Re-add if not the removed perk, then continue loop
execute unless data storage mgs:temp {_perk_val:"quick_swap"} run data modify storage mgs:temp editor.perks append from storage mgs:temp _perk_val
function mgs:v5.0.0/multiplayer/editor/rebuild_perks_1

