
#> mgs:v5.4.3/maps/editor/settings_base
#
# @within	mgs:v5.4.3/dialog/close_then
#			mgs:v5.4.3/maps/editor/settings with storage mgs:temp map_settings.base
#
# @args		x (unknown)
#			y (unknown)
#			z (unknown)
#

$data modify storage mgs:temp dialog.inputs[3].initial set value "$(x)"
$data modify storage mgs:temp dialog.inputs[4].initial set value "$(y)"
$data modify storage mgs:temp dialog.inputs[5].initial set value "$(z)"

