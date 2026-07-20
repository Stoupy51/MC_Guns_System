
#> mgs:v5.1.0/zombies/escort/monkey_ride
#
# @executed	as @e[tag=mgs.zb_escorted] & at @s
#
# @within	mgs:v5.1.0/zombies/escort/zombie_tick
#

execute if entity @e[tag=mgs.monkey_bomb,distance=..4] run return run function mgs:v5.1.0/zombies/escort/release
function mgs:v5.1.0/zombies/escort/escort_tail

