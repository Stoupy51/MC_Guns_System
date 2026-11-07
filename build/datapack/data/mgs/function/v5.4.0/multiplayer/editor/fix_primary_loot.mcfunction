
#> mgs:v5.4.0/multiplayer/editor/fix_primary_loot
#
# @within	mgs:v5.4.0/dialog/close_then
#			mgs:v5.4.0/multiplayer/editor/save with storage mgs:temp editor
#
# @args		primary_full (unknown)
#

$data modify storage mgs:temp _build.primary_data.gun_slot.loot set value "mgs:i/$(primary_full)"

