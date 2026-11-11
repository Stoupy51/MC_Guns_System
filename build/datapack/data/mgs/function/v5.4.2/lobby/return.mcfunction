
#> mgs:v5.4.2/lobby/return
#
# @within	mgs:v5.4.2/dialog/close_then
#			mgs:v5.4.2/missions/stop [ as @a[scores={mgs.mi.in_game=1}] ]
#			mgs:v5.4.2/zombies/reset_player
#			mgs:v5.4.2/multiplayer/reset_player
#

execute if data storage mgs:config lobby.dimension run function mgs:v5.4.2/lobby/teleport with storage mgs:config lobby

