
#> mgs:v5.0.1/zombies/game_tick
#
# @within	mgs:v5.0.1/tick
#

# Revive system tick (process downed players)
function mgs:v5.0.1/zombies/revive/tick

# Call map-defined tick script
function mgs:v5.0.1/shared/maps/call_tick_script_at_base

# Zombie Spawning (if there are still zombies to spawn)
execute if score #zb_to_spawn mgs.data matches 1.. run function mgs:v5.0.1/zombies/spawn_tick

# Rise animation tick for spawning zombies
execute as @e[tag=mgs.zb_rising] at @s run function mgs:v5.0.1/zombies/zombie_rise_tick

# Boundary enforcement (skip spectators, only if map has bounds)
execute if score #zb_has_bounds mgs.data matches 1 as @e[tag=mgs.zombie_round] at @s run function mgs:v5.0.1/shared/check_bounds
execute if score #zb_has_bounds mgs.data matches 1 as @e[type=player,scores={mgs.zb.in_game=1},gamemode=!creative,gamemode=!spectator] at @s run function mgs:v5.0.1/zombies/check_bounds_player

# Check round completion
execute store result score #zb_alive mgs.data if entity @e[tag=mgs.zombie_round]
execute if score #zb_alive mgs.data matches 0 if score #zb_to_spawn mgs.data matches 0 run function mgs:v5.0.1/zombies/round_complete

# Check game over: only trigger when no healthy AND no downed players remain
# - Healthy: downed=0, gamemode=!spectator (playing normally)
# - Downed: downed=1, gamemode=spectator (spectating their mannequin, can be revived)
# - Bled out: downed=0, gamemode=spectator (waiting for next round — truly dead)
execute if score #zb_round_grace mgs.data matches 1.. run scoreboard players remove #zb_round_grace mgs.data 1
execute unless score #zb_round_grace mgs.data matches 1.. store result score #zb_alive_players mgs.data if entity @a[scores={mgs.zb.in_game=1,mgs.zb.downed=0},gamemode=!spectator]
execute unless score #zb_round_grace mgs.data matches 1.. store result score #zb_downed_alive mgs.data if entity @a[scores={mgs.zb.in_game=1,mgs.zb.downed=1},gamemode=spectator]
execute unless score #zb_round_grace mgs.data matches 1.. run scoreboard players operation #zb_alive_players mgs.data += #zb_downed_alive mgs.data
execute unless score #zb_round_grace mgs.data matches 1.. if score #zb_alive_players mgs.data matches 0 run function mgs:v5.0.1/zombies/game_over

# Stuck zombie check (every 20 ticks, 24 random non-rising zombies)
execute store result score #zb_tick_mod mgs.data run scoreboard players get #total_tick mgs.data
scoreboard players operation #zb_tick_mod mgs.data %= #20 mgs.data
execute if score #zb_tick_mod mgs.data matches 0 as @e[tag=mgs.zombie_round,tag=!mgs.zb_rising,limit=24,sort=random] at @s run function mgs:v5.0.1/zombies/stuck_zombie_check

# Stuck zombie glow: count up once all spawns are done (60s = 1200 ticks after last spawn)
execute if score #zb_to_spawn mgs.data matches 0 run scoreboard players add #zb_stuck_timer mgs.data 1
execute if score #zb_to_spawn mgs.data matches 1.. run scoreboard players set #zb_stuck_timer mgs.data 0
# Once threshold reached, tick glow refresh timer (every 5s = 100 ticks → apply glowing for 6s = 120 ticks)
execute if score #zb_stuck_timer mgs.data matches 1200.. run scoreboard players add #zb_glow_timer mgs.data 1
execute if score #zb_glow_timer mgs.data matches 100.. run scoreboard players set #zb_glow_timer mgs.data 0
execute if score #zb_stuck_timer mgs.data matches 1200.. if score #zb_glow_timer mgs.data matches 0 if entity @e[tag=mgs.zombie_round] run function mgs:v5.0.1/zombies/glow_stuck_zombies

# Refresh sidebar every second (20 ticks)
scoreboard players add #zb_sidebar_timer mgs.data 1
execute if score #zb_sidebar_timer mgs.data matches 20.. run scoreboard players set #zb_sidebar_timer mgs.data 0
execute if score #zb_sidebar_timer mgs.data matches 0 run function mgs:v5.0.1/zombies/refresh_sidebar

# Cleanup
kill @e[type=experience_orb]

# Award kill points from totalKillCount delta
execute as @a[scores={mgs.zb.in_game=1},gamemode=!spectator] run function mgs:v5.0.1/zombies/check_kill_points

# Intercept dying zombies before vanilla death particles are emitted.
function mgs:v5.0.1/zombies/death_watch_tick

# Managed horde ambience: ~every 35 ticks, give each player one controlled, count-scaled groan.
scoreboard players add #zb_horde_timer mgs.data 1
execute if score #zb_horde_timer mgs.data matches 35.. run scoreboard players set #zb_horde_timer mgs.data 0
execute if score #zb_horde_timer mgs.data matches 0 as @a[scores={mgs.zb.in_game=1},gamemode=!spectator] at @s run function mgs:v5.0.1/zombies/horde_ambient

# Ability tick (Zonweeb variant only)
execute if data storage mgs:zombies game{variant:"zonweeb"} run function mgs:v5.0.1/zombies/ability_tick

# Refresh player info item every 5 seconds (100 ticks)
scoreboard players add #zb_info_timer mgs.data 1
execute if score #zb_info_timer mgs.data matches 100.. run scoreboard players set #zb_info_timer mgs.data 0
execute if score #zb_info_timer mgs.data matches 0 as @a[scores={mgs.zb.in_game=1},gamemode=!spectator] if items entity @s hotbar.8 *[custom_data~{mgs:{zb_info:true,zombies:{hotbar:8}}}] run function mgs:v5.0.1/zombies/inventory/refresh_info_item

# Mystery box animation tick
function mgs:v5.0.1/zombies/mystery_box/tick

# PAP animation tick (all phases use positive timer: 240→0)
execute as @e[tag=mgs.pap_machine,scores={mgs.pap_anim=1..}] at @s run function mgs:v5.0.1/zombies/pap/anim/step

# Barriers: restore frozen speeds from last tick, then dispatch all display ticks
execute as @e[tag=mgs.zombie_round,tag=mgs.barrier_frozen] run function mgs:v5.0.1/zombies/barriers/restore_zombie_speed
execute as @e[tag=mgs.barrier_display] at @s run function mgs:v5.0.1/zombies/barriers/tick

# Power-up entity tick (lifetime countdown, blink, pickup detection)
execute as @e[tag=mgs.pu_item] at @s run function mgs:v5.0.1/zombies/powerups/entity_tick

# Orphan cleanup: a text_display whose item entity was destroyed (burned/exploded) would never
# be removed by expire/pickup — kill any pu_text that no longer has a pu_item beneath it.
execute as @e[tag=mgs.pu_text] at @s unless entity @e[tag=mgs.pu_item,distance=..4] run kill @s

# Insta Kill also works with the knife: give active players a huge melee attack damage so a single
# melee hit one-shots zombies (guns already insta-kill via the raycast path). remove+add keeps it
# idempotent each tick; the modifier is removed once the effect wears off.
execute as @a[scores={mgs.special.instant_kill=1..}] run attribute @s minecraft:attack_damage modifier remove mgs:insta_kill
execute as @a[scores={mgs.special.instant_kill=1..}] run attribute @s minecraft:attack_damage modifier add mgs:insta_kill 100000 add_value
execute as @a[scores={mgs.special.instant_kill=..0}] run attribute @s minecraft:attack_damage modifier remove mgs:insta_kill

# Blink state: toggles between 0 and 1 every 4 ticks (~0.2s half-cycle, matching BO2's 0.4s full cycle)
scoreboard players add #zb_blink_counter mgs.data 1
execute if score #zb_blink_counter mgs.data matches 4.. run scoreboard players set #zb_blink_counter mgs.data 0
execute if score #zb_blink_counter mgs.data matches 0 run scoreboard players add #zb_blink_state mgs.data 1
execute if score #zb_blink_state mgs.data matches 2.. run scoreboard players set #zb_blink_state mgs.data 0

# Decrement duration scoreboards
execute as @a[scores={mgs.special.double_points=1..}] run scoreboard players remove @s mgs.special.double_points 1

# Update bossbars
function mgs:v5.0.1/zombies/powerups/update_insta_kill_bb
function mgs:v5.0.1/zombies/powerups/update_double_points_bb
function mgs:v5.0.1/zombies/powerups/update_unlimited_ammo_bb

# Fire Sale: global timer countdown + price restore on expiry
execute if score #zb_fire_sale_timer mgs.data matches 1.. run function mgs:v5.0.1/zombies/powerups/fire_sale_tick

# Bonfire Sale: global timer countdown
execute if score #zb_bonfire_sale_timer mgs.data matches 1.. run function mgs:v5.0.1/zombies/powerups/bonfire_sale_tick

scoreboard players add #qr_price_tick mgs.data 1
execute if score #qr_price_tick mgs.data matches 20.. run scoreboard players set #qr_price_tick mgs.data 0
execute if score #qr_price_tick mgs.data matches 0 run function mgs:v5.0.1/zombies/perks/update_quick_revive_price

# Trap active tick (damage + timer)
execute as @e[tag=mgs.trap_center,scores={mgs.zb.trap.timer=1..}] at @s run function mgs:v5.0.1/zombies/traps/active_tick

# Trap cooldown uses expiration tick comparison (no per-tick decrements needed)

