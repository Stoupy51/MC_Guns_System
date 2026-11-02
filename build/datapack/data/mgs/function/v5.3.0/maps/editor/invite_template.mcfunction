
#> mgs:v5.3.0/maps/editor/invite_template
#
# @within	mgs:v5.3.0/maps/editor/invite with storage mgs:temp _inv
#
# @args		tpl (string)
#

$data modify storage mgs:temp dialog.actions[0].action.template set value "/function mgs:v5.3.0/maps/editor/invite_selected {ids:[$(tpl)0]}"

