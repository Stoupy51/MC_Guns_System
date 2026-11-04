
#> mgs:v5.3.0/multiplayer/editor/set_primary_full
#
# @within	mgs:v5.3.0/dialog/close_then
#			mgs:v5.3.0/multiplayer/editor/pick_primary_camo with storage mgs:temp editor
#
# @args		primary (unknown)
#			primary_scope (unknown)
#			primary_camo (unknown)
#

$data modify storage mgs:temp editor.primary_full set value "$(primary)$(primary_scope)$(primary_camo)"

