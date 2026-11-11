
#> mgs:v5.4.2/zombies/escort/give_up
#
# @within	mgs:v5.4.2/dialog/close_then
#			mgs:v5.4.2/zombies/escort/escort_tail
#			mgs:v5.4.2/zombies/escort/watchdog
#

# A monkey escort never falls through to the teleport rescue.
execute if entity @n[type=minecraft:wandering_trader,tag=mgs.zb_escort,tag=mgs.zb_escort_monkey,distance=..8] run return run function mgs:v5.4.2/zombies/escort/monkey_hold

tag @s add mgs.zb_escort_failed
execute as @n[type=minecraft:wandering_trader,tag=mgs.zb_escort,distance=..8] run function mgs:v5.4.2/zombies/escort/discard_trader
function mgs:v5.4.2/zombies/escort/detach
function mgs:v5.4.2/zombies/on_stuck_zombie

