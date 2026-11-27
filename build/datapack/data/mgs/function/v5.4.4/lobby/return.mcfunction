
#> mgs:v5.4.4/lobby/return
#
# @within	mgs:v5.4.4/dialog/close_then
#			mgs:v5.4.4/missions/stop [ as @a[scores={mgs.mi.in_game=1}] ]
#			mgs:v5.4.4/zombies/reset_player
#			mgs:v5.4.4/multiplayer/reset_player
#

execute if data storage mgs:config lobby.dimension run function mgs:v5.4.4/lobby/teleport with storage mgs:config lobby

