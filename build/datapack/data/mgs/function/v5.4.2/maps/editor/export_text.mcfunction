
#> mgs:v5.4.2/maps/editor/export_text
#
# @within	mgs:v5.4.2/dialog/close_then
#			mgs:v5.4.2/maps/editor/export with storage mgs:temp _export
#
# @args		map (unknown)
#

$data modify storage mgs:temp dialog.inputs[0].initial set value '$(map)'
return 1

