
#> mgs:v5.1.0/lobby/clear
#
# @executed	as the player & at current position
#
# @within	dialog mgs:v5.1.0/config/global
#

data remove storage mgs:config lobby
tellraw @s [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"translate":"mgs.lobby_cleared_players_stay_where_their_game_ends","color":"yellow"}]

