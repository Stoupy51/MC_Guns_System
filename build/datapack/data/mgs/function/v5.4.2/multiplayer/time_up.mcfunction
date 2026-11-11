
#> mgs:v5.4.2/multiplayer/time_up
#
# @within	mgs:v5.4.2/dialog/close_then
#			mgs:v5.4.2/multiplayer/game_tick
#

# FFA: most kills wins.
execute if data storage mgs:multiplayer game{gamemode:"ffa"} run function mgs:v5.4.2/multiplayer/ffa_time_up

# Team modes: most points wins.
execute unless data storage mgs:multiplayer game{gamemode:"ffa"} if score #red mgs.mp.team > #blue mgs.mp.team run function mgs:v5.4.2/multiplayer/team_wins {team:"Red"}
execute unless data storage mgs:multiplayer game{gamemode:"ffa"} if score #blue mgs.mp.team > #red mgs.mp.team run function mgs:v5.4.2/multiplayer/team_wins {team:"Blue"}
execute unless data storage mgs:multiplayer game{gamemode:"ffa"} if score #red mgs.mp.team = #blue mgs.mp.team run function mgs:v5.4.2/multiplayer/game_draw

