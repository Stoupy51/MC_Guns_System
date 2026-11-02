
#> mgs:v5.3.0/zombies/revive/tp_to_body
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.3.0/zombies/revive/on_down with storage mgs:temp
#
# @args		rv_dim (unknown)
#			rv_x (unknown)
#			rv_y (unknown)
#			rv_z (unknown)
#

$execute in $(rv_dim) run tp @s $(rv_x) $(rv_y) $(rv_z)

