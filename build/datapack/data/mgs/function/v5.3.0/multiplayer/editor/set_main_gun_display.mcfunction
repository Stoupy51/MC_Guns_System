
#> mgs:v5.3.0/multiplayer/editor/set_main_gun_display
#
# @within	mgs:v5.3.0/dialog/close_then
#			mgs:v5.3.0/multiplayer/editor/save with storage mgs:temp editor
#
# @args		primary_name (unknown)
#			primary_scope_name (unknown)
#			primary_camo_name (unknown)
#

$data modify storage mgs:temp _new_loadout.main_gun_display set value "$(primary_name) ($(primary_scope_name), $(primary_camo_name))"

