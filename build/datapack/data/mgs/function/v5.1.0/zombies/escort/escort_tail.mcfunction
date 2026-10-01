
#> mgs:v5.1.0/zombies/escort/escort_tail
#
# @executed	as @e[tag=mgs.zb_escorted] & at @s
#
# @within	mgs:v5.1.0/zombies/escort/zombie_tick
#			mgs:v5.1.0/zombies/escort/walk_ride
#			mgs:v5.1.0/zombies/escort/monkey_ride
#

# TTL out: the trader could not reach the target, fall back to the teleport rescue.
scoreboard players remove @s mgs.zb.escort_ttl 1
execute if score @s mgs.zb.escort_ttl matches ..0 run return run function mgs:v5.1.0/zombies/escort/give_up

# Every second (retarget picks player, PaP lure or monkey).
scoreboard players operation #zb_esc_mod mgs.data = @s mgs.zb.escort_ttl
scoreboard players operation #zb_esc_mod mgs.data %= #20 mgs.data
execute if score #zb_esc_mod mgs.data matches 0 as @n[type=minecraft:wandering_trader,tag=mgs.zb_escort,distance=..8] at @s run function mgs:v5.1.0/zombies/escort/retarget

# Catches a trader that cannot move in 5 s instead of 45 s.
execute if score #zb_esc_mod mgs.data matches 0 run function mgs:v5.1.0/zombies/escort/watchdog

