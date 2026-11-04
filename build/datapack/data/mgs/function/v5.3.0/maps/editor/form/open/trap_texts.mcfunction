
#> mgs:v5.3.0/maps/editor/form/open/trap_texts
#
# @within	mgs:v5.3.0/dialog/close_then
#			mgs:v5.3.0/maps/editor/form/open/trap with entity @s data
#
# @args		effect_radius (unknown)
#			offset_pos (unknown)
#

$data modify storage mgs:temp _form_text set value '$(effect_radius)'
data modify storage mgs:temp dialog.inputs[5].initial set string storage mgs:temp _form_text 1 -1
$data modify storage mgs:temp _form_text set value '$(offset_pos)'
data modify storage mgs:temp dialog.inputs[6].initial set string storage mgs:temp _form_text 1 -1

