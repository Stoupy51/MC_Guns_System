
#> mgs:v5.1.0/zombies/game_tick
#
# @within	mgs:v5.1.0/tick
#

# Revive system tick (process downed players)
function mgs:v5.1.0/zombies/revive/tick

# Call map-defined tick script
function mgs:v5.1.0/shared/maps/call_script_at_base {script:"tick"}

# Zombie Spawning (if there are still zombies to spawn)
execute if score #zb_to_spawn mgs.data matches 1.. run function mgs:v5.1.0/zombies/spawn_tick

# Rise animation tick for spawning zombies
execute as @e[tag=mgs.zb_rising] at @s run function mgs:v5.1.0/zombies/zombie_rise_tick

# Boundary enforcement (skip spectators, only if map has bounds)
execute if score #zb_has_bounds mgs.data matches 1 as @e[tag=mgs.zombie_round] at @s run function mgs:v5.1.0/shared/check_bounds
execute if score #zb_has_bounds mgs.data matches 1 as @e[type=player,scores={mgs.zb.in_game=1},gamemode=!creative,gamemode=!spectator] at @s run function mgs:v5.1.0/zombies/check_bounds_player

# Check round completion
execute store result score #zb_alive mgs.data if entity @e[tag=mgs.zombie_round]
# Dogs still telegraphing aren't entities yet, so #zb_alive can't see them. #zb_dog_pending is only
# a fast gate though: whenever it claims dogs are pending, resync it from the real portal count so a
# desynced counter can't freeze the run. That scan only runs on the tick the round would complete.
execute if score #zb_alive mgs.data matches 0 if score #zb_to_spawn mgs.data matches 0 if score #zb_dog_pending mgs.data matches 1.. store result score #zb_dog_pending mgs.data if entity @e[tag=mgs.dog_portal]
execute if score #zb_alive mgs.data matches 0 if score #zb_to_spawn mgs.data matches 0 if score #zb_dog_pending mgs.data matches ..0 run function mgs:v5.1.0/zombies/round_complete

# Check game over: only trigger when no healthy AND no downed players remain
# - Healthy: downed=0, gamemode=!spectator (playing normally)
# - Downed: downed=1, gamemode=spectator (spectating their mannequin, can be revived)
# - Bled out: downed=0, gamemode=spectator (waiting for next round — truly dead)
execute if score #zb_round_grace mgs.data matches 1.. run scoreboard players remove #zb_round_grace mgs.data 1
execute unless score #zb_round_grace mgs.data matches 1.. store result score #zb_alive_players mgs.data if entity @a[scores={mgs.zb.in_game=1,mgs.zb.downed=0},gamemode=!spectator]
execute unless score #zb_round_grace mgs.data matches 1.. store result score #zb_downed_alive mgs.data if entity @a[scores={mgs.zb.in_game=1,mgs.zb.downed=1},gamemode=spectator]
execute unless score #zb_round_grace mgs.data matches 1.. run scoreboard players operation #zb_alive_players mgs.data += #zb_downed_alive mgs.data
execute unless score #zb_round_grace mgs.data matches 1.. if score #zb_alive_players mgs.data matches 0 run function mgs:v5.1.0/zombies/game_over

# Stuck zombie check (every 20 ticks, 24 random non-rising zombies; escorted ones are NoAI
# and already being rescued by their trader — see escort.py)
execute store result score #zb_tick_mod mgs.data run scoreboard players get #total_tick mgs.data
scoreboard players operation #zb_tick_mod mgs.data %= #20 mgs.data
execute if score #zb_tick_mod mgs.data matches 0 as @e[tag=mgs.zombie_round,tag=!mgs.zb_rising,tag=!mgs.zb_escorted,limit=24,sort=random] at @s run function mgs:v5.1.0/zombies/stuck_zombie_check

# Stuck zombie glow: count up once all spawns are done (60s = 1200 ticks after last spawn)
execute if score #zb_to_spawn mgs.data matches 0 run scoreboard players add #zb_stuck_timer mgs.data 1
execute if score #zb_to_spawn mgs.data matches 1.. run scoreboard players set #zb_stuck_timer mgs.data 0
# Once threshold reached, tick glow refresh timer (every 5s = 100 ticks → apply glowing for 6s = 120 ticks)
execute if score #zb_stuck_timer mgs.data matches 1200.. run scoreboard players add #zb_glow_timer mgs.data 1
execute if score #zb_glow_timer mgs.data matches 100.. run scoreboard players set #zb_glow_timer mgs.data 0
execute if score #zb_stuck_timer mgs.data matches 1200.. if score #zb_glow_timer mgs.data matches 0 if score #zb_alive mgs.data matches 1.. run function mgs:v5.1.0/zombies/glow_stuck_zombies

# Last-zombies fast path: once every zombie has spawned and only a handful remain, don't make
# players wait the full 60s before stragglers glow — glow them immediately (every 100t) so a
# single hard-to-find zombie can't drag the round out (common complaint from ~round 10 on).
execute unless score #zb_alive mgs.data matches 1..3 run scoreboard players set #zb_fewleft_timer mgs.data 0
execute if score #zb_to_spawn mgs.data matches 0 if score #zb_alive mgs.data matches 1..3 run scoreboard players add #zb_fewleft_timer mgs.data 1
execute if score #zb_fewleft_timer mgs.data matches 1 run function mgs:v5.1.0/zombies/glow_stuck_zombies
execute if score #zb_fewleft_timer mgs.data matches 100.. run scoreboard players set #zb_fewleft_timer mgs.data 0

# Refresh sidebar every 5 ticks.
scoreboard players add #zb_sidebar_timer mgs.data 1
execute if score #zb_sidebar_timer mgs.data matches 5.. run scoreboard players set #zb_sidebar_timer mgs.data 0
execute if score #zb_sidebar_timer mgs.data matches 0 run function mgs:v5.1.0/zombies/refresh_sidebar

# Cleanup
kill @e[type=experience_orb]

# Award kill points from totalKillCount delta
execute as @a[scores={mgs.zb.in_game=1},gamemode=!spectator] run function mgs:v5.1.0/zombies/check_kill_points

# Intercept dying zombies before vanilla death particles are emitted.
function mgs:v5.1.0/zombies/death_watch_tick

# Freeze watchdog: auto-recover a round that has stopped advancing (see watchdog_tick).
function mgs:v5.1.0/zombies/watchdog_tick

# Dog spawn portals: 1.5s of sparks, then the bolt. Gated on the round kind, NOT on
# #zb_dog_pending — a portal orphaned by a desynced counter would then never tick, never strike and
# never die, which is the freeze the resync in game_tick pairs with this to rule out.
execute if score #zb_dog_round mgs.data matches 1 as @e[tag=mgs.dog_portal] at @s run function mgs:v5.1.0/zombies/dog_portal_tick

# Safety net: a dog that missed its scaling call is a vanilla 8-HP wolf, which reads as a bug
# (one-punch kills) rather than as a difficulty setting. types/dog is idempotent and tags what it
# scales, so this costs one tag-filtered scan and normally matches nothing.
execute if score #zb_dog_round mgs.data matches 1 as @e[tag=mgs.zb_dog,tag=!mgs.zb_scaled] run function mgs:v5.1.0/zombies/types/dog

# Wolves are neutral mobs and hunt nothing without an anger target. Writing `angry_at` alone is
# enough (the game calls setTarget() from it on reload, then sustains the timer); writing AngerTime
# does nothing, as the always-saved `anger_end_time` outranks it. The `unless data` guard means a
# dog already locked on costs a read and no write. #zb_tick_mod is total_tick % 20 from earlier.
execute if score #zb_dog_round mgs.data matches 1 if score #zb_tick_mod mgs.data matches 0 as @e[tag=mgs.zb_dog,tag=!mgs.zb_rising] at @s unless data entity @s angry_at run data modify entity @s angry_at set from entity @p[scores={mgs.zb.in_game=1},gamemode=!spectator,gamemode=!creative] UUID

# Managed horde ambience: ~every 35 ticks, give each player one controlled, count-scaled groan.
# Skipped on dog rounds: dogs aren't summoned Silent, so their own growls are the ambience.
scoreboard players add #zb_horde_timer mgs.data 1
execute if score #zb_horde_timer mgs.data matches 35.. run scoreboard players set #zb_horde_timer mgs.data 0
execute if score #zb_dog_round mgs.data matches 0 if score #zb_horde_timer mgs.data matches 0 as @a[scores={mgs.zb.in_game=1},gamemode=!spectator] at @s run function mgs:v5.1.0/zombies/horde_ambient

# Escort system (escort.py): drag escorted zombies behind their pathfinding traders
execute if score #zb_escort_count mgs.data matches 1.. as @e[tag=mgs.zb_escorted] at @s run function mgs:v5.1.0/zombies/escort/zombie_tick

# Interaction safeguard (count-INDEPENDENT, every tick)
execute as @e[type=minecraft:wandering_trader,tag=mgs.zb_escort,tag=!mgs.zb_escort_monkey] at @s if entity @p[scores={mgs.zb.in_game=1,mgs.zb.downed=0},gamemode=!spectator,distance=..6] run function mgs:v5.1.0/zombies/escort/end_at_trader

# Every 2s: resync the escort counter from reality
scoreboard players operation #zb_esc_sweep mgs.data = #total_tick mgs.data
scoreboard players operation #zb_esc_sweep mgs.data %= #40 mgs.data
execute if score #zb_esc_sweep mgs.data matches 0 store result score #zb_escort_count mgs.data if entity @e[tag=mgs.zb_escorted]
execute if score #zb_esc_sweep mgs.data matches 0 as @e[type=minecraft:wandering_trader,tag=mgs.zb_escort] at @s unless entity @e[tag=mgs.zb_escorted,distance=..8] run function mgs:v5.1.0/zombies/escort/discard_trader

# PaP-room lure: recompute lure state every 2s (inert unless the map defined a lure centre)
execute if score #zb_esc_sweep mgs.data matches 20 if score #zb_pap_has mgs.data matches 1 run function mgs:v5.1.0/zombies/escort/update_lure

# Ability tick (Zonweeb variant only)
execute if data storage mgs:zombies game{variant:"zonweeb"} run function mgs:v5.1.0/zombies/ability_tick

# Refresh player info item every 5 seconds (100 ticks)
scoreboard players add #zb_info_timer mgs.data 1
execute if score #zb_info_timer mgs.data matches 100.. run scoreboard players set #zb_info_timer mgs.data 0
execute if score #zb_info_timer mgs.data matches 0 as @a[scores={mgs.zb.in_game=1},gamemode=!spectator] if items entity @s hotbar.8 *[custom_data~{mgs:{zb_info:true,zombies:{hotbar:8}}}] run function mgs:v5.1.0/zombies/inventory/refresh_info_item

# Mystery box animation tick
function mgs:v5.1.0/zombies/mystery_box/tick

# PAP animation tick (all phases use positive timer: 300→0)
execute as @e[type=minecraft:interaction,tag=mgs.pap_machine,scores={mgs.pap_anim=1..}] at @s run function mgs:v5.1.0/zombies/pap/anim/step

# Timeslip: two extra steps this tick for Timeslip-owned machines (3x total speed)
execute as @e[type=minecraft:interaction,tag=mgs.pap_machine,scores={mgs.zb.pap.timeslip=1,mgs.pap_anim=1..}] at @s run function mgs:v5.1.0/zombies/pap/anim/step_timeslip

# Barriers: restore frozen speeds from last tick, then dispatch all display ticks
execute as @e[tag=mgs.zombie_round,tag=mgs.barrier_frozen] run function mgs:v5.1.0/zombies/barriers/restore_zombie_speed
execute as @e[type=minecraft:block_display,tag=mgs.barrier_display] at @s run function mgs:v5.1.0/zombies/barriers/tick

# Refresh barricade brightness every 5s (local light can change: doors, power, placed lights)
scoreboard players add #barrier_bright_timer mgs.data 1
execute if score #barrier_bright_timer mgs.data matches 100.. run scoreboard players set #barrier_bright_timer mgs.data 0
execute if score #barrier_bright_timer mgs.data matches 0 as @e[type=minecraft:block_display,tag=mgs.barrier_display] at @s run function mgs:v5.1.0/zombies/barriers/compute_brightness

# Power-up entities exist only after a drop. #pu_active (maintained on spawn/expire/pickup) gates the
# two per-tick scans below so an empty board costs nothing. Resync once every 40 ticks as a safety net
# (the count is already exact since pu_item is Invulnerable and only dies through tracked paths).
execute store result score #pu_active_phase mgs.data run scoreboard players get #total_tick mgs.data
scoreboard players operation #pu_active_phase mgs.data %= #40 mgs.data
execute if score #pu_active_phase mgs.data matches 0 store result score #pu_active mgs.data if entity @e[type=minecraft:item,tag=mgs.pu_item]

# Power-up entity tick (lifetime countdown, blink, pickup detection)
execute if score #pu_active mgs.data matches 1.. as @e[type=minecraft:item,tag=mgs.pu_item] at @s run function mgs:v5.1.0/zombies/powerups/entity_tick

# Orphan cleanup: a text_display whose item entity was destroyed (burned/exploded) would never
# be removed by expire/pickup — kill any pu_text that no longer has a pu_item beneath it.
execute if score #pu_active mgs.data matches 1.. as @e[type=minecraft:text_display,tag=mgs.pu_text] at @s unless entity @e[type=minecraft:item,tag=mgs.pu_item,distance=..4] run kill @s

# Insta Kill also works with the knife: give active players a huge melee attack damage so a single
# melee hit one-shots zombies (guns already insta-kill via the raycast path). The mgs.ik_melee tag
# tracks who currently carries the modifier, so the attribute commands only run on state
# transitions (they used to run for EVERY player EVERY tick, mostly as guaranteed failures).
execute as @a[tag=!mgs.ik_melee,scores={mgs.special.instant_kill=1..}] run function mgs:v5.1.0/zombies/powerups/insta_kill_melee_on
execute as @a[tag=mgs.ik_melee,scores={mgs.special.instant_kill=..0}] run function mgs:v5.1.0/zombies/powerups/insta_kill_melee_off

# Blink state: toggles between 0 and 1 every 4 ticks (~0.2s half-cycle, matching BO2's 0.4s full cycle)
scoreboard players add #zb_blink_counter mgs.data 1
execute if score #zb_blink_counter mgs.data matches 4.. run scoreboard players set #zb_blink_counter mgs.data 0
execute if score #zb_blink_counter mgs.data matches 0 run scoreboard players add #zb_blink_state mgs.data 1
execute if score #zb_blink_state mgs.data matches 2.. run scoreboard players set #zb_blink_state mgs.data 0

# Decrement duration scoreboards
execute as @a[scores={mgs.special.double_points=1..}] run scoreboard players operation @s mgs.special.double_points -= #tick_delta mgs.data

# Update bossbars
function mgs:v5.1.0/zombies/powerups/update_insta_kill_bb
function mgs:v5.1.0/zombies/powerups/update_double_points_bb
function mgs:v5.1.0/zombies/powerups/update_unlimited_ammo_bb

# Fire Sale: global timer countdown + price restore on expiry
execute if score #zb_fire_sale_timer mgs.data matches 1.. run function mgs:v5.1.0/zombies/powerups/fire_sale_tick

# Bonfire Sale: global timer countdown
execute if score #zb_bonfire_sale_timer mgs.data matches 1.. run function mgs:v5.1.0/zombies/powerups/bonfire_sale_tick

execute as @e[tag=mgs.tombstone,scores={mgs.zb.ts.state=1}] at @s run function mgs:v5.1.0/zombies/perks/tombstone_marker_tick

scoreboard players add #qr_price_tick mgs.data 1
execute if score #qr_price_tick mgs.data matches 20.. run scoreboard players set #qr_price_tick mgs.data 0
execute if score #qr_price_tick mgs.data matches 0 run function mgs:v5.1.0/zombies/perks/update_quick_revive_price

execute as @e[type=item_display,tag=mgs.wunderfizz_orb] at @s run function mgs:v5.1.0/zombies/wunderfizz/orb_tick
execute if score #wf_move_timer mgs.data matches 1.. run function mgs:v5.1.0/zombies/wunderfizz/move_tick

execute if data storage mgs:zombies game{state:"active"} run function mgs:v5.1.0/zombies/whos_who/tick

# Trap active tick (damage + timer)
execute as @e[type=minecraft:marker,tag=mgs.trap_center,scores={mgs.zb.trap.timer=1..}] at @s run function mgs:v5.1.0/zombies/traps/active_tick

# Trap cooldown tick (wall-clock via #tick_delta, same basis as the active timer)
execute as @e[type=minecraft:marker,tag=mgs.trap_center,scores={mgs.zb.trap.cd=1..}] run function mgs:v5.1.0/zombies/traps/cooldown_tick

