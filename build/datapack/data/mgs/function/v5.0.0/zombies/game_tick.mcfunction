
#> mgs:v5.0.0/zombies/game_tick
#
# @within	mgs:v5.0.0/tick
#

# Revive system tick (process downed players)
function mgs:v5.0.0/zombies/revive/tick

# Zombie Spawning (if there are still zombies to spawn)
execute if score #zb_to_spawn mgs.data matches 1.. run function mgs:v5.0.0/zombies/spawn_tick

# Rise animation tick for spawning zombies
execute as @e[tag=mgs.zb_rising] at @s run function mgs:v5.0.0/zombies/zombie_rise_tick

# Boundary enforcement (skip spectators, only if map has bounds)
execute if score #zb_has_bounds mgs.data matches 1 as @e[tag=mgs.zombie_round] at @s run function mgs:v5.0.0/zombies/check_bounds
execute if score #zb_has_bounds mgs.data matches 1 as @e[type=player,scores={mgs.zb.in_game=1},gamemode=!creative,gamemode=!spectator] at @s run function mgs:v5.0.0/zombies/check_bounds

# Check round completion
execute store result score #zb_alive mgs.data if entity @e[tag=mgs.zombie_round]
execute if score #zb_alive mgs.data matches 0 if score #zb_to_spawn mgs.data matches 0 run function mgs:v5.0.0/zombies/round_complete

# Check game over (all players downed or spectator means no one can revive)
execute if score #zb_round_grace mgs.data matches 1.. run scoreboard players remove #zb_round_grace mgs.data 1
execute unless score #zb_round_grace mgs.data matches 1.. store result score #zb_alive_players mgs.data if entity @a[scores={mgs.zb.in_game=1,mgs.zb.downed=0},gamemode=!spectator]
execute unless score #zb_round_grace mgs.data matches 1.. if score #zb_alive_players mgs.data matches 0 run function mgs:v5.0.0/zombies/game_over

# Stuck zombie glow: count up once all spawns are done (60s = 1200 ticks after last spawn)
execute if score #zb_to_spawn mgs.data matches 0 run scoreboard players add #zb_stuck_timer mgs.data 1
execute if score #zb_to_spawn mgs.data matches 1.. run scoreboard players set #zb_stuck_timer mgs.data 0
# Once threshold reached, tick glow refresh timer (every 5s = 100 ticks → apply glowing for 6s = 120 ticks)
execute if score #zb_stuck_timer mgs.data matches 1200.. run scoreboard players add #zb_glow_timer mgs.data 1
execute if score #zb_glow_timer mgs.data matches 100.. run scoreboard players set #zb_glow_timer mgs.data 0
execute if score #zb_stuck_timer mgs.data matches 1200.. if score #zb_glow_timer mgs.data matches 0 if entity @e[tag=mgs.zombie_round] run function mgs:v5.0.0/zombies/glow_stuck_zombies

# Refresh sidebar every second (20 ticks)
scoreboard players add #zb_sidebar_timer mgs.data 1
execute if score #zb_sidebar_timer mgs.data matches 20.. run scoreboard players set #zb_sidebar_timer mgs.data 0
execute if score #zb_sidebar_timer mgs.data matches 0 run function mgs:v5.0.0/zombies/refresh_sidebar

# Cleanup
kill @e[type=experience_orb]

# Intercept dying zombies before vanilla death particles are emitted.
function mgs:v5.0.0/zombies/death_watch_tick

# Ability tick
function mgs:v5.0.0/zombies/ability_tick

# Refresh player info item every 5 seconds (100 ticks)
scoreboard players add #zb_info_timer mgs.data 1
execute if score #zb_info_timer mgs.data matches 100.. run scoreboard players set #zb_info_timer mgs.data 0
execute if score #zb_info_timer mgs.data matches 0 as @a[scores={mgs.zb.in_game=1},gamemode=!spectator] if items entity @s hotbar.8 *[custom_data~{mgs:{zb_info:true,zombies:{hotbar:8}}}] run function mgs:v5.0.0/zombies/inventory/refresh_info_item

# Mystery box animation tick
function mgs:v5.0.0/zombies/mystery_box/tick

# PAP animation tick (all phases use positive timer: 240→0)
execute as @e[tag=mgs.pap_machine,scores={mgs.pap_anim=1..}] at @s run function mgs:v5.0.0/zombies/pap/anim/step

# Barriers: restore frozen speeds from last tick, then dispatch all display ticks
execute as @e[tag=mgs.zombie_round,tag=mgs.barrier_frozen] run function mgs:v5.0.0/zombies/barriers/restore_zombie_speed
execute as @e[tag=mgs.barrier_display] at @s run function mgs:v5.0.0/zombies/barriers/tick

# Trap active tick (damage + timer)
execute as @e[tag=mgs.trap_center,scores={mgs.zb.trap.timer=1..}] at @s run function mgs:v5.0.0/zombies/traps/active_tick

# Trap cooldown uses expiration tick comparison (no per-tick decrements needed)

