
#> mgs:v5.1.0/zombies/revive/tp_to_death
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.1.0/zombies/revive/spawn_downed_body with storage mgs:temp
#
# @args		rv_x (unknown)
#			rv_y (unknown)
#			rv_z (unknown)
#			rv_y_hud (unknown)
#

$tp @n[tag=mgs.downed_new] $(rv_x) $(rv_y) $(rv_z)
$tp @n[tag=mgs.downed_hud_new] $(rv_x) $(rv_y_hud) $(rv_z)

