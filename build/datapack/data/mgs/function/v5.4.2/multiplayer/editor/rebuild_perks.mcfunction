
#> mgs:v5.4.2/multiplayer/editor/rebuild_perks
#
# @within	mgs:v5.4.2/dialog/close_then
#			mgs:v5.4.2/multiplayer/editor/remove_perk with storage mgs:temp
#			mgs:v5.4.2/multiplayer/editor/rebuild_perks with storage mgs:temp
#
# @args		_toggle_perk (unknown)
#

execute unless data storage mgs:temp _remove_iter[0] run return 0
data modify storage mgs:temp _perk_val set from storage mgs:temp _remove_iter[0]
data remove storage mgs:temp _remove_iter[0]
$execute unless data storage mgs:temp {_perk_val:"$(_toggle_perk)"} run data modify storage mgs:temp editor.perks append from storage mgs:temp _perk_val
function mgs:v5.4.2/multiplayer/editor/rebuild_perks with storage mgs:temp

