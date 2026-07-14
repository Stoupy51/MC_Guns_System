
#> mgs:v5.1.0/zombies/powerups/entity_tick
#
# @executed	as @e[tag=mgs.pu_item] & at @s
#
# @within	mgs:v5.1.0/zombies/game_tick [ as @e[tag=mgs.pu_item] & at @s ]
#

# Decrement lifetime timer
scoreboard players remove @s mgs.zb.pu.timer 1

# Expired: remove visuals and stop processing this entity
execute if score @s mgs.zb.pu.timer matches ..0 run return run function mgs:v5.1.0/zombies/powerups/expire

# Blink warning in the last 10 seconds
execute if score @s mgs.zb.pu.timer matches 1..199 run function mgs:v5.1.0/zombies/powerups/blink_tick

# Ambient loop: play loop_2s at the item every 2 seconds (40 ticks)
scoreboard players operation #pu_loop_phase mgs.data = @s mgs.zb.pu.timer
scoreboard players operation #pu_loop_phase mgs.data %= #40 mgs.data
execute if score #pu_loop_phase mgs.data matches 0 run playsound mgs:zombies/powerups/item/loop_2s ambient @a[scores={mgs.zb.in_game=1},distance=..24] ~ ~ ~ 0.5 1.0

# Pickup check (do_pickup kills @s, so this must be the last command)
execute if entity @a[scores={mgs.zb.in_game=1},gamemode=!spectator,distance=..1.5,tag=!mgs.pu_collecting] run function mgs:v5.1.0/zombies/powerups/do_pickup

# Downed players pick up power-ups by crawling their mannequin over them (Black Ops rule).
# Only fires when no alive player is in range (alive players take priority and already ran above).
execute unless entity @a[scores={mgs.zb.in_game=1},gamemode=!spectator,distance=..1.5] if entity @e[tag=mgs.downed_mannequin,distance=..1.5] run function mgs:v5.1.0/zombies/powerups/do_pickup

