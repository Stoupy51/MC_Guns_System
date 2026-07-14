
#> mgs:v5.1.0/zombies/escort/set_wander_target
#
# @executed	as @n[tag=mgs.zb_escort_new] & at @s
#
# @within	mgs:v5.1.0/zombies/escort/retarget with storage mgs:temp _escort
#
# @args		x (unknown)
#			y (unknown)
#			z (unknown)
#

$data modify entity @s wander_target set value [I;$(x),$(y),$(z)]

