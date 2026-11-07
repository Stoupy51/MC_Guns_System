
#> mgs:v5.4.0/multiplayer/editor/set_secondary_full
#
# @within	mgs:v5.4.0/dialog/close_then
#			mgs:v5.4.0/multiplayer/editor/pick_secondary_camo with storage mgs:temp editor
#
# @args		secondary (unknown)
#			secondary_scope (unknown)
#			secondary_camo (unknown)
#

$data modify storage mgs:temp editor.secondary_full set value "$(secondary)$(secondary_scope)$(secondary_camo)"

