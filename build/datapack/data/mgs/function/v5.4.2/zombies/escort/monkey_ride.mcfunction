
#> mgs:v5.4.2/zombies/escort/monkey_ride
#
# @within	mgs:v5.4.2/dialog/close_then
#			mgs:v5.4.2/zombies/escort/zombie_tick
#

execute if entity @e[tag=mgs.monkey_bomb,distance=..4] run return run function mgs:v5.4.2/zombies/escort/monkey_hold
function mgs:v5.4.2/zombies/escort/escort_tail

