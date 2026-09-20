
#> mgs:v5.1.0/zombies/perks/tombstone_tp
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.1.0/zombies/perks/tombstone_on_down with storage mgs:temp
#
# @args		rv_x (unknown)
#			rv_y (unknown)
#			rv_z (unknown)
#

$tp @n[tag=mgs.tombstone_new] $(rv_x) $(rv_y) $(rv_z)

