
#> mgs:v5.4.4/multiplayer/release
#
# @within	mgs:v5.4.4/dialog/close_then
#			mgs:v5.4.4/multiplayer/stop 300t [ scheduled ]
#			mgs:v5.4.4/multiplayer/stop
#

data modify storage mgs:multiplayer game.state set value "lobby"
execute as @a[scores={mgs.mp.in_game=1}] run function mgs:v5.4.4/multiplayer/reset_player
scoreboard players set #mp_has_boundary mgs.data 0

