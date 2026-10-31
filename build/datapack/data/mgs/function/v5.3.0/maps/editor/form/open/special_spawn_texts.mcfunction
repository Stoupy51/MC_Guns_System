
#> mgs:v5.3.0/maps/editor/form/open/special_spawn_texts
#
# @executed	at @s & as @n[tag=mgs.map_element,distance=..10]
#
# @within	mgs:v5.3.0/maps/editor/form/open/special_spawn with entity @s data
#
# @args		mob (unknown)
#			activation_box (unknown)
#			walk_to (unknown)
#

$data modify storage mgs:temp dialog.inputs[5].initial set value '$(mob)'
$data modify storage mgs:temp _form_text set value '$(activation_box)'
data modify storage mgs:temp dialog.inputs[6].initial set string storage mgs:temp _form_text 1 -1
$data modify storage mgs:temp _form_text set value '$(walk_to)'
data modify storage mgs:temp dialog.inputs[7].initial set string storage mgs:temp _form_text 1 -1
return 1

