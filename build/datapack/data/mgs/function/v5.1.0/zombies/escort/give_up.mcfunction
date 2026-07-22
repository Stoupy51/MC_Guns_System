
#> mgs:v5.1.0/zombies/escort/give_up
#
# @executed	as @e[tag=mgs.zb_escorted] & at @s
#
# @within	mgs:v5.1.0/zombies/escort/escort_tail
#			mgs:v5.1.0/zombies/escort/watchdog
#

# A MONKEY escort must never fall through to the teleport rescue: that rescue drops the zombie next
# to a player, which is the exact opposite of what a monkey bomb is for. It also doesn't earn the
# failure flag — nothing would ever clear it (only the teleport does), and the zombie would be
# locked out of every future escort for the rest of the game.
execute if entity @n[type=minecraft:wandering_trader,tag=mgs.zb_escort,tag=mgs.zb_escort_monkey,distance=..8] run return run function mgs:v5.1.0/zombies/escort/give_up_monkey

tag @s add mgs.zb_escort_failed
execute as @n[type=minecraft:wandering_trader,tag=mgs.zb_escort,distance=..8] run function mgs:v5.1.0/zombies/escort/discard_trader
function mgs:v5.1.0/zombies/escort/detach
function mgs:v5.1.0/zombies/on_stuck_zombie

