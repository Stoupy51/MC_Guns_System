
#> mgs:v5.0.0/zombies/round_complete
#
# @within	mgs:v5.0.0/zombies/game_tick
#

# Guard: prevent re-triggering every tick
scoreboard players set #zb_to_spawn mgs.data -1

# Signal round end
function #mgs:zombies/on_round_end

# Announce
execute store result score #completed_round mgs.data run data get storage mgs:zombies game.round
tellraw @a ["",{"text":"","color":"dark_green","bold":true},"🧟 ",{"translate":"mgs.round","color":"green"},{"score":{"name":"#completed_round","objective":"mgs.data"},"color":"gold","bold":true},{"translate":"mgs.complete_next_round_in_5_seconds","color":"green"}]

# Schedule next round after 5 seconds
schedule function mgs:v5.0.0/zombies/start_round 5s

# Respawn all bled-out (spectator) players for the next round
function mgs:v5.0.0/zombies/revive/round_respawn

