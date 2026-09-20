
#> mgs:v5.1.0/zombies/escort/give_up
#
# @executed	as @e[tag=mgs.zb_escorted] & at @s
#
# @within	mgs:v5.1.0/zombies/escort/escort_tail
#			mgs:v5.1.0/zombies/escort/watchdog
#

# A MONKEY escort must never fall through to the teleport rescue
execute if entity @n[type=minecraft:wandering_trader,tag=mgs.zb_escort,tag=mgs.zb_escort_monkey,distance=..8] run return run function mgs:v5.1.0/zombies/escort/monkey_hold

tag @s add mgs.zb_escort_failed
execute as @n[type=minecraft:wandering_trader,tag=mgs.zb_escort,distance=..8] run function mgs:v5.1.0/zombies/escort/discard_trader
function mgs:v5.1.0/zombies/escort/detach
function mgs:v5.1.0/zombies/on_stuck_zombie

