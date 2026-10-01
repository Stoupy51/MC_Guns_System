
#> mgs:v5.1.0/zombies/powerups/entity_tick
#
# @executed	at @s
#
# @within	mgs:v5.1.0/zombies/game_tick [ at @s ]
#

scoreboard players operation @s mgs.zb.pu.timer -= #tick_delta mgs.data

execute if score @s mgs.zb.pu.timer matches ..0 run return run function mgs:v5.1.0/zombies/powerups/expire

# Blinks in the last 10 s.
execute if score @s mgs.zb.pu.timer matches 1..199 run function mgs:v5.1.0/zombies/powerups/blink_tick

# loop_2s every 40 ticks.
scoreboard players operation #pu_loop_phase mgs.data = @s mgs.zb.pu.timer
scoreboard players operation #pu_loop_phase mgs.data %= #40 mgs.data
execute if score #pu_loop_phase mgs.data matches 0 run playsound mgs:zombies/powerups/item/loop_2s ambient @a[scores={mgs.zb.in_game=1},distance=..24] ~ ~ ~ 0.5 1.0

# do_pickup kills @s, so this stays last.
execute if entity @a[scores={mgs.zb.in_game=1},gamemode=!spectator,distance=..1.5,tag=!mgs.pu_collecting] run function mgs:v5.1.0/zombies/powerups/do_pickup

# Downed players pick up by crawling their mannequin over it (Black Ops rule), when no alive player is in range.
execute unless entity @a[scores={mgs.zb.in_game=1},gamemode=!spectator,distance=..1.5] if entity @e[type=minecraft:mannequin,tag=mgs.downed_mannequin,distance=..1.5] run function mgs:v5.1.0/zombies/powerups/do_pickup

