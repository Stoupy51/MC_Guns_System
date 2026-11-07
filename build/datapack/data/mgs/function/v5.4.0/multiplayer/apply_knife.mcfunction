
#> mgs:v5.4.0/multiplayer/apply_knife
#
# @within	mgs:v5.4.0/dialog/close_then
#			mgs:v5.4.0/multiplayer/apply_class_dynamic with storage mgs:temp _knife
#
# @args		camo (string)
#

$loot replace entity @s hotbar.0 loot mgs:i/combat_knife$(camo)

