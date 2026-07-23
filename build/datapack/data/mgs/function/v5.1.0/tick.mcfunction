
#> mgs:v5.1.0/tick
#
# @within	mgs:v5.1.0/load/tick_verification
#

# Infinitely incrementing tick counter for general timing purposes
scoreboard players add #total_tick mgs.data 1

# Real-time tick equivalents from the mgs:clock stopwatch (scale 20 = seconds x20).
# #tick_delta = real ticks elapsed since the previous game tick: ~1 at 20 TPS, 2+ under lag.
# Mode timers subtract #tick_delta instead of 1 so durations stay wall-clock accurate.
# No lower clamp to 1: ms rounding jitters deltas between 0/1/2 but their SUM stays exact.
# Upper clamp 40 (2s) bounds the jump after a singleplayer pause or a world freeze.
execute store result score #real_tick mgs.data run stopwatch query mgs:clock 20
scoreboard players operation #tick_delta mgs.data = #real_tick mgs.data
scoreboard players operation #tick_delta mgs.data -= #real_prev mgs.data
scoreboard players operation #real_prev mgs.data = #real_tick mgs.data
execute unless score #tick_delta mgs.data matches 0.. run scoreboard players set #tick_delta mgs.data 0
execute if score #tick_delta mgs.data matches 41.. run scoreboard players set #tick_delta mgs.data 40

# Player loop
execute as @e[type=player,sort=random] at @s run function mgs:v5.1.0/player/tick

# Tick function for slow bullets (projectiles)
execute if score #slow_bullet_count mgs.data matches 1.. as @e[tag=mgs.slow_bullet] at @s run function mgs:v5.1.0/projectile/tick

# Tick every live grenade. This is intentionally NOT gated on a running count: a counter desync
# (e.g. a grenade removed outside grenade/delete, or a double-detonate) used to drop the count to 0
# and freeze EVERY projectile's ticking ("no more items to tick", monkey bombs included). Selecting
# by tag each tick is cheap and self-correcting.
execute as @e[tag=mgs.grenade] at @s run function mgs:v5.1.0/grenade/tick

# Armed mob AI loop
execute if score #armed_mob_count mgs.data matches 1.. as @e[tag=mgs.armed] at @s run function mgs:v5.1.0/mob/tick

# Resync armed mob count every 5 seconds (mobs dying never decrement the counter)
scoreboard players operation #armed_mob_phase mgs.data = #total_tick mgs.data
scoreboard players operation #armed_mob_phase mgs.data %= #100 mgs.data
execute if score #armed_mob_count mgs.data matches 1.. if score #armed_mob_phase mgs.data matches 0 store result score #armed_mob_count mgs.data if entity @e[tag=mgs.armed]

# Zombies game tick
execute if data storage mgs:zombies game{state:"active"} run function mgs:v5.1.0/zombies/game_tick
execute if data storage mgs:zombies game{state:"preparing"} run function mgs:v5.1.0/zombies/prep_tick

# Multiplayer game tick
execute if data storage mgs:multiplayer game{state:"active"} run function mgs:v5.1.0/multiplayer/game_tick
execute if data storage mgs:multiplayer game{state:"preparing"} run function mgs:v5.1.0/multiplayer/prep_tick

# Missions game tick
execute if data storage mgs:missions game{state:"active"} run function mgs:v5.1.0/missions/game_tick
execute if data storage mgs:missions game{state:"preparing"} run function mgs:v5.1.0/missions/prep_tick

