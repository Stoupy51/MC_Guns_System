
#> mgs:v5.3.0/multiplayer/editor/fix_secondary_loot
#
# @within	mgs:v5.3.0/dialog/close_then
#			mgs:v5.3.0/multiplayer/editor/save with storage mgs:temp editor
#
# @args		secondary_full (unknown)
#

$data modify storage mgs:temp _build.secondary_data.gun_slot.loot set value "mgs:i/$(secondary_full)"

