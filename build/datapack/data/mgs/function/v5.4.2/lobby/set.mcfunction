
#> mgs:v5.4.2/lobby/set
#
# @within	mgs:v5.4.2/dialog/close_then
#			dialog mgs:v5.4.2/config/global
#

data modify storage mgs:config lobby set value {}
data modify storage mgs:config lobby.dimension set from entity @s Dimension
data modify storage mgs:config lobby.x set from entity @s Pos[0]
data modify storage mgs:config lobby.y set from entity @s Pos[1]
data modify storage mgs:config lobby.z set from entity @s Pos[2]
data modify storage mgs:config lobby.yaw set from entity @s Rotation[0]
data modify storage mgs:config lobby.pitch set from entity @s Rotation[1]
tellraw @s [[{"text":"","color":"gold"},"[",{"translate":"mgs","fallback":"MGS"},"] "],{"translate":"mgs.lobby_set_where_you_stand_players_return_here_when_their_game_en","fallback":"Lobby set where you stand. Players return here when their game ends.","color":"green"}]

