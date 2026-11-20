
#> mgs:v5.4.3/maps/editor/settings_write
#
# @within	mgs:v5.4.3/dialog/close_then
#			mgs:v5.4.3/maps/editor/settings_apply with storage mgs:temp map_settings.target
#
# @args		mode (unknown)
#			idx (unknown)
#

$data modify storage mgs:maps $(mode)[$(idx)] merge from storage mgs:temp map_settings.fields
$function mgs:v5.4.3/maps/editor/list/$(mode)

