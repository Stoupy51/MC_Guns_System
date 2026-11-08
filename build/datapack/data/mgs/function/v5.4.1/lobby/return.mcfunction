
#> mgs:v5.4.1/lobby/return
#
# @within	mgs:v5.4.1/dialog/close_then
#			mgs:v5.4.1/multiplayer/stop [ as @a[scores={mgs.mp.in_game=1}] ]
#			mgs:v5.4.1/missions/stop [ as @a[scores={mgs.mi.in_game=1}] ]
#			mgs:v5.4.1/zombies/reset_player
#

execute if data storage mgs:config lobby.dimension run function mgs:v5.4.1/lobby/teleport with storage mgs:config lobby

