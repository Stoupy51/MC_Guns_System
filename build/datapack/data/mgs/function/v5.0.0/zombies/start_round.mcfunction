
#> mgs:v5.0.0/zombies/start_round
#
# @within	mgs:v5.0.0/zombies/end_prep
#			mgs:v5.0.0/zombies/round_complete 5s [ scheduled ]
#

# Increment round number
execute store result score #zb_round mgs.data run data get storage mgs:zombies game.round
scoreboard players add #zb_round mgs.data 1
execute store result storage mgs:zombies game.round int 1 run scoreboard players get #zb_round mgs.data

# Calculate zombies to spawn this round: min(48, 7 + round) * min(4, player_count)
# Solo player: r1=8,  r5=12, r10=17, r20=27,  r40=47,  r41+ caps at 48
# 4+ players:  r1=32, r5=48, r10=68, r20=108, r40=188, r41+ caps at 192
execute store result score #zb_player_count mgs.data if entity @a[scores={mgs.zb.in_game=1},gamemode=!spectator]
execute if score #zb_player_count mgs.data matches 5.. run scoreboard players set #zb_player_count mgs.data 4
scoreboard players operation #zb_to_spawn mgs.data = #zb_round mgs.data
scoreboard players add #zb_to_spawn mgs.data 7
execute if score #zb_to_spawn mgs.data matches 49.. run scoreboard players set #zb_to_spawn mgs.data 48
scoreboard players operation #zb_to_spawn mgs.data *= #zb_player_count mgs.data

# Store zombies to spawn and remaining count
scoreboard players operation #zb_remaining mgs.data = #zb_to_spawn mgs.data

# Calculate initial spawn timer and batch size for this round
function mgs:v5.0.0/zombies/calc_spawn_timer

# Grace period: don't check game over for 3 seconds (60 ticks)
scoreboard players set #zb_round_grace mgs.data 60

# Reset stuck zombie glow timers
scoreboard players set #zb_stuck_timer mgs.data 0
scoreboard players set #zb_glow_timer mgs.data 0

# Signal round start
function #mgs:zombies/on_round_start

# Refresh sidebar
function mgs:v5.0.0/zombies/refresh_sidebar

# Announce
tellraw @a ["",{"text":"","color":"dark_green","bold":true},"🧟 ",{"translate":"mgs.round","color":"red"},{"score":{"name":"#zb_round","objective":"mgs.data"},"color":"gold","bold":true},[{"text":" ","color":"red"}, {"translate":"mgs.has_begun"}]]

# Replenish grenades for all alive players (+2, cap at 4)
execute as @a[scores={mgs.zb.in_game=1},gamemode=!spectator] run function mgs:v5.0.0/zombies/inventory/replenish_grenades

# Reduce ability cooldowns
function mgs:v5.0.0/zombies/perks/reduce_cooldowns

# Check guardian ability (summon golem at round start)
function mgs:v5.0.0/zombies/perks/check_guardian

