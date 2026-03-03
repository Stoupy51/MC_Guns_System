
#> mgs:v5.0.0/multiplayer/show_dialog
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.0.0/multiplayer/select_class with storage mgs:temp
#			mgs:v5.0.0/multiplayer/editor/start with storage mgs:temp
#			mgs:v5.0.0/multiplayer/editor/pick_primary with storage mgs:temp
#			mgs:v5.0.0/multiplayer/editor/pick_secondary with storage mgs:temp
#			mgs:v5.0.0/multiplayer/editor/show_confirm with storage mgs:temp
#
# @args		dialog (unknown)
#

$dialog show @s $(dialog)

