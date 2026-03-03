
#> mgs:v5.0.0/multiplayer/editor/remove_perk_2
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.0.0/multiplayer/editor/toggle_perk_2
#

# Rebuild perks list without "infinite_ammo"
data modify storage mgs:temp _remove_iter set from storage mgs:temp editor.perks
data modify storage mgs:temp editor.perks set value []
function mgs:v5.0.0/multiplayer/editor/rebuild_perks_2

