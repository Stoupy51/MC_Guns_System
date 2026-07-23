
#> mgs:v5.1.0/zombies/revive/tp_revive_pos
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.1.0/zombies/perks/dying_wish_trigger with storage mgs:temp
#			mgs:v5.1.0/zombies/whos_who/on_down with storage mgs:temp
#			mgs:v5.1.0/zombies/revive/revive_complete with storage mgs:temp
#
# @args		rv_x (unknown)
#			rv_y (unknown)
#			rv_z (unknown)
#

$tp @s $(rv_x) $(rv_y) $(rv_z)

