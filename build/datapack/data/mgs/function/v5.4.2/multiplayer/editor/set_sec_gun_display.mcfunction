
#> mgs:v5.4.2/multiplayer/editor/set_sec_gun_display
#
# @within	mgs:v5.4.2/dialog/close_then
#			mgs:v5.4.2/multiplayer/editor/save with storage mgs:temp editor
#
# @args		secondary_name (unknown)
#			secondary_scope_name (unknown)
#			secondary_camo_name (unknown)
#

$data modify storage mgs:temp _new_loadout.secondary_gun_display set value "$(secondary_name) ($(secondary_scope_name), $(secondary_camo_name))"

