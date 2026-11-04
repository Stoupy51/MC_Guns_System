
#> mgs:v5.3.0/lobby/return
#
# @within	mgs:v5.3.0/dialog/close_then
#			mgs:v5.3.0/multiplayer/stop [ as @a[scores={mgs.mp.in_game=1}] ]
#			mgs:v5.3.0/missions/stop [ as @a[scores={mgs.mi.in_game=1}] ]
#			mgs:v5.3.0/zombies/reset_player
#

execute if data storage mgs:config lobby.dimension run function mgs:v5.3.0/lobby/teleport with storage mgs:config lobby

