
#> mgs:v5.3.0/maps/editor/invite_box_add
#
# @within	mgs:v5.3.0/dialog/close_then
#			mgs:v5.3.0/maps/editor/invite_box with storage mgs:temp _inv
#
# @args		id (unknown)
#			name (unknown)
#			tpl (unknown)
#			d (unknown)
#

$data modify storage mgs:temp dialog.inputs append value {type:"minecraft:boolean",key:"p$(id)",label:"$(name)",initial:false,on_true:"$(id)",on_false:"0"}
$data modify storage mgs:temp _inv.tpl set value "$(tpl)$(d)(p$(id)),"

