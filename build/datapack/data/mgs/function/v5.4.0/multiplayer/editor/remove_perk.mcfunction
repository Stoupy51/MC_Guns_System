
#> mgs:v5.4.0/multiplayer/editor/remove_perk
#
# @within	mgs:v5.4.0/dialog/close_then
#			mgs:v5.4.0/multiplayer/editor/toggle_perk
#

data modify storage mgs:temp _remove_iter set from storage mgs:temp editor.perks
data modify storage mgs:temp editor.perks set value []
function mgs:v5.4.0/multiplayer/editor/rebuild_perks with storage mgs:temp

