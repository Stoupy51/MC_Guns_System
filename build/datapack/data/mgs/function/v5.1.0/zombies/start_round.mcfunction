
#> mgs:v5.1.0/zombies/start_round
#
# @within	mgs:v5.1.0/zombies/end_prep
#			mgs:v5.1.0/zombies/round_complete 5s [ scheduled ]
#			mgs:zombies/recover
#

# Increment round number
execute store result score #zb_round mgs.data run data get storage mgs:zombies game.round
scoreboard players add #zb_round mgs.data 1
execute store result storage mgs:zombies game.round int 1 run scoreboard players get #zb_round mgs.data

# Dog round: every 5th round from 5 on, and only on maps that placed special spawn markers
scoreboard players set #zb_dog_round mgs.data 0
scoreboard players operation #zb_dog_mod mgs.data = #zb_round mgs.data
scoreboard players operation #zb_dog_mod mgs.data %= #5 mgs.data
execute if score #zb_has_special mgs.data matches 1 if score #zb_round mgs.data matches 5.. if score #zb_dog_mod mgs.data matches 0 run scoreboard players set #zb_dog_round mgs.data 1

# Player count, clamped at 4, drives both round-size formulas
execute store result score #zb_player_count mgs.data if entity @a[scores={mgs.zb.in_game=1},gamemode=!spectator]
execute if score #zb_player_count mgs.data matches 5.. run scoreboard players set #zb_player_count mgs.data 4

# Enemy count for this round — see each subfunction for its curve
execute if score #zb_dog_round mgs.data matches 0 run function mgs:v5.1.0/zombies/calc_round_count_zombies
execute if score #zb_dog_round mgs.data matches 1 run function mgs:v5.1.0/zombies/calc_round_count_dogs

# Snapshot the round's total zombie count (zb_to_spawn is decremented as they spawn).
# Used by the power-up drop chance: min(5%, 2/total_round_zombies).
scoreboard players operation #zb_round_total mgs.data = #zb_to_spawn mgs.data

# Calculate initial spawn timer and batch size for this round
function mgs:v5.1.0/zombies/calc_spawn_timer

# Grace period: don't check game over for 3 seconds (60 ticks)
scoreboard players set #zb_round_grace mgs.data 60

# Reset stuck zombie glow timers
scoreboard players set #zb_stuck_timer mgs.data 0
scoreboard players set #zb_glow_timer mgs.data 0

# Reset the freeze watchdog: its counter survives between matches and would trip recovery early
scoreboard players set #zb_wd_ticks mgs.data 0

# Signal round start
function #mgs:zombies/on_round_start

# Refresh sidebar
function mgs:v5.1.0/zombies/refresh_sidebar

# Announce
execute if score #zb_dog_round mgs.data matches 0 run tellraw @a ["",{"text":"","color":"dark_green","bold":true},"🧟 ",{"translate":"mgs.round","color":"red"},{"score":{"name":"#zb_round","objective":"mgs.data"},"color":"gold","bold":true},[{"text":" ","color":"red"}, {"translate":"mgs.has_begun"}]]
execute if score #zb_dog_round mgs.data matches 0 as @a[scores={mgs.zb.in_game=1}] at @s run playsound mgs:zombies/round_start_generic ambient @s ~ ~ ~ 0.15 1.0

# Dog rounds get their own announcement + howl instead of the usual round jingle
execute if score #zb_dog_round mgs.data matches 1 run tellraw @a ["",{"text":"","color":"dark_red","bold":true},"🐺 ",{"translate":"mgs.round","color":"dark_red"},{"score":{"name":"#zb_round","objective":"mgs.data"},"color":"gold","bold":true},[{"text":" — ","color":"dark_red"}, {"translate":"mgs.the_hounds_are_loose"}]]
execute if score #zb_dog_round mgs.data matches 1 as @a[scores={mgs.zb.in_game=1}] at @s run playsound minecraft:entity.wolf.howl ambient @s ~ ~ ~ 1.0 0.6

# Replenish grenades for all alive players (+2, cap at 4)
execute as @a[scores={mgs.zb.in_game=1},gamemode=!spectator] run function mgs:v5.1.0/zombies/inventory/replenish_grenades

# Ability cooldowns + guardian summon (Zonweeb variant only)
execute if data storage mgs:zombies game{variant:"zonweeb"} run function mgs:v5.1.0/zombies/perks/reduce_cooldowns
execute if data storage mgs:zombies game{variant:"zonweeb"} run function mgs:v5.1.0/zombies/perks/check_guardian

# Reset per-round power-up drop tracking
scoreboard players set #zb_drops_this_round mgs.data 0
scoreboard players set #zb_cycle_done mgs.data 0

# Start a fresh shuffle bag for the round; its size = one full drop cycle's worth of drops
function mgs:v5.1.0/zombies/powerups/queue_refill
execute store result score #zb_cycle_len mgs.data run data get storage mgs:data _pu_queue

