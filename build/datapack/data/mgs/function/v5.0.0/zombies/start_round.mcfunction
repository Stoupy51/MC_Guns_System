
#> mgs:v5.0.0/zombies/start_round
#
# @within	mgs:v5.0.0/zombies/end_prep
#			mgs:v5.0.0/zombies/round_complete 200t [ scheduled ]
#

# Increment round number
execute store result score #zb_round mgs.data run data get storage mgs:zombies game.round
scoreboard players add #zb_round mgs.data 1
execute store result storage mgs:zombies game.round int 1 run scoreboard players get #zb_round mgs.data

# Calculate zombies to spawn this round: base formula = round * 4 + (player_count - 1) * 2
execute store result score #zb_player_count mgs.data if entity @a[scores={mgs.zb.in_game=1},gamemode=!spectator]
scoreboard players remove #zb_player_count mgs.data 1
scoreboard players operation #zb_player_count mgs.data *= #2 mgs.data
scoreboard players operation #zb_to_spawn mgs.data = #zb_round mgs.data
scoreboard players operation #zb_to_spawn mgs.data *= #4 mgs.data
scoreboard players operation #zb_to_spawn mgs.data += #zb_player_count mgs.data

# Store zombies to spawn and remaining count
scoreboard players operation #zb_remaining mgs.data = #zb_to_spawn mgs.data

# Set spawn timer (spawn a zombie every 2 seconds = 40 ticks)
scoreboard players set #zb_spawn_timer mgs.data 20

# Grace period: don't check game over for 3 seconds (60 ticks)
scoreboard players set #zb_round_grace mgs.data 60

# Title
title @a[scores={mgs.zb.in_game=1}] times 10 40 10
title @a[scores={mgs.zb.in_game=1}] title [{"text":"Round ","color":"red","bold":true},{"score":{"name":"#zb_round","objective":"mgs.data"},"color":"gold","bold":true}]

# Signal round start
function #mgs:zombies/on_round_start

# Refresh sidebar
function mgs:v5.0.0/zombies/refresh_sidebar

# Announce
tellraw @a ["",{"text":"","color":"dark_green","bold":true},"🧟 ",{"text":"Round ","color":"red"},{"score":{"name":"#zb_round","objective":"mgs.data"},"color":"gold","bold":true},{"translate": "mgs.has_begun","color":"red"}]

# Reduce ability cooldowns
function mgs:v5.0.0/zombies/perks/reduce_cooldowns

# Check guardian ability (summon golem at round start)
function mgs:v5.0.0/zombies/perks/check_guardian

