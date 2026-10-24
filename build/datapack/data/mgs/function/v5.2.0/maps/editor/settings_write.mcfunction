
#> mgs:v5.2.0/maps/editor/settings_write
#
# @within	mgs:v5.2.0/maps/editor/settings_apply with storage mgs:temp map_settings.target
#
# @args		mode (unknown)
#			idx (unknown)
#

$data modify storage mgs:maps $(mode)[$(idx)] merge from storage mgs:temp map_settings.fields
$function mgs:v5.2.0/maps/editor/list/$(mode)

