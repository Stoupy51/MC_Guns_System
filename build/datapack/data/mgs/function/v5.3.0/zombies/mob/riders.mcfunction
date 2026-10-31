
#> mgs:v5.3.0/zombies/mob/riders
#
# @executed	as @n[tag=mgs.zb_new]
#
# @within	mgs:v5.3.0/zombies/mob/setup
#

data modify storage mgs:temp _riders prepend from storage mgs:temp _mob.riders
function mgs:v5.3.0/zombies/mob/rider
data remove storage mgs:temp _riders[0]

