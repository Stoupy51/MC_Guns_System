
#> mgs:v5.0.0/multiplayer/show_dialog
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.0.0/multiplayer/select_class with storage mgs:temp
#			mgs:v5.0.0/multiplayer/editor/start with storage mgs:temp
#			mgs:v5.0.0/multiplayer/editor/scope/primary_full with storage mgs:temp
#			mgs:v5.0.0/multiplayer/editor/scope/primary_no4 with storage mgs:temp
#			mgs:v5.0.0/multiplayer/editor/scope/primary_1only with storage mgs:temp
#			mgs:v5.0.0/multiplayer/editor/show_secondary_dialog with storage mgs:temp
#			mgs:v5.0.0/multiplayer/editor/scope/secondary_4only with storage mgs:temp
#			mgs:v5.0.0/multiplayer/editor/show_equipment_dialog with storage mgs:temp
#			mgs:v5.0.0/multiplayer/editor/show_confirm with storage mgs:temp
#
# @args		dialog (unknown)
#

$dialog show @s $(dialog)

