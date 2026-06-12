
#> mgs:v5.0.1/multiplayer/editor/equip2_done
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.0.1/multiplayer/editor/pick_equip2_camo
#			mgs:v5.0.1/multiplayer/editor/pick_equip_slot2
#

# Clear perks list (fresh start)
data modify storage mgs:temp editor.perks set value []
# Show perks dialog
function mgs:v5.0.1/multiplayer/editor/show_perks_dialog

