
#> mgs:v5.4.3/lobby/return
#
# @within	mgs:v5.4.3/dialog/close_then
#			mgs:v5.4.3/missions/stop [ as @a[scores={mgs.mi.in_game=1}] ]
#			mgs:v5.4.3/zombies/reset_player
#			mgs:v5.4.3/multiplayer/reset_player
#

execute if data storage mgs:config lobby.dimension run function mgs:v5.4.3/lobby/teleport with storage mgs:config lobby

