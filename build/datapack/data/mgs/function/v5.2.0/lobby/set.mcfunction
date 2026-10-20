
#> mgs:v5.2.0/lobby/set
#
# @executed	as the player & at current position
#
# @within	dialog mgs:v5.2.0/config/global
#

data modify storage mgs:config lobby set value {}
data modify storage mgs:config lobby.dimension set from entity @s Dimension
data modify storage mgs:config lobby.x set from entity @s Pos[0]
data modify storage mgs:config lobby.y set from entity @s Pos[1]
data modify storage mgs:config lobby.z set from entity @s Pos[2]
data modify storage mgs:config lobby.yaw set from entity @s Rotation[0]
data modify storage mgs:config lobby.pitch set from entity @s Rotation[1]
tellraw @s [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"translate":"mgs.lobby_set_where_you_stand_players_return_here_when_their_game_en","color":"green"}]

