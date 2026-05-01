
#> mgs:v5.0.0/zombies/powerups/entity_tick
#
# @executed	as @e[tag=mgs.pu_item] & at @s
#
# @within	mgs:v5.0.0/zombies/game_tick [ as @e[tag=mgs.pu_item] & at @s ]
#

# Decrement lifetime timer
scoreboard players remove @s mgs.zb.pu.timer 1

# Expired: remove visuals and stop processing this entity
execute if score @s mgs.zb.pu.timer matches ..0 run return run function mgs:v5.0.0/zombies/powerups/expire

# Blink warning in the last 10 seconds
execute if score @s mgs.zb.pu.timer matches 1..199 run function mgs:v5.0.0/zombies/powerups/blink_tick

# Pickup check (do_pickup kills @s, so this must be the last command)
execute if entity @a[scores={mgs.zb.in_game=1},gamemode=!spectator,distance=..1.5,tag=!mgs.pu_collecting] run function mgs:v5.0.0/zombies/powerups/do_pickup

