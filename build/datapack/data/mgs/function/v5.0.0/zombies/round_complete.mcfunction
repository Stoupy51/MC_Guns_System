
#> mgs:v5.0.0/zombies/round_complete
#
# @within	mgs:v5.0.0/zombies/game_tick
#

# Guard: prevent re-triggering every tick
scoreboard players set #zb_to_spawn mgs.data -1

# Signal round end
function #mgs:zombies/on_round_end

# Title
title @a[scores={mgs.zb.in_game=1}] times 10 40 10
title @a[scores={mgs.zb.in_game=1}] title [{"translate":"mgs.round_complete","color":"green","bold":true}]

# Give all players 500 bonus points for surviving the round
execute as @a[scores={mgs.zb.in_game=1},gamemode=!spectator] run scoreboard players add @s mgs.zb.points 500

# Announce
execute store result score #completed_round mgs.data run data get storage mgs:zombies game.round
tellraw @a ["",{"text":"","color":"dark_green","bold":true},"🧟 ",{"translate":"mgs.round","color":"green"},{"score":{"name":"#completed_round","objective":"mgs.data"},"color":"gold","bold":true},{"translate":"mgs.complete_500_points_next_round_in_10_seconds","color":"green"}]

# Schedule next round after 10 seconds
schedule function mgs:v5.0.0/zombies/start_round 200t

# Respawn all bled-out (spectator) players for the next round
function mgs:v5.0.0/zombies/revive/round_respawn

