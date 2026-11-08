
#> mgs:v5.4.1/zombies/revive/tp_to_death
#
# @within	mgs:v5.4.1/dialog/close_then
#			mgs:v5.4.1/zombies/revive/spawn_downed_body with storage mgs:temp
#
# @args		rv_dim (unknown)
#			rv_x (unknown)
#			rv_y (unknown)
#			rv_z (unknown)
#			rv_y_hud (unknown)
#

$execute in $(rv_dim) run tp @n[tag=mgs.downed_new] $(rv_x) $(rv_y) $(rv_z)
$execute in $(rv_dim) run tp @n[tag=mgs.downed_hud_new] $(rv_x) $(rv_y_hud) $(rv_z)

