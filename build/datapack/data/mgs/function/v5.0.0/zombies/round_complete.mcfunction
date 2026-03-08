
#> mgs:v5.0.0/zombies/round_complete
#
# @within	mgs:v5.0.0/zombies/game_tick
#

# Signal round end
function #mgs:zombies/on_round_end

# Title
title @a[scores={mgs.zb.in_game=1}] times 10 40 10
title @a[scores={mgs.zb.in_game=1}] title [{"translate": "mgs.round_complete","color":"green","bold":true}]

# Give all players 500 bonus points for surviving the round
execute as @a[scores={mgs.zb.in_game=1},gamemode=!spectator] run scoreboard players add @s mgs.zb.points 500

# Announce
execute store result score #_completed_round mgs.data run data get storage mgs:zombies game.round
tellraw @a ["",{"text":"","color":"dark_green","bold":true},"🧟 ",{"text":"Round ","color":"green"},{"score":{"name":"#_completed_round","objective":"mgs.data"},"color":"gold","bold":true},{"translate": "mgs.complete_500_points_next_round_in_10_seconds","color":"green"}]

# Schedule next round after 10 seconds
schedule function mgs:v5.0.0/zombies/start_round 200t

