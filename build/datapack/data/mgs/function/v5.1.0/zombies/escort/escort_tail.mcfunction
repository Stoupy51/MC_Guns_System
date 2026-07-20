
#> mgs:v5.1.0/zombies/escort/escort_tail
#
# @executed	as @e[tag=mgs.zb_escorted] & at @s
#
# @within	mgs:v5.1.0/zombies/escort/zombie_tick
#			mgs:v5.1.0/zombies/escort/monkey_ride
#

# TTL countdown; the trader could not reach its target in time -> teleport-rescue fallback
scoreboard players remove @s mgs.zb.escort_ttl 1
execute if score @s mgs.zb.escort_ttl matches ..0 run return run function mgs:v5.1.0/zombies/escort/give_up

# Re-aim the trader at its target every second (retarget picks player / PaP lure / monkey)
scoreboard players operation #zb_esc_mod mgs.data = @s mgs.zb.escort_ttl
scoreboard players operation #zb_esc_mod mgs.data %= #20 mgs.data
execute if score #zb_esc_mod mgs.data matches 0 as @n[type=minecraft:wandering_trader,tag=mgs.zb_escort,distance=..8] at @s run function mgs:v5.1.0/zombies/escort/retarget

# Watchdog every second: a trader that can't move is caught in 5s, not 45s
execute if score #zb_esc_mod mgs.data matches 0 run function mgs:v5.1.0/zombies/escort/watchdog

