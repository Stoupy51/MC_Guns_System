
#> mgs:v5.4.2/zombies/mob/riders
#
# @within	mgs:v5.4.2/dialog/close_then
#			mgs:v5.4.2/zombies/mob/setup
#

data modify storage mgs:temp _riders prepend from storage mgs:temp _mob.riders
function mgs:v5.4.2/zombies/mob/rider
data remove storage mgs:temp _riders[0]

