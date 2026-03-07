
#> mgs:v5.0.0/multiplayer/gamemodes/ffa/on_kill
#
# @within	mgs:v5.0.0/multiplayer/on_kill_signal
#

# Only personal kill tracking (no team scoring)
scoreboard players add @s mgs.mp.kills 1

# Refresh FFA sidebar with updated rankings
function mgs:v5.0.0/multiplayer/refresh_sidebar_ffa

# Check win
execute store result score #score_limit mgs.data run data get storage mgs:multiplayer game.score_limit
execute if score @s mgs.mp.kills >= #score_limit mgs.data run function mgs:v5.0.0/multiplayer/gamemodes/ffa/player_wins

