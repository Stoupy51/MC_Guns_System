
#> mgs:v5.1.0/zombies/game_tick
#
# @within	mgs:v5.1.0/tick
#

function mgs:v5.1.0/zombies/revive/tick

function mgs:v5.1.0/shared/maps/call_script_at_base {script:"tick"}

execute if score #zb_to_spawn mgs.data matches 1.. run function mgs:v5.1.0/zombies/spawn_tick

# Untyped: other enemies than zombies will rise too.
execute as @e[tag=mgs.zb_rising] at @s run function mgs:v5.1.0/zombies/zombie_rise_tick

# Only when the map has bounds.
execute if score #zb_has_bounds mgs.data matches 1 as @e[tag=mgs.zombie_round] at @s run function mgs:v5.1.0/shared/check_bounds
execute if score #zb_has_bounds mgs.data matches 1 as @e[type=player,scores={mgs.zb.in_game=1},gamemode=!creative,gamemode=!spectator] at @s run function mgs:v5.1.0/zombies/check_bounds_player

execute store result score #zb_alive mgs.data if entity @e[tag=mgs.zombie_round]
# Dogs still in their portal are not entities. #zb_dog_pending is only a fast gate: when it claims pending dogs,
# it is resynced from the real portal count so a desynced counter cannot freeze the run.
execute if score #zb_alive mgs.data matches 0 if score #zb_to_spawn mgs.data matches 0 if score #zb_dog_pending mgs.data matches 1.. store result score #zb_dog_pending mgs.data if entity @e[type=minecraft:marker,tag=mgs.dog_portal]
execute if score #zb_alive mgs.data matches 0 if score #zb_to_spawn mgs.data matches 0 if score #zb_dog_pending mgs.data matches ..0 run function mgs:v5.1.0/zombies/round_complete

# Game over once nobody is left to revive anyone. Healthy: downed=0, not spectator (Who's Who owners included);
# downed: downed=1, spectator; bled out: downed=0, spectator. Solo Quick Revive with uses left revives on its own.
execute if score #zb_round_grace mgs.data matches 1.. run scoreboard players remove #zb_round_grace mgs.data 1
execute unless score #zb_round_grace mgs.data matches 1.. store result score #zb_alive_players mgs.data if entity @a[scores={mgs.zb.in_game=1,mgs.zb.downed=0},gamemode=!spectator]
execute unless score #zb_round_grace mgs.data matches 1.. if score #zb_alive_players mgs.data matches 0 store result score #zb_ingame_total mgs.data if entity @a[scores={mgs.zb.in_game=1}]
execute unless score #zb_round_grace mgs.data matches 1.. if score #zb_alive_players mgs.data matches 0 if score #zb_ingame_total mgs.data matches 1 store success score #zb_alive_players mgs.data as @a[scores={mgs.zb.in_game=1,mgs.zb.downed=1},tag=mgs.zb_qr_armed] unless score @s mgs.zb.qr_uses matches 3..

# Nobody left for two ticks in a row, so a revive or respawn landing on the same tick cannot end the run.
execute unless score #zb_round_grace mgs.data matches 1.. if score #zb_alive_players mgs.data matches 1.. run scoreboard players set #zb_nobody_ticks mgs.data 0
execute unless score #zb_round_grace mgs.data matches 1.. if score #zb_alive_players mgs.data matches 0 run scoreboard players add #zb_nobody_ticks mgs.data 1
execute unless score #zb_round_grace mgs.data matches 1.. if score #zb_nobody_ticks mgs.data matches 2.. run function mgs:v5.1.0/zombies/game_over

# Every 20 ticks, 24 random non-rising zombies; escorted ones are NoAI and already being rescued (see escort).
execute store result score #zb_tick_mod mgs.data run scoreboard players get #total_tick mgs.data
scoreboard players operation #zb_tick_mod mgs.data %= #20 mgs.data
execute if score #zb_tick_mod mgs.data matches 0 as @e[tag=mgs.zombie_round,tag=!mgs.zb_rising,tag=!mgs.zb_escorted,limit=24,sort=random] at @s run function mgs:v5.1.0/zombies/stuck_zombie_check

# Every player in the run glows yellow.
execute if score #zb_tick_mod mgs.data matches 0 run effect give @a[scores={mgs.zb.in_game=1},gamemode=!spectator] minecraft:glowing 3 0 true

# Stragglers glow 60 s (1200 ticks) after the last spawn.
execute if score #zb_to_spawn mgs.data matches 0 run scoreboard players add #zb_stuck_timer mgs.data 1
execute if score #zb_to_spawn mgs.data matches 1.. run scoreboard players set #zb_stuck_timer mgs.data 0
# Then glowing for 6 s every 5 s.
execute if score #zb_stuck_timer mgs.data matches 1200.. run scoreboard players add #zb_glow_timer mgs.data 1
execute if score #zb_glow_timer mgs.data matches 100.. run scoreboard players set #zb_glow_timer mgs.data 0
execute if score #zb_stuck_timer mgs.data matches 1200.. if score #zb_glow_timer mgs.data matches 0 if score #zb_alive mgs.data matches 1.. run function mgs:v5.1.0/zombies/glow_stuck_zombies

# With 3 or fewer zombies left they glow every 5 s right away, so one hard-to-find zombie cannot drag the round out.
execute unless score #zb_alive mgs.data matches 1..3 run scoreboard players set #zb_fewleft_timer mgs.data 0
execute if score #zb_to_spawn mgs.data matches 0 if score #zb_alive mgs.data matches 1..3 run scoreboard players add #zb_fewleft_timer mgs.data 1
execute if score #zb_fewleft_timer mgs.data matches 1 run function mgs:v5.1.0/zombies/glow_stuck_zombies
execute if score #zb_fewleft_timer mgs.data matches 100.. run scoreboard players set #zb_fewleft_timer mgs.data 0

scoreboard players add #zb_sidebar_timer mgs.data 1
execute if score #zb_sidebar_timer mgs.data matches 5.. run scoreboard players set #zb_sidebar_timer mgs.data 0
execute if score #zb_sidebar_timer mgs.data matches 0 run function mgs:v5.1.0/zombies/refresh_sidebar

kill @e[type=experience_orb]

execute as @a[scores={mgs.zb.in_game=1},gamemode=!spectator] run function mgs:v5.1.0/zombies/check_kill_points

# Before vanilla death particles.
function mgs:v5.1.0/zombies/death_watch_tick

# Recovers a round that stopped advancing (see watchdog_tick).
function mgs:v5.1.0/zombies/watchdog_tick

# Gated on the round kind, not #zb_dog_pending: a portal orphaned by a desynced counter would never tick, strike or die.
execute if score #zb_dog_round mgs.data matches 1 as @e[type=minecraft:marker,tag=mgs.dog_portal] at @s run function mgs:v5.1.0/zombies/dog_portal_tick

# A dog that missed its scaling is a vanilla 8 HP wolf. types/dog tags what it scales, so this normally matches nothing.
execute if score #zb_dog_round mgs.data matches 1 as @e[type=minecraft:wolf,tag=mgs.zb_dog,tag=!mgs.zb_scaled] run function mgs:v5.1.0/zombies/types/dog

# Wolves hunt nothing without an anger target. `angry_at` alone is enough (setTarget runs from it on reload);
# AngerTime does nothing, the saved anger_end_time outranks it. #zb_tick_mod is total_tick % 20.
execute if score #zb_dog_round mgs.data matches 1 if score #zb_tick_mod mgs.data matches 0 as @e[type=minecraft:wolf,tag=mgs.zb_dog,tag=!mgs.zb_rising] at @s unless data entity @s angry_at run data modify entity @s angry_at set from entity @p[scores={mgs.zb.in_game=1},gamemode=!spectator,gamemode=!creative] UUID

# Each player's cooldown is refreshed by horde_ambient from the zombie count near them; it also owns the sprint channel.
# Skipped on dog rounds: dogs are not Silent, their growls are the ambience.
scoreboard players remove @a[scores={mgs.zb.in_game=1,mgs.zb.horde_cd=1..}] mgs.zb.horde_cd 1
execute if score #zb_dog_round mgs.data matches 0 as @a[scores={mgs.zb.in_game=1,mgs.zb.horde_cd=..0},gamemode=!spectator] at @s run function mgs:v5.1.0/zombies/horde_ambient

execute if score #zb_escort_count mgs.data matches 1.. as @e[tag=mgs.zb_escorted] at @s run function mgs:v5.1.0/zombies/escort/zombie_tick

# Interaction safeguard, every tick. Monkey and walk-to escorts are exempt: map makers aim walks where the action is,
# so it would cancel them short of the target. Their eaten click is recovered in weapon/common.
execute as @e[type=minecraft:wandering_trader,tag=mgs.zb_escort,tag=!mgs.zb_escort_monkey,tag=!mgs.zb_escort_walk] at @s if entity @p[scores={mgs.zb.in_game=1,mgs.zb.downed=0},gamemode=!spectator,distance=..6] run function mgs:v5.1.0/zombies/escort/end_at_trader

# Every 2 s the counter is resynced from the entities.
scoreboard players operation #zb_esc_sweep mgs.data = #total_tick mgs.data
scoreboard players operation #zb_esc_sweep mgs.data %= #40 mgs.data
execute if score #zb_esc_sweep mgs.data matches 0 store result score #zb_escort_count mgs.data if entity @e[tag=mgs.zb_escorted]
execute if score #zb_esc_sweep mgs.data matches 0 as @e[type=minecraft:wandering_trader,tag=mgs.zb_escort] at @s unless entity @e[tag=mgs.zb_escorted,distance=..8] run function mgs:v5.1.0/zombies/escort/discard_trader

# Inert unless the map defined a lure centre.
execute if score #zb_esc_sweep mgs.data matches 20 if score #zb_pap_has mgs.data matches 1 run function mgs:v5.1.0/zombies/escort/update_lure

# Zonweeb only.
execute if data storage mgs:zombies game{variant:"zonweeb"} run function mgs:v5.1.0/zombies/ability_tick

# Every 5 s.
scoreboard players add #zb_info_timer mgs.data 1
execute if score #zb_info_timer mgs.data matches 100.. run scoreboard players set #zb_info_timer mgs.data 0
execute if score #zb_info_timer mgs.data matches 0 as @a[scores={mgs.zb.in_game=1},gamemode=!spectator] if items entity @s hotbar.8 *[custom_data~{mgs:{zb_info:true,zombies:{hotbar:8}}}] run function mgs:v5.1.0/zombies/inventory/refresh_info_item

function mgs:v5.1.0/zombies/mystery_box/tick

# The timer counts down from 300.
execute as @e[type=minecraft:interaction,tag=mgs.pap_machine,scores={mgs.pap_anim=1..}] at @s run function mgs:v5.1.0/zombies/pap/anim/step

# Timeslip: two extra steps per tick (3x).
execute as @e[type=minecraft:interaction,tag=mgs.pap_machine,scores={mgs.zb.pap.timeslip=1,mgs.pap_anim=1..}] at @s run function mgs:v5.1.0/zombies/pap/anim/step_timeslip

# Speeds frozen last tick are restored first.
execute as @e[tag=mgs.zombie_round,tag=mgs.barricade_frozen] run function mgs:v5.1.0/zombies/barricades/restore_zombie_speed
execute as @e[type=minecraft:block_display,tag=mgs.barricade_display] at @s run function mgs:v5.1.0/zombies/barricades/tick

# Every 5 s, since local light can change (doors, power, placed lights).
scoreboard players add #barricade_bright_timer mgs.data 1
execute if score #barricade_bright_timer mgs.data matches 100.. run scoreboard players set #barricade_bright_timer mgs.data 0
execute if score #barricade_bright_timer mgs.data matches 0 as @e[type=minecraft:block_display,tag=mgs.barricade_display] at @s run function mgs:v5.1.0/zombies/barricades/compute_brightness

# #pu_active (kept on spawn, expire and pickup) gates the two scans below. Resynced every 40 ticks as a safety net:
# pu_item is Invulnerable and only dies through tracked paths.
execute store result score #pu_active_phase mgs.data run scoreboard players get #total_tick mgs.data
scoreboard players operation #pu_active_phase mgs.data %= #40 mgs.data
execute if score #pu_active_phase mgs.data matches 0 store result score #pu_active mgs.data if entity @e[type=minecraft:item,tag=mgs.pu_item]

execute if score #pu_active mgs.data matches 1.. as @e[type=minecraft:item,tag=mgs.pu_item] at @s run function mgs:v5.1.0/zombies/powerups/entity_tick

# A text_display whose item burned or exploded is never removed by expire or pickup.
execute if score #pu_active mgs.data matches 1.. as @e[type=minecraft:text_display,tag=mgs.pu_text] at @s unless entity @e[type=minecraft:item,tag=mgs.pu_item,distance=..4] run kill @s

# Insta Kill also works with the knife through a huge melee damage modifier (guns insta-kill in the raycast).
# The ik_melee tag marks who carries it, so the attribute commands only run on transitions.
execute as @a[tag=!mgs.ik_melee,scores={mgs.special.instant_kill=1..}] run function mgs:v5.1.0/zombies/powerups/insta_kill_melee_on
execute as @a[tag=mgs.ik_melee,scores={mgs.special.instant_kill=..0}] run function mgs:v5.1.0/zombies/powerups/insta_kill_melee_off

# Toggles every 4 ticks, BO2's 0.4 s blink cycle.
scoreboard players add #zb_blink_counter mgs.data 1
execute if score #zb_blink_counter mgs.data matches 4.. run scoreboard players set #zb_blink_counter mgs.data 0
execute if score #zb_blink_counter mgs.data matches 0 run scoreboard players add #zb_blink_state mgs.data 1
execute if score #zb_blink_state mgs.data matches 2.. run scoreboard players set #zb_blink_state mgs.data 0

execute as @a[scores={mgs.special.double_points=1..}] run scoreboard players operation @s mgs.special.double_points -= #tick_delta mgs.data

function mgs:v5.1.0/zombies/powerups/update_insta_kill_bb
function mgs:v5.1.0/zombies/powerups/update_double_points_bb
function mgs:v5.1.0/zombies/powerups/update_unlimited_ammo_bb

execute if score #zb_fire_sale_timer mgs.data matches 1.. run function mgs:v5.1.0/zombies/powerups/fire_sale_tick

execute if score #zb_bonfire_sale_timer mgs.data matches 1.. run function mgs:v5.1.0/zombies/powerups/bonfire_sale_tick

execute as @e[type=minecraft:item_display,tag=mgs.tombstone,scores={mgs.zb.ts.state=1}] at @s run function mgs:v5.1.0/zombies/perks/tombstone_marker_tick

scoreboard players add #qr_price_tick mgs.data 1
execute if score #qr_price_tick mgs.data matches 20.. run scoreboard players set #qr_price_tick mgs.data 0
execute if score #qr_price_tick mgs.data matches 0 run function mgs:v5.1.0/zombies/perks/update_quick_revive_price

execute as @e[type=item_display,tag=mgs.wunderfizz_orb] at @s run function mgs:v5.1.0/zombies/wunderfizz/orb_tick
execute if score #wf_move_timer mgs.data matches 1.. run function mgs:v5.1.0/zombies/wunderfizz/move_tick

execute if data storage mgs:zombies game{state:"active"} run function mgs:v5.1.0/zombies/whos_who/tick

execute as @e[type=minecraft:marker,tag=mgs.trap_center,scores={mgs.zb.trap.timer=1..}] at @s run function mgs:v5.1.0/zombies/traps/active_tick

# Real time through #tick_delta, like the active timer.
execute as @e[type=minecraft:marker,tag=mgs.trap_center,scores={mgs.zb.trap.cd=1..}] run function mgs:v5.1.0/zombies/traps/cooldown_tick

execute as @a[scores={mgs.zb.in_game=1}] run function mgs:v5.1.0/zombies/xp/track_points

