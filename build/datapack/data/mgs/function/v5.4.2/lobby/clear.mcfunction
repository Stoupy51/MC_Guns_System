
#> mgs:v5.4.2/lobby/clear
#
# @within	mgs:v5.4.2/dialog/close_then
#			dialog mgs:v5.4.2/config/global
#

data remove storage mgs:config lobby
tellraw @s [[{"text":"","color":"gold"},"[",{"translate":"mgs","fallback":"MGS"},"] "],{"translate":"mgs.lobby_cleared_players_stay_where_their_game_ends","fallback":"Lobby cleared. Players stay where their game ends.","color":"yellow"}]

