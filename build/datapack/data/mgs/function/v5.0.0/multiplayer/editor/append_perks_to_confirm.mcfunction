
#> mgs:v5.0.0/multiplayer/editor/append_perks_to_confirm
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.0.0/multiplayer/editor/show_confirm
#

data modify storage mgs:temp _perk_iter set from storage mgs:temp editor.perks
function mgs:v5.0.0/multiplayer/editor/append_perk_line

