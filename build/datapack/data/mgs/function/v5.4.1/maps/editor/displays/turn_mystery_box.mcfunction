
#> mgs:v5.4.1/maps/editor/displays/turn_mystery_box
#
# @within	mgs:v5.4.1/dialog/close_then
#			mgs:v5.4.1/maps/editor/displays/mystery_box_pos with storage mgs:temp _ed_mb
#
# @args		yaw (float)
#			pitch (float)
#

$execute rotated $(yaw) $(pitch) run function mgs:v5.4.1/maps/editor/displays/summon_mystery_box

