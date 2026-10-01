
#> mgs:v5.1.0/tick
#
# @within	mgs:v5.1.0/load/tick_verification
#

scoreboard players add #total_tick mgs.data 1

# #tick_delta = real ticks since the previous game tick (about 1 at 20 TPS, 2+ under lag); mode timers subtract it so durations stay wall-clock accurate.
# No lower clamp: ms rounding jitters deltas between 0, 1 and 2 but their sum stays exact. The upper clamp 40 (2 s) bounds the jump after a pause or freeze.
execute store result score #real_tick mgs.data run stopwatch query mgs:clock 20
scoreboard players operation #tick_delta mgs.data = #real_tick mgs.data
scoreboard players operation #tick_delta mgs.data -= #real_prev mgs.data
scoreboard players operation #real_prev mgs.data = #real_tick mgs.data
execute unless score #tick_delta mgs.data matches 0.. run scoreboard players set #tick_delta mgs.data 0
execute if score #tick_delta mgs.data matches 41.. run scoreboard players set #tick_delta mgs.data 40

execute as @e[type=player,sort=random] at @s run function mgs:v5.1.0/player/tick

scoreboard players operation #fx_sweep mgs.data = #total_tick mgs.data
scoreboard players operation #fx_sweep mgs.data %= #fx_sweep_period mgs.data

execute if score #slow_bullet_count mgs.data matches 1.. as @e[type=minecraft:item_display,tag=mgs.slow_bullet] at @s run function mgs:v5.1.0/projectile/tick

# Not gated on a counter: a desync (a grenade removed outside grenade/delete, a double detonation) could stop every grenade ticking.
# Selecting by tag each tick is cheap and self-correcting.
execute as @e[type=minecraft:item_display,tag=mgs.grenade] at @s run function mgs:v5.1.0/grenade/tick

execute if score #armed_mob_count mgs.data matches 1.. as @e[tag=mgs.armed] at @s run function mgs:v5.1.0/mob/tick

# Every 5 s: dying mobs never decrement the counter.
scoreboard players operation #armed_mob_phase mgs.data = #total_tick mgs.data
scoreboard players operation #armed_mob_phase mgs.data %= #100 mgs.data
execute if score #armed_mob_count mgs.data matches 1.. if score #armed_mob_phase mgs.data matches 0 store result score #armed_mob_count mgs.data if entity @e[tag=mgs.armed]

# Once a second (see progression/tick_player).
scoreboard players operation #xp_sec_tick mgs.data = #total_tick mgs.data
scoreboard players operation #xp_sec_tick mgs.data %= #20 mgs.data
execute if score #xp_sec_tick mgs.data matches 0 as @a run function mgs:v5.1.0/progression/tick_player

# #zb_freeze (admin menu) swaps in the freeze tick: every zombies timer lives in game_tick, so skipping it pauses the round.
execute if data storage mgs:zombies game{state:"active"} unless score #zb_freeze mgs.data matches 1 run function mgs:v5.1.0/zombies/game_tick
execute if data storage mgs:zombies game{state:"active"} if score #zb_freeze mgs.data matches 1 run function mgs:v5.1.0/zombies/freeze_tick

execute if data storage mgs:multiplayer game{state:"active"} run function mgs:v5.1.0/multiplayer/game_tick
execute if data storage mgs:multiplayer game{state:"preparing"} run function mgs:v5.1.0/multiplayer/prep_tick

execute if data storage mgs:missions game{state:"active"} run function mgs:v5.1.0/missions/game_tick
execute if data storage mgs:missions game{state:"preparing"} run function mgs:v5.1.0/missions/prep_tick

