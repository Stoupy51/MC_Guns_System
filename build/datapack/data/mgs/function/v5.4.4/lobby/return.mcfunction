
#> mgs:v5.4.4/lobby/return
#
# @within	mgs:v5.4.4/dialog/close_then
#			mgs:v5.4.4/zombies/reset_player
#			mgs:v5.4.4/multiplayer/reset_player
#			mgs:v5.4.4/missions/reset_player
#			mgs:v5.4.4/lobby/login
#			mgs:v5.4.4/lobby/send_home
#

execute if data storage mgs:config lobby.dimension run function mgs:v5.4.4/lobby/teleport with storage mgs:config lobby

execute if score #public_lobby mgs.config matches 1 if data storage mgs:config lobby.dimension run function mgs:v5.4.4/lobby/arrive

