
#> mgs:v5.4.1/zombies/revive/tp_to_body
#
# @within	mgs:v5.4.1/dialog/close_then
#			mgs:v5.4.1/zombies/revive/on_down with storage mgs:temp
#
# @args		rv_dim (unknown)
#			rv_x (unknown)
#			rv_y (unknown)
#			rv_z (unknown)
#

$execute in $(rv_dim) run tp @s $(rv_x) $(rv_y) $(rv_z)

