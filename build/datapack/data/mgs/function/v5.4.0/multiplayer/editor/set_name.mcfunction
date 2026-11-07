
#> mgs:v5.4.0/multiplayer/editor/set_name
#
# @within	mgs:v5.4.0/dialog/close_then
#			mgs:v5.4.0/multiplayer/editor/save with storage mgs:temp editor
#
# @args		primary_name (unknown)
#			secondary_name (unknown)
#

$data modify storage mgs:temp _new_loadout.name set value "$(primary_name) + $(secondary_name)"

