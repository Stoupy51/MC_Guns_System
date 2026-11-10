
#> mgs:v5.4.1/multiplayer/kill_cam/close
#
# @within	mgs:v5.4.1/dialog/close_then
#			mgs:v5.4.1/multiplayer/gamemodes/snd/next_round
#			mgs:v5.4.1/multiplayer/kill_cam/cleanup
#

scoreboard players set #kc_window mgs.data 0
data remove storage mgs:kill_cam frames
data remove storage mgs:kill_cam deaths
data remove storage mgs:kill_cam pending_shots

