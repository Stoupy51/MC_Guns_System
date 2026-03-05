
#> mgs:v5.0.0/multiplayer/time_up
#
# @within	mgs:v5.0.0/multiplayer/game_tick
#

# FFA: player with most kills wins
execute if data storage mgs:multiplayer game{gamemode:"ffa"} run function mgs:v5.0.0/multiplayer/ffa_time_up

# Team modes: team with more points wins
execute unless data storage mgs:multiplayer game{gamemode:"ffa"} if score #red mgs.mp.team > #blue mgs.mp.team run function mgs:v5.0.0/multiplayer/team_wins {team:"Red"}
execute unless data storage mgs:multiplayer game{gamemode:"ffa"} if score #blue mgs.mp.team > #red mgs.mp.team run function mgs:v5.0.0/multiplayer/team_wins {team:"Blue"}
execute unless data storage mgs:multiplayer game{gamemode:"ffa"} if score #red mgs.mp.team = #blue mgs.mp.team run function mgs:v5.0.0/multiplayer/game_draw

