
#> mgs:v5.0.0/zombies/game_tick
#
# @within	mgs:v5.0.0/tick
#

# Spectate Timer (3s respawn cooldown)
execute as @a[scores={mgs.zb.in_game=1,mgs.mp.spectate_timer=1..}] run scoreboard players remove @s mgs.mp.spectate_timer 1
execute as @a[scores={mgs.zb.in_game=1,mgs.mp.spectate_timer=0},gamemode=spectator] at @s run function mgs:v5.0.0/zombies/actual_respawn

# Zombie Spawning (if there are still zombies to spawn)
execute if score #zb_to_spawn mgs.data matches 1.. run function mgs:v5.0.0/zombies/spawn_tick

# Boundary enforcement (skip spectators, only if map has bounds)
execute if score #zb_has_bounds mgs.data matches 1 as @e[tag=mgs.zombie_round] at @s run function mgs:v5.0.0/zombies/check_bounds
execute if score #zb_has_bounds mgs.data matches 1 as @e[type=player,scores={mgs.zb.in_game=1},gamemode=!creative,gamemode=!spectator] at @s run function mgs:v5.0.0/zombies/check_bounds

# Check round completion
execute store result score #zb_alive mgs.data if entity @e[tag=mgs.zombie_round]
execute if score #zb_alive mgs.data matches 0 if score #zb_to_spawn mgs.data matches 0 run function mgs:v5.0.0/zombies/round_complete

# Check game over (all players down/spectator, but not during first 3 seconds)
execute if score #zb_round_grace mgs.data matches 1.. run scoreboard players remove #zb_round_grace mgs.data 1
execute unless score #zb_round_grace mgs.data matches 1.. store result score #zb_alive_players mgs.data if entity @a[scores={mgs.zb.in_game=1},gamemode=!spectator]
execute unless score #zb_round_grace mgs.data matches 1.. if score #zb_alive_players mgs.data matches 0 run function mgs:v5.0.0/zombies/game_over

# Refresh sidebar every second (20 ticks)
scoreboard players add #zb_sidebar_timer mgs.data 1
execute if score #zb_sidebar_timer mgs.data matches 20.. run scoreboard players set #zb_sidebar_timer mgs.data 0
execute if score #zb_sidebar_timer mgs.data matches 0 run function mgs:v5.0.0/zombies/refresh_sidebar

# Cleanup
kill @e[type=experience_orb]

# Ability tick
function mgs:v5.0.0/zombies/ability_tick

#execute as @a[scores={mgs.zb.in_game=1},gamemode=!spectator] if items entity @s hotbar.8 *[custom_data~{mgs:{zb_info:true,zombies:{hotbar:8}}}] run function mgs:v5.0.0/zombies/inventory/refresh_info_item

# Mystery box animation tick
function mgs:v5.0.0/zombies/mystery_box/tick

# PAP animation tick (all phases use positive timer: 240→0)
execute as @e[tag=mgs.pap_machine,scores={mgs.pap_anim=1..}] at @s run function mgs:v5.0.0/zombies/pap/anim/step

# Trap active tick (damage + timer)
execute as @e[tag=mgs.trap_center,scores={mgs.zb.trap.timer=1..}] at @s run function mgs:v5.0.0/zombies/traps/active_tick

# Trap cooldown uses expiration tick comparison (no per-tick decrements needed)

